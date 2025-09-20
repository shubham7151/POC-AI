from app.services.interfaces.interfaces import IModelInfoInterface
from fastapi import HTTPException
import requests
from app.services.utils.litellm_util import LiteLLMClient
from app.core.logging.logger import logger

class ModelService(IModelInfoInterface):
    def __init__(self, llm_client: LiteLLMClient):
        self.llm_client = llm_client
        self.logger = logger

    def get_model_info(self, auth_token: str):
        try:
            url = f"{self.llm_client.base_url}/v1/models"
            if not auth_token.startswith("Bearer "):
                auth_token = f"Bearer {auth_token}"
            headers = {
                "Authorization": auth_token
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred while fetching model info: {http_err}")
            status_code = http_err.response.status_code if http_err.response else None
            if status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing auth token")
            elif status_code == 403:
                raise HTTPException(status_code=403, detail="Forbidden: Access denied")
            else:
                raise HTTPException(status_code=status_code or 500, detail=f"HTTP error: {http_err}")
        except requests.RequestException as e:
            raise Exception(f"Error communicating with llm : {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")