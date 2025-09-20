import requests
from app.core.config.settings import settings
from app.api.dependencies.pydantic_models import ChatCompletionRequest
from app.core.logging.logger import logger
from fastapi import HTTPException

class LiteLLMClient:

    def __init__(self):
        self.base_url = settings.litellm_base_url

    def chat_completion_request(self, payload: ChatCompletionRequest, auth_token: str):
        try:
            url = f"{self.base_url}/v1/chat/completions"

            if not auth_token.startswith("Bearer"):
                auth_token = f"Bearer {auth_token}"

            logger.debug(f"Sending request to LiteLLM at {url} with payload: {payload} and auth_token: {auth_token}")
            logger.debug(f"payload model dump: {payload.model_dump()}")
            headers = {
                "Authorization": auth_token,
                "Content-Type": "application/json"
            }
            response = requests.post(url, json=payload.model_dump(), headers=headers)
            response.raise_for_status()
            logger.debug(f"Received response from LiteLLM: {response.json()}")
            return response.json()
        except HTTPException as he:
            raise he
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            status_code = http_err.response.status_code
            if status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing auth token")
            raise HTTPException(status_code=status_code, detail=f"HTTP error: {http_err}")
        except requests.RequestException as e:
            raise Exception(f"Error communicating with llm : {e}")
        except Exception:
            raise Exception("Internal Server Error")
    
