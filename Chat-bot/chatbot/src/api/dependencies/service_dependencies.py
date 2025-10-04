from src.services.chat_services import ChatService
from src.db.repository import Database
from src.utils.llm_util import LLMUtil
from fastapi import Depends
from src.core.settings import settings

def get_db_service():
    db_config = {
        'DATABASE_URL': settings.DATABASE_URL
    }
    return Database(db_config).get_db()

def get_llm_service(model: str = "gemini-2.5-flash"):
    return LLMUtil(model)

def get_chat_service(
        db: Database = Depends(get_db_service), 
        llm: LLMUtil = Depends(get_llm_service)
        ):
    return ChatService(db, llm)

