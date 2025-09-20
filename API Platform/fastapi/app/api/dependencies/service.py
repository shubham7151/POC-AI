"""
This is a service dependency module.
"""

from app.services.implementations.chat_service import ChatService
from app.services.implementations.model_service import ModelService
from app.services.utils.litellm_util import LiteLLMClient

def get_chat_service() -> ChatService:
    llm_client = LiteLLMClient()
    chat_service = ChatService(llm_client=llm_client)
    return chat_service

def get_model_service() -> ModelService:
    llm_client = LiteLLMClient()
    model_service = ModelService(llm_client=llm_client)
    return model_service