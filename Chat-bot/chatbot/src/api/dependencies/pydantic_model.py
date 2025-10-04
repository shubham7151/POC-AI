from pydantic import BaseModel

class NewChat(BaseModel):
    pass

class NewChatResponse(BaseModel):
    session_id: str

class UserMessage(BaseModel):
    session_id: str
    message: str
