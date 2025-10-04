from src.db.repository import Database
from src.utils.llm_util import LLMUtil
from src.model.models import ChatSession

class ChatService:
    def __init__(self, db : Database , llm : LLMUtil ):
        self.db = db
        self.llm = llm

    def new_chat(self) -> str:
        """Initialize a new chat session and return the session ID."""

        db_generator = self.db.get_db()
        db_session = next(db_generator)
        try:
            # Create a new chat session in the database
            new_session = ChatSession()
            db_session.add(new_session)
            db_session.commit()
            db_session.refresh(new_session)
            return new_session.session_id
        finally:
            db_session.close()
        

    