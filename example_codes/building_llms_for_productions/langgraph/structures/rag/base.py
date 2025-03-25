from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings

from abc import ABC, abstractmethod
from operator import itemgetter
# from langchain import hub


class RetrievalChain(ABC):
    def __init__(self):
        self.source_uri = None
        self.k = 10

    @abstractmethod
    def load_documents(self, source_uris):
        """Load the document using loader."""
        pass

    @abstractmethod
    def create_text_splitter(self):
        """Create a text splitter."""
        pass

    def split_documents(self, docs, text_splitter):
        """Use the text splitter to split the document."""
        return text_splitter.split_documents(docs)

    def create_embedding(self):
        return OllamaEmbeddings(model='bge-m3:latest')

    def create_vectorstore(self, split_docs):
        return FAISS.from_documents(
            documents=split_docs, embedding=self.create_embedding()
        )

    def create_retriever(self, vectorstore):
        # Create a retriever that performs searches using the MMR algorithm.
        dense_retriever = vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": self.k}
        )
        return dense_retriever

    def create_model(self):
        return ChatOllama(model='qwen2.5:7b', temperature=0)

    def create_prompt(self):
        # return hub.pull("teddynote/rag-prompt-chat-history")
        return load_prompt('rag/prompts/rag-prompt-with-chat-history-vi.yaml')

    @staticmethod
    def format_docs(docs):
        return "\n".join(docs)

    def create_chain(self):
        docs = self.load_documents(self.source_uri)
        text_splitter = self.create_text_splitter()
        split_docs = self.split_documents(docs, text_splitter)
        self.vectorstore = self.create_vectorstore(split_docs)
        self.retriever = self.create_retriever(self.vectorstore)
        model = self.create_model()
        prompt = self.create_prompt()
        self.chain = (
            {
                "question": itemgetter("question"),
                "context": itemgetter("context"),
                "chat_history": itemgetter("chat_history"),
            }
            | prompt
            | model
            | StrOutputParser()
        )
        return self
