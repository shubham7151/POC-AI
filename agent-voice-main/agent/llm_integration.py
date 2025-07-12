import requests
import json
import os
from dotenv import load_dotenv


from utils.chat_util import get_system_prompt_gemini

load_dotenv()  # Load environment variables from .env file
GENAI_LLM_CERT = os.getenv("LLM_CERT")
env = os.getenv("ENV", "development")

def llm_integration(chat_history, genai_key, logger):
    try:
        url = "https://genaiplatform.ajbpoc.co.uk/v1/chat/completions"
        try:
            payload = json.dumps({
                "model": "gpt-4o",
                "messages": chat_history,
                "max_tokens": 512,
                "temperature": 0.1,
                "stream": True,
                "redact_pii": False
            })
        except json.JSONDecodeError as e:
            logger.error(f"Error serializing payload to JSON: {e}")
            return None

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {genai_key}'
        }

        dir_path = os.path.dirname(os.path.realpath(__file__))
        cert_path = os.path.join(dir_path, "..", "resource", "genaiplatform.ajbpoc.co.uk.crt")
        cert_path = os.path.abspath(cert_path)

        try:
            if env == "production":
                llm_response = requests.request("POST", url, headers=headers, data=payload, stream=True, timeout=10)
            else:
                llm_response = requests.request("POST", url, headers=headers, data=payload, verify=cert_path, stream=True, timeout=10)

        except requests.RequestException as e:
            logger.error(f"Error making request to LLM API: {e}")
            return None

        return llm_response
    except Exception as e:
        logger.error(f"Unexpected error in llm_integration: {e}")
        return None

def alt_llm_integration(chat_history, genai_key, logger, user):
    try:
        model_name = "gemini-2.0-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={genai_key}"

        payload = {
            "systemInstruction": get_system_prompt_gemini(user)["systemInstruction"], 
            "contents": chat_history,
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 512
            }
        }

        headers = {
            "Content-Type": "application/json"
        }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cert_path = os.path.join(dir_path, "..", "resource", "genaiplatform.ajbpoc.co.uk.crt")
        cert_path = os.path.abspath(cert_path)
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10, stream=False)

        return response.json()

    except requests.RequestException as e:
        logger.error(f"Error calling Gemini 2.5 Flash‑Lite: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
    
def format_for_gemini(chat_history):
    formatted = []
    for message in chat_history:
        role = message.get("role")
        content_blocks = message.get("content", [])
        # Extract only the 'text' parts
        text_parts = [block.get("text", "") for block in content_blocks if block.get("type") == "text"]
        if text_parts:
            formatted.append({"role": role, "parts": text_parts})
    return formatted
