from langchain_google_genai import GoogleGenerativeAI
from src.core.settings import settings

class LLMUtil:
    def __init__(self, model: str ):
        self.llm = GoogleGenerativeAI(model=model, api_key=settings.GOOGLE_API_KEY)

    def generate_response(self, prompts: list):
        return self.llm.invoke(prompts)
    
    
