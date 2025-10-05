from src.api.dependencies.pydantic_model import Message
from src.model.models import ChatMessage
from src.core.logger import logger
from src.model.models import ChatSession, ChatMessage
from sqlalchemy import desc


class ChatUtil:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_chat_history(self, session_id):
        chat_message_history = (
            self.db_session.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(desc(ChatMessage.created_at))
            .limit(10)
            .all()
        )
        return chat_message_history
            

    def generate_message(self, message: str, role: str) -> dict:
        if message and role and role in ["system", "user", "assistant"]:
            return {
                "role": role,
                "content": message
            }
        else:
            raise ValueError("Message is null or invalid role")
    
    def chat_new_session(self):
        try:
            new_session = ChatSession()
            self.db_session.add(new_session)
            self.db_session.commit()
            self.db_session.refresh(new_session)

            return {
                "session_id": str(new_session.id)
            }
        except Exception as e:
            logger.error(f"Issue creating session {e}", exc_info=True)
            raise e
        
    def update_chat(self, message: Message, role:str):
        try:
            new_message = ChatMessage(
                session_id = message.session_id,
                role= role,
                content=message.content,
            )
            self.db_session.add(new_message)
            self.db_session.commit()
            self.db_session.refresh(new_message)
        except Exception as e:
            logger.error(f"Error updating message {e}", exc_info=True)
            raise e
        
    def convert_to_openai_format(self, chat_history:list):
        messages = []
        system_prompt = {
            "role":"system",
            "content":"you are a chat bot name babbu"
        }
        messages.append(system_prompt)
        for chat in chat_history:
            messages.append(self.generate_message(chat.content,chat.role))
        return messages
