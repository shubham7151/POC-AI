from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies.pydantic_model import (
    Message, 
    NewChat,
    NewChatResponse
)
from src.api.dependencies.service_dependencies import get_chat_service
from src.services.chat_services import ChatService
from src.core.logger import logger

router = APIRouter()

@router.get("/chat/new", tags=["chat"], response_model=NewChatResponse)
def new_chat(
    chat_service: ChatService = Depends(get_chat_service)
):
    logger.info(f"New Chat Service started : Start")
    try:
        response = chat_service.new_chat()
        logger.info(f"New Chat Service completed : Success")
        return response
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"New Chat Service error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

# chat/message
@router.post("/chat/message", tags=["chat"], response_model=Message)
def new_message(
    message: Message,
    chat_service: ChatService = Depends(get_chat_service)
):
    logger.info("chat message service started: Start")
    try:
        response = chat_service.new_message(message=message)
        return response
    except Exception as e:
        logger.error(f"New Message error {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

