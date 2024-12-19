# Result
[Demonstrate video](https://drive.google.com/file/d/1bObr33S6Ytk02Fy1US9B5P5PCU23HKIq/view)
# Business Context

Kotak Mahindra Bank is one of India's premier banking and financial services institutions, offering a wide range of online banking services in addition to our long-standing presence through an extensive network of branches across the country. 

As part of our ongoing growth strategy, we are focused on expanding our online banking services to attract a larger customer base. However, we are currently facing challenges due to a lack of awareness among customers regarding internet banking practices, resulting in delays in responding to customer inquiries and issues. These delays have led to customer dissatisfaction.

To address this, we are committed to implementing a solution that resolves common customer concerns efficiently, thereby enhancing their experience and encouraging more customers to join our bank.

# Business Problem
### Objective
- Expand the online banking network by attracting more customers to Kotak Mahindra Bank.
- Improve customer satisfaction by addressing common issues and reducing response times.
- Enhance digital literacy among customers to ensure smoother interactions with the online banking platform.

### Challenges
- Lack of awareness and understanding of internet banking practices among customers.
- Delayed response times in addressing customer issues due to insufficient support infrastructure.
- Negative customer perception of online banking services due to unresolved concerns and inefficiencies.
- Difficulty in scaling customer support to meet the increasing demand for digital banking services.

### Solution
- Develop and integrate automated solutions (e.g., chatbots, FAQs) to provide quicker responses to common customer queries.

# Solution

To address the challenges of delayed response times and enhance customer satisfaction, we propose the development and implementation of a **RAG (Retrieve and Generate)** system. This system will leverage an **FAQ dataset** to provide fast, relevant, and accurate responses to customer queries, significantly improving the overall customer experience with our online banking platform.

#### Key Components of the RAG System:
- **Retrieve**: The system will first retrieve relevant documents or answers from a pre-existing FAQ dataset based on the user's query. By using advanced Natural Language Processing (NLP) techniques, the RAG system will analyze the customer's question and fetch the most pertinent information from the available knowledge base.
  
- **Generate**: In cases where a direct answer isn't available in the FAQ database, the system will generate an appropriate response using language generation models. This allows the system to handle queries that might not have been specifically anticipated, while still providing meaningful answers.

#### Benefits of the RAG System:
- **Faster Response Times**: By automating the query resolution process, the RAG system will significantly reduce response times, enabling customers to get quick answers to their concerns without having to wait for human intervention.
  
- **Accurate and Relevant Information**: By using a comprehensive FAQ dataset and advanced retrieval techniques, the system ensures that the information provided is accurate and highly relevant to the customer’s inquiry.

- **Scalability**: The RAG system can handle a high volume of queries simultaneously, allowing us to scale customer support operations without a proportional increase in staffing.

- **Enhanced Customer Satisfaction**: By delivering timely, reliable, and easy-to-understand responses, we can significantly improve customer satisfaction, thereby encouraging more customers to engage with and join our online banking platform.

# Workflow
1. Fetch FAQs data through web-scrapping
2. Data Preprocessing (if needed)
3. store data in database with embedding
4. build rag chain model
5. evaluate the model with test dataset
6. Build api app with FastAPI
7. Deploy on AWS

# Technologies

### 1. **Version Control and Collaboration**
- **Git**
  - **Purpose:** A distributed version control system for tracking changes in source code.
  - **Usage:** Git is used to manage the codebase, track modifications, and allow multiple developers to collaborate seamlessly on the same project.

- **GitHub**
  - **Purpose:** A cloud-based hosting service for Git repositories with added collaboration features.
  - **Usage:** GitHub facilitates the storage of code repositories, issue tracking, pull requests, and team collaboration, ensuring smooth project management and version control across distributed teams.

### 2. **Web Scraping**
- **Requests**
  - **Purpose:** A simple HTTP library used for sending requests to web pages and retrieving their content.
  - **Usage:** The `requests` library is utilized to make HTTP requests and scrape data from web pages to collect relevant information for the FAQ dataset or related purposes.

- **Selenium**
  - **Purpose:** A powerful web automation tool used to interact with web pages programmatically.
  - **Usage:** Selenium is employed to scrape dynamic content from websites or automate web interactions, such as fetching real-time data, which is crucial for maintaining an up-to-date FAQ database or other relevant data sources.

### 3. **Database**
- **MongoDB**
  - **Purpose:** A NoSQL database known for its flexibility and scalability.
  - **Usage:** MongoDB stores and manages large volumes of unstructured data, such as customer queries and responses, as well as the FAQ dataset, enabling efficient retrieval and scaling as the system grows.

### 4. **Large Language Models (LLMs)**
- **Ollama**
  - **Purpose:** A framework for building and deploying large language models.
  - **Usage:** Ollama enables us to utilize advanced NLP models to power the question-answering system, ensuring that responses are contextually accurate and coherent.

- **Gemini**
  - **Purpose:** A suite of AI models designed to handle complex language understanding and generation tasks.
  - **Usage:** Gemini can be integrated to enhance the LLM-based query generation capabilities, enabling it to process diverse customer inquiries and provide reliable responses.

- **Groq**
  - **Purpose:** A cloud based api designed to make calls llm models based on cloud.
  - **Usage:** Groq will be used to speed up the inference process for large-scale LLMs, reducing latency and improving real-time response times when serving customer queries.

### 5. **RAG Chain**
- **Langchain**
  - **Purpose:** A framework for building applications that combine LLMs with external data sources.
  - **Usage:** Langchain will be used to link the RAG (Retrieve and Generate) system with the FAQ dataset and other relevant external data sources. It enables the efficient retrieval of information based on customer queries and the generation of precise responses.

### 6. **Evaluation**
- **RAGas**
  - **Purpose:** A tool to evaluate the performance and accuracy of RAG systems.
  - **Usage:** RAGas will be used to assess how well the RAG system performs in delivering relevant and accurate answers to customer queries, enabling continuous improvement of the model and response quality.

# Evalute metrics
 - **answer_relevancy:**  0.879
 - **context_precision:** 0.926
 - **faithfulness:** 0.941