from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
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
    """
    Initialize a new chat session and return the session ID.
    """
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
    """
    Process a new message in an existing chat session and return the assistant's response.
    """
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

@router.get("/chat/{session_id}", tags=["chat"])
def get_chat_history(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Retrieve the chat history for a given session ID.
    """
    logger.info(f"Get Chat History Service started for session_id: {session_id}")
    try:
        chat_history = chat_service.chat_util.get_chat_history(session_id)
        logger.info(f"Get Chat History Service completed for session_id: {session_id}")
        chat_content = [
            {
                "role":chat.role,
                "content":chat.content
            }
            for chat in reversed(chat_history)
        ]
        return chat_content
    except Exception as e:
        logger.error(f"Get Chat History error {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    
@router.post("/document/add", tags=["document"])
def add_documents(
    uploaded_file: UploadFile = File(...),
):
    """
    Endpoint to add documents to the system.
    """
    logger.info("Add Documents Service started: Start")
    try:
        fileNmae = uploaded_file.filename
        logger.info(f"Uploaded file name: {fileNmae}")
        return {"detail": "Documents added successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Add Documents error {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/document/embedd", tags=["document"])
def get_document_embeddings(
    text: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Endpoint to get document embeddings for a given text.
    """
    logger.info("Get Document Embeddings Service started: Start")
    try:
        embeddings = chat_service.llm.get_embeddings(text)
        logger.info("Get Document Embeddings Service completed: Success")
        return {"embeddings": embeddings}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Get Document Embeddings error {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )