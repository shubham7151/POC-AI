from src.db.repository import Database
from src.utils.llm_util import LLMUtil
from src.utils.chat_util import ChatUtil
from src.core.logger import logger
from src.api.dependencies.pydantic_model import Message
from fastapi import HTTPException

class ChatService:
    def __init__(self, chat_util: ChatUtil , llm : LLMUtil ):
        self.llm = llm
        self.chat_util = chat_util

    def new_chat(self):
        """Initialize a new chat session and return the session ID."""
        try:
            # Create a new chat session in the database
            session = self.chat_util.chat_new_session()
            return session
        except Exception as e  :
            logger.error("Error in creating new session", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error"
            )

    def new_message(self, message: Message):
        """
        Update Db with new user message and assitant message
        """
        try:
            # update user message into db
            self.chat_util.update_chat(message=message,role= "user")
            # fetch previous chat history
            chat_history = self.chat_util.get_chat_history(message.session_id)
            # convert chat history to OpenAI format
            llm_message = self.chat_util.convert_to_openai_format(chat_history)
            # invoke llm call 
            response = self.llm.generate_response(llm_message)
            # update assistant message
            assistant_message = Message(
                session_id=message.session_id,
                content=response
            )
            self.chat_util.update_chat(assistant_message, role="assistant")
            logger.info(f"response from llm {response}")
            return {
                "session_id" : message.session_id,
                "content" : response
            }
        except Exception as e:
            logger.error(f"Unexpected Error {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error"
            )

        

    