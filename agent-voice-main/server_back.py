from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from typing import Dict
from dataclasses import dataclass, field
from datetime import datetime
#from twilio.rest import Client
import os
import requests
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from agent.llm_integration import llm_integration, alt_llm_integration # Import the LLM integration function
from utils.chat_util import get_system_prompt, generateChatHistory  ,get_system_prompt_gemini, chat_history_format_for_gemini
import asyncio

#from utils.db_util import getUserDetails, updateDatabase # Import the function to get user details 
import os

load_dotenv()  # This loads the .env file into the environment

genai_key = os.getenv("GENAI_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
backend_url = os.getenv("BACKEND_URL")
env = os.getenv("ENV", "development")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcription_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

caller_sid = None

response_queue = asyncio.Queue()
user_record = {
    "cust_id" : 1,
    "name": "Ekiyor",
    "dob": "1999-01-01", 
}

class TranscriptionDataModel(BaseModel):
    transcript: str
 
 
class TwilioTranscriptionRequest(BaseModel):
    LanguageCode: str
    TranscriptionSid: str
    Stability: float
    TranscriptionEvent: str
    CallSid: str
    TranscriptionData: TranscriptionDataModel
    Timestamp: datetime
    Final: bool
    AccountSid: str
    Track: str
    SequenceId: int


# userDetails = getUserDetails()

chat_history = []
local_caller_sid = None
#chat_history = get_system_prompt(user=None)

UI_STATUS = "started"


@app.post("/twilio-text-response/{caller_sid}")
async def twilio_text_response(caller_sid:str, request: Request):
    try:
        global  UI_STATUS
        UI_STATUS = "collecting"
        form_data = await request.form()
        
        event_type = form_data.get("TranscriptionEvent")

        if event_type == "transcription-started":
            logger.info(f"Transcription started for {caller_sid}")
            

        elif event_type == "transcription-content":
            transcription_data = form_data.get("TranscriptionData")
            transcript = ""
            if transcription_data:
                try:
                    data_dict = json.loads(transcription_data)
                    transcript = data_dict.get("transcript", "")
                except json.JSONDecodeError:
                    logger.warning("Could not parse TranscriptionData")

            is_final = form_data.get("Final") == "true"
            
            if is_final:
                logger.info(f"Final transcription received for {caller_sid}: {transcript}")
                chat_history_format_for_gemini(chat_history, transcript, "user", logger)
                
                llm_response = alt_llm_integration(
                    chat_history=chat_history,
                    genai_key=gemini_api_key,
                    logger=logger,
                    user=user_record
                )
                if llm_response is None:

                    headers = {'Content-Type': 'application/json'}
                    payload = json.dumps({
                        "response_text": "Sorry!, There is some issue with the backend service. Will call you later.",
                        "action": "hangup"
                    })
                    requests.post(f"{base_url}/respond/{caller_sid}", json=payload, headers=headers)

                elif llm_response:
                    response_data = llm_response
                    try:
                        for candidate in response_data.get("candidates", []):
                            print(f"Candidate: {candidate}")
                        logger.info(f"Response Data from Gemini: {response_data}")
                        response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
                        chat_history_format_for_gemini(chat_history, response_text, "model", logger)
                        headers = {
                            'Content-Type': 'application/json',
                        }
                        payload = json.dumps({
                            "response_text": f"{response_text}",
                            "action": "speak"
                            })
                        
                        if("INFORMATION_COLLECTED" in response_text):
                            payload = json.dumps({
                                "response_text": f"Thank you for your time. Your email has been updated successfully.",
                                "action": "hangup"
                                })
                            
                            UI_STATUS = "updating"
                            
                            # parts = response_text.split('end', 1)

                            # # The first part is before 'end'
                            # message_part = parts[0].strip()

                            # # The second part is after 'end'
                            # json_text = parts[1].strip()

                            # # Extract the JSON object from the text (assumes it starts with a { and ends with a })
                            # start = json_text.find('{')
                            # end = json_text.rfind('}') + 1
                            # json_data = json.loads(json_text[start:end])

                        requests.request("POST", f"{base_url}/respond/{caller_sid}", headers=headers, data=payload)
                            
                        
                        dir_path = os.path.dirname(os.path.realpath(__file__))
                        cert_path = os.path.join(dir_path, "resource", "genaiplatform.ajbpoc.co.uk.crt")
                        

                    except (KeyError, IndexError) as e:
                        logger.error(f"Error parsing Gemini response: {e}")
                        response_text = "I'm sorry, there was an error processing your request."
                    
                else:
                    logger.error(f"LLM API error: {llm_response.status_code} - {llm_response.text}")
                    response_text = "Error processing your request. Please try again later."
            
        return {"status": "OK"}
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        return {"status": "Error", "message": "Failed to parse response data"}
    except requests.RequestException as e:
        logger.error(f"HTTP request error: {str(e)}")
        return {"status": "Error", "message": "Failed to communicate with backend service"}
    except Exception as e:
        logger.error(f"Unexpected error in twilio_text_response: {str(e)}", exc_info=True)
        return {"status": "Error", "message": "An unexpected error occurred"}
    
@app.get("/status")
def status_check():
    return {"status": "OK", "UI_STATUS": UI_STATUS}


# @app.post("/twilio-text-response/{caller_sid}")
# async def twilio_text_response(caller_sid: str, request: Request, background_tasks: BackgroundTasks):
#     try:
#         local_caller_sid = caller_sid
#         form_data = await request.form()
#         event_type = form_data.get("TranscriptionEvent")
#         logger.info(f"Received Twilio transcription event: {form_data}")

#         if event_type == "transcription-started":
#             logger.info(f"Transcription started for {caller_sid}")
           

#         elif event_type == "transcription-content":
#             transcription_data = form_data.get("TranscriptionData")
#             transcript = ""

#             if transcription_data:
#                 try:
#                     data_dict = json.loads(transcription_data)
#                     transcript = data_dict.get("transcript", "")
#                     logger.info(f"Transcription content received: {transcript}")
#                 except json.JSONDecodeError:
#                     logger.warning("Could not parse TranscriptionData")

#             is_final = form_data.get("Final") == "true"

#             if is_final:
#                 # Schedule the background LLM callback
#                 logger.info(f"initializing LLM call")
#                 background_tasks.add_task(
#                     handle_llm_callback,
#                     caller_sid,
#                     transcript,
#                     user_record
#                 )

#         return {"status": "OK"}

#     except json.JSONDecodeError as e:
#         logger.error(f"JSON parsing error: {str(e)}")
#         return {"status": "Error", "message": "Failed to parse response data"}

#     except requests.RequestException as e:
#         logger.error(f"HTTP request error: {str(e)}")
#         return {"status": "Error", "message": "Failed to communicate with backend service"}

#     except Exception as e:
#         logger.error(f"Unexpected error in twilio_text_response: {str(e)}", exc_info=True)
#         return {"status": "Error", "message": "An unexpected error occurred"}


# -----------------------------------
# Background Task for LLM Processing
# -----------------------------------
async def handle_llm_callback(caller_sid: str, transcript: str, user_record: Optional[Dict] = None):
    try:
        logger.info(f"Running LLM callback for {caller_sid} with transcript: {transcript}")

        chat_history_format_for_gemini(chat_history, transcript, "user", logger)
        logger.info(f"Chat history after formatting: {chat_history}")
        llm_response = alt_llm_integration(
            chat_history=chat_history,
            genai_key=gemini_api_key,
            logger=logger,
            user=user_record
        )

        if not llm_response:
            payload = json.dumps({
                "response_text": "Sorry! Backend issue. Will call you later.",
                "action": "hangup"
                
            })

            await response_queue.put(payload)
        else:
            response_text = llm_response["candidates"][0]["content"]["parts"][0]["text"]
            chat_history_format_for_gemini(chat_history, response_text, "model", logger)

            

            # if "INFORMATION_INVALID" in response_text:
            #     parts = response_text.split('end', 1)
            #     message_part = parts[0].strip()
            #     json_text = parts[1].strip()
            #     start = json_text.find('{')
            #     end = json_text.rfind('}') + 1
            #     json_data = json.loads(json_text[start:end])

            #     payload = json.dumps({
            #         "response_text": f"{message_part}",
            #         "action": "hangup"
            #     })
            #     headers = {'Content-Type': 'application/json'}

            if "INFORMATION_COLLECTED" in response_text:
                parts = response_text.split('end', 1)
                message_part = parts[0].strip()
                json_text = parts[1].strip()
                start = json_text.find('{')
                end = json_text.rfind('}') + 1
                json_data = json.loads(json_text[start:end])

                payload = json.dumps({
                    "response_text": f"{message_part}",
                    "action": "hangup"
                })
                headers = {'Content-Type': 'application/json'}

                payload = json.dumps({
                            "cust_id": user_record["cust_id"], 
                            "email": json_data.get("email", "")
                            })
                response = requests.post(f"{backend_url}/update-record", headers=headers, data=payload, timeout=10, stream=False)
        
        # Put the payload into the response queue
                await response_queue.put(payload)
            else:
                payload = json.dumps({
                "response_text": response_text,
                "action": "speak"
            })
                await response_queue.put(payload)

        # headers = {'Content-Type': 'application/json'}
        cert_path = os.path.join(os.path.dirname(__file__), "resource", "genaiplatform.ajbpoc.co.uk.crt")
        # requests.post(f"{base_url}/respond/{caller_sid}", headers=headers, data=payload)
        # loop through response_queue and log it
        for response in response_queue._queue:
            logger.info(f"Response in queue: {response}")
        
    except Exception as e:
        logger.error(f"Error in handle_llm_callback: {str(e)}", exc_info=True)

# Background task (sync call in async loop using asyncio.to_thread)
async def response_sender():
    while True:
        payload = await response_queue.get()
        payload = json.loads(payload) 
        # Offload the blocking requests.post to a thread
        if payload.get("action") == "hangup":
            chat_history = []
        
        if env == "production":
            await asyncio.to_thread(requests.post, f"{base_url}/respond/{caller_sid}", data=payload, headers={"Content-Type": "application/json"})
        else:    
            await asyncio.to_thread(requests.post, f"{base_url}/respond/{caller_sid}", data=payload, headers={"Content-Type": "application/json"}, verify=r"C:\Users\sdubey\Documents\GEnAi\ngrok\resource\genaiplatform.ajbpoc.co.uk.crt")

        await asyncio.sleep(2)

import datetime as Datetime
class Record(BaseModel):
    cust_id: int
    name : str
    phnumber: str
    dob : Datetime.datetime
    email: str = None


@app.post("/user-info")
def user_info(record : Record):
    try:
       user_record = record.dict()
       if not user_record:
              return {"status": "error", "message": "No user info provided"}
       return user_record
    except Exception as e:
        logger.error(f"Error processing user info: {str(e)}")
        return {"status": "error", "message": "Failed to process user info"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(response_sender())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")