from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain.chains import create_retrieval_chain
import os
from dotenv import load_dotenv
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from src.ChatHistory import get_chat_history, add_chat
load_dotenv()

def embeddings_():
    return (
         OllamaEmbeddings(
         model="nomic-embed-text:latest",
        )
    )

def llm_model():
    return (
        ChatOllama(
        model="llama3.2:3b",
        temperature=0,
        # other params...
    )
    )




def vector_store_retriever():
    MONGODB_ATLAS_CLUSTER_URI = os.environ['MONGODB_ATLAS_CLUSTER_URI']
    # initialize MongoDB python client
    client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
    embeddings = embeddings_()

    DB_NAME = "langchain_db"
    COLLECTION_NAME = "langchain_vectorstores"
    ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-index-vectorstores"

    MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        relevance_score_fn="cosine",
    )
    return vector_store.as_retriever(search_kwargs={"k": 3})

def rag_chain(input_, chat_history):

    vectorstore_retriever = vector_store_retriever()
    llm = llm_model()

    contextualize_q_system_prompt = """
    Given a chat history and the latest user question
    which might reference context in the chat history,
    formulate a standalone question which can be understood
    without the chat history. Do NOT answer the question,
    just reformulate it if needed and otherwise return it as is.
    """

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, vectorstore_retriever, contextualize_q_prompt
    )

    system_prompt = (
        "You are a bank customer care bot who provide "
        "who provide solution to customer input"
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use five sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return chain.invoke({"input": input_, "chat_history": chat_history,"context":history_aware_retriever})["answer"]

def chatbot(input_, session_id):

    chat_history = get_chat_history(session_id)

    answers = rag_chain(input_, chat_history)

    add_chat(input_, answers,session_id)

    return answers