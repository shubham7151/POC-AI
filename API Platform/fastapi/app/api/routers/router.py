from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.openapi.utils import get_openapi
from app.api.dependencies.pydantic_models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
)
from app.services.implementations.chat_service import ChatService
from app.core.logging.logger import logger
from app.api.dependencies.service import (
    get_chat_service,
    get_model_service
)

router = APIRouter()
header_schema = APIKeyHeader(name= "Authorization", auto_error=False)

@router.get("/apiKey")
async def show_api_key(auth_key : str = Depends(header_schema)):
    return {
        "Authorization" : auth_key
    }

@router.get("/schema-debug")
def get_openapi_schema_debug(request : Request):
    
    app = request.app
    return get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes
    )

@router.get("/model", tags=["model"], summary="Get model information")
def get_model_info(
    auth_token: str = Depends(header_schema),
    model_service = Depends(get_model_service)
):
    response = model_service.get_model_info(auth_token)
    return response


@router.post("/v1/chat/completions", tags=["chat"], summary="Chat completion endpoint", response_model=ChatCompletionResponse)
def chat_completion(
    chat_request: ChatCompletionRequest,
    chat_service: ChatService = Depends(get_chat_service),
    auth_token: str = Depends(header_schema)
):
    try:
        logger.info(f"Received chat completion request: {chat_request}")
        response = chat_service.chat_completion(chat_request, auth_token)
        logger.info(f"Chat completion response: {response}")
        return response
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in chat completion: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    