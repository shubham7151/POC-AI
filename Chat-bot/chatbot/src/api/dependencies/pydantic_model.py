from pydantic import BaseModel

class NewChat(BaseModel):
    pass

class NewChatResponse(BaseModel):
    session_id: str

class Message(BaseModel):
    session_id: str
    content: str

