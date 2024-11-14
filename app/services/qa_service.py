from langchain_community.document_loaders import PyPDFLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from app.core.config import get_settings
from dotenv import load_dotenv
import json
import os
load_dotenv()

settings = get_settings()

class QAService:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4o",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def process_document(self, file_path: str, file_type: str):
        """Process uploaded document based on file type."""
        if file_type == "pdf":
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif file_type == "json":
            def metadata_func(record: dict, metadata: dict) -> dict:
                metadata["content"] = record.get("content")
                return metadata

            loader = JSONLoader(
                file_path=file_path,
                jq_schema=".content",
                metadata_func=metadata_func
            )
            documents = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        splits = self.text_splitter.split_documents(documents)
        vectorstore = FAISS.from_documents(splits, self.embeddings)
        return vectorstore

    def create_qa_chain(self, vectorstore):
        """Create a question-answering chain."""
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_kwargs={"k": settings.VECTOR_SEARCH_K}
            ),
            return_source_documents=True
        )

    def load_questions(self, questions_path: str):
        """Load and parse questions from JSON file."""
        with open(questions_path, 'r') as f:
            questions_list = json.load(f)

        parsed_questions = []
        for q in questions_list:
            if isinstance(q, dict) and 'question' in q:
                parsed_questions.append(q['question'])
            elif isinstance(q, str):
                parsed_questions.append(q)

        return parsed_questions