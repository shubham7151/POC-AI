from abc import ABC, abstractmethod
from app.api.dependencies.pydantic_models import ChatCompletionRequest

class IChatCompletionInterface(ABC):
    
    @abstractmethod
    def chat_completion(self, chat_request : ChatCompletionRequest, auth_token: str)-> dict:
        pass

class IModelInfoInterface(ABC):
    
    @abstractmethod
    def get_model_info(self, auth_token: str):
        pass