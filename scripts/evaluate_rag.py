import os
from dotenv import load_dotenv
import json
import pandas as pd
from langchain_groq import ChatGroq
from src.chatbot import vector_store_retriever,rag_chain
from langchain_ollama import OllamaEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
load_dotenv()

class Evaluator:
    def __init__(self):
        self.embedding_llm = self.get_embeddings_llm()
        self.evaluator_llm = self.get_evaluator_model()
        self.dataset = self.get_dataset()
        pass

    @staticmethod
    def get_embeddings_llm():
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text:latest",
        )

        return LangchainEmbeddingsWrapper(embeddings)

    @staticmethod
    def get_evaluator_model():
        llm = ChatGroq(temperature=0, model_name="gemma2-9b-it")
        return LangchainLLMWrapper(llm)

    @staticmethod
    def get_dataset():
        test_set = pd.read_csv("../data/test_set.csv")

        questions = test_set["question"].tolist()
        ground_truths = test_set["ground_truth"].tolist()

        answers = []
        content = []

        vector_store = vector_store_retriever()

        for question in questions[:5]:
            answer = rag_chain(question, chat_history=[])
            answers.append(answer)
            content.append([docs.page_content for docs in vector_store.get_relevant_documents(question)])

        data = {
            "question": questions[:5],
            "ground_truth": ground_truths[:5],
            "response": answers[:5],
            "contexts": content[:5]
        }

        return Dataset.from_dict(data)


    def evaluate(self):

        result = evaluate(
            self.dataset,
            metrics=[
                answer_relevancy,
                context_recall,
                context_precision,
                faithfulness,
            ],
            llm=self.evaluator_llm,
            embeddings=self.embedding_llm,
        )

        result.to_pandas().to_csv("../report/evaluation_results.csv",index=False)

if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.evaluate()