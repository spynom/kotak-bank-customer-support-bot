from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
load_dotenv()


def get_chat_history(session_id):
    chat_history = []
    # Your connection URI
    uri = os.getenv('MONGODB_ATLAS_CLUSTER_URI')

    # Create a client instance and connect to MongoDB
    client = MongoClient(uri)

    # Access a database
    db = client['langchain_db']

    collection = db['sessions']  # Create or access the 'sessions' collection

    # Fetch data ordered by 'date' in ascending order
    sorted_documents = collection.find({'session_id':session_id}).sort('date', -1)  # 1 for ascending, -1 for descending

    for num, doc in enumerate( sorted_documents):
        chat_history.append(HumanMessage(content=doc["query"]))
        chat_history.append(AIMessage(content=doc["answer"]))
        if num >5:
            break

    return chat_history

def add_chat(query,answer, session_id):
    # Your connection URI
    uri = os.getenv('MONGODB_ATLAS_CLUSTER_URI')

    # Create a client instance and connect to MongoDB
    client = MongoClient(uri)

    # Access a database
    db = client['langchain_db']

    collection = db['sessions']  # Create or access the 'sessions' collection

    collection.insert_one({'session_id':session_id,'date':datetime.now(), 'query':query, 'answer':answer})