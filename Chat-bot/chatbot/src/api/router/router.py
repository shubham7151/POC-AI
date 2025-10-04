from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies.pydantic_model import (
    UserMessage, 
    NewChat,
    NewChatResponse
)
from src.api.dependencies.service_dependencies import get_chat_service
from src.services.chat_services import ChatService
from src.core.logger import logger

router = APIRouter()

@router.post("/chat/new", tags=["chat"], response_model=NewChatResponse)
def new_chat(
    chat: NewChat,
    chat_service: ChatService = Depends(get_chat_service)
):
    logger.info(f"New Chat Service started : Start")
    try:
        response = chat_service.new_chat()
        logger.info(f"New Chat Service completed : Success")
        return {"response": response}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"New Chat Service error: {str(e)}")
        return {"error": str(e)}
