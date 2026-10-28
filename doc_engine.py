import os
from dotenv import load_dotenv
# pyrefly: ignore[missing-import]
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
# pyrefly: ignore[missing-import]
from llama_index.llms.groq import Groq
# pyrefly: ignore[missing-import]
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment")

# Configure LLM and local HuggingFace embeddings
Settings.llm = Groq(model="openai/gpt-oss-120b", api_key=groq_api_key)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

def query_documents(user_query: str) -> str:
    response = query_engine.query(user_query)
    return str(response)