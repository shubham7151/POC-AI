from pydantic import BaseModel
from typing import Optional

class ChatCompletionRequest(BaseModel):
    model : str
    messages : list[dict]
    temperature : Optional[float] = 1.0
    top_p : Optional[float] = 1.0
    stream : Optional[bool] = False
    stop : Optional[list[str]] | None = None
    max_tokens : Optional[int] | None = None
    response_format : Optional[dict] | None = None 

class ChatCompletionResponse(BaseModel):
    response: str