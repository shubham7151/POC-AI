from langchain_google_genai import GoogleGenerativeAI

class LLMUtil:
    def __init__(self, model: str ):
        self.llm = GoogleGenerativeAI(model=model)

    def generate_response(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
    
