from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from src.core.settings import settings
import os

class LLMUtil:
    def __init__(self, model: str ):
        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        self.llm = GoogleGenerativeAI(model=model, api_key=settings.GOOGLE_API_KEY)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",api_key=settings.GOOGLE_API_KEY)
    
    def generate_response(self, prompts: list):
        return self.llm.invoke(prompts)
    
    def get_embeddings(self, text: str):
        return self.embeddings.embed_query(text)
