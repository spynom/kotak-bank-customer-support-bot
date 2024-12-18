import requests
from bs4 import BeautifulSoup
import time
import json

from Logger import get_logger

logger = get_logger('ScrapData')

extracted_data = {
    "data": [],
}

urls = []

def response_status(response: requests.Response):
    if response.status_code == 200:
        return True
    else:
        logger.error(f"Request failed with status code: {response.status_code}")
        raise Exception(f"Failed to get data from {response.url}, status code: {response.status_code}")

def check_faq_landing(soup: BeautifulSoup):
    return soup.find('div', attrs={'class': 'FAQ-landing'}) is not None

def scrap_faq(url, extracted_data):
    #time.sleep(0.25)  # To avoid hammering the server with requests

    if url not in urls:
        urls.append(url)
    else:
        return None

    try:
        response = requests.get(url)
        if response_status(response):
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')


            if check_faq_landing(soup):
                query = soup.find('ul', attrs={'class': 'breadcrumb self-span'})
                solution = soup.find('div', attrs={'class': 'FAQ-landing'})

                if query and solution:
                    query_text = query.text.strip()
                    solution_text = (solution.find('div', attrs={'class': 'FAQ-landing-content'})
                                     .find('div', attrs={'class': 'selfhelpanswer self-span answerself-help'})
                                     .text.strip())

                    extracted_data["data"].append({
                        'query': query_text,
                        'solution': solution_text,
                        'url': url
                    })

                    logger.info(f"Processed URL: {url}")
                else:
                    logger.warning(f"Missing data in FAQ landing for URL: {url}")

            else:
                # Recursively process FAQ list content if FAQ-landing is not found

                base_url = 'https://www.kotak.com'
                faq_urls = soup.find_all('div', class_="FAQ-list-content FAQ-list-bottom")
                for faq in faq_urls:
                    faq_url = faq.find('a').get('href')
                    scrap_faq(f"{base_url}{faq_url}", extracted_data)

    except Exception as e:
        logger.error(f"Error processing URL {url}: {str(e)}")

def scrap_and_save(url, file_path):
    scrap_faq(url, extracted_data)

    # Save the extracted data to a JSON file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)
            logger.info(f"Data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data to file: {str(e)}")

if __name__ == '__main__':
    scrap_and_save('https://www.kotak.com/en/help-center.html', 'data/scrappedFQA.json')
