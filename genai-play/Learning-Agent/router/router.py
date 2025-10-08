from fastapi import APIRouter, Request
from service.service import invokellm
from utils.helper import invoke_functions, build_message
from settings import Settings
from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Optional, Union
from logger import logger#
from utils.helper import get_function_schema, get_system_prompt
settings = Settings()
router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": "Hello from Learning-Agent router!"}

class ChatRequest(BaseModel):
    user_id: str
    context: Optional[str] = None

@router.post("/pla")
async def chat(request: Request, chat_request: ChatRequest):
    try:
        state = None
        body = await request.json()
        #**** generate request structure
        user_id = body.get("user_id", "1")
        page_context = body.get("context", None)

        messages = [
            {"role": "system", "content": f"{get_system_prompt()}"},
            ]
        messages.append({"role": "user", "content": f"User ID is {user_id}. {page_context if page_context else ''}"})
        request = {
            "model": "gpt-4o",
            "messages": messages,
            "functions": get_function_schema(),
            "response_format": {"type":"json_object"},
        }
        logger.info(f"Request to LLM: {request}")
        finish_reason = ""
        while finish_reason != "stop":
            response = invokellm(request)
            logger.info(f"LLM Response: {response}")
            finish_reason = response.get("choices", [{}])[0].get("finish_reason", "stop")
            function_call = response.get("choices", [{}])[0].get("message", {}).get("function_call", None)
            if function_call:
                
                arguments = function_call.get("arguments")
                function_response = invoke_functions(function_call, arguments)
                messages = build_message(messages, function_response)
                body["messages"] = messages
        import json
        return json.loads(response["choices"][0]["message"]["content"], strict=False)
    except Exception as e:
        logger.error(f"Error in /pla endpoint: {e}")
        return {
            "content": "Hi Alice, it's great to see that you've already started investing and have diversified across different accounts like ISAs and stocks. To help you refine and build your portfolio further. This quick video by Dan Coatsworth breaks down practical steps for constructing a balanced investment portfolio. It’s an excellent way to ensure your investments align with your financial goals. Happy learning!",
            "links": ["https://www.ajbell.co.uk/investment/videos/how-build-investment-portfolio", "https://www.ajbellmoneymatters.co.uk/podcasts/investing-art"]
        }