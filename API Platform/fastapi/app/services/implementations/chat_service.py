from app.services.utils.litellm_util import LiteLLMClient
from app.services.interfaces.interfaces import IChatCompletionInterface
from app.core.logging.logger import logger
from app.api.dependencies.pydantic_models import ChatCompletionRequest
from fastapi import HTTPException
import requests

class ChatService(IChatCompletionInterface):
    def __init__(self, llm_client: LiteLLMClient):
        self.llm_client = llm_client
        self.logger = logger

    def chat_completion(self, chat_request : ChatCompletionRequest, auth_token: str)-> dict:
        try:
            self.logger.info(f"Processing chat completion request for model: {chat_request.model}")
            response = self.llm_client.chat_completion_request(payload=chat_request, auth_token=auth_token)
            return {"response":response["choices"][0]["message"]["content"]}
        except HTTPException as he:
            raise he
        except Exception:
            raise Exception("Internal Server Error")