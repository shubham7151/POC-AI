from src.services.chat_services import ChatService
from src.db.repository import Database
from src.utils.llm_util import LLMUtil
from src.utils.chat_util import ChatUtil
from fastapi import Depends
from src.core.settings import settings
from sqlalchemy.orm import Session

def get_db_service():
    db_config = {
        'DATABASE_URL': settings.DATABASE_URL
    }
    return Database(db_config)

def get_db_session(db: Database = Depends(get_db_service)):
    yield from db.get_db()

def get_llm_service(model: str = "gemini-2.5-flash") -> LLMUtil:
    return LLMUtil(model)

def get_chat_util(db_session = Depends(get_db_session)) -> ChatUtil:
    return ChatUtil(db_session)

def get_chat_service(
        chat_util: ChatUtil = Depends(get_chat_util),
        llm: LLMUtil = Depends(get_llm_service)
        )-> ChatService:
    return ChatService(chat_util, llm)

