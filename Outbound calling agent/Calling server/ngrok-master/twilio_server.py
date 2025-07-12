from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv
import asyncio
import logging
import os

load_dotenv()  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
SERVER_URL = os.getenv("SERVER_URL")
TRANSCRIPTION_CALLBACK_URL = os.getenv("TRANSCRIPTION_CALLBACK_URL")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Placeholders for your services
async def transcribe_with_vosk(audio_data: bytes) -> str:
    """Your Vosk implementation"""
    return "Customer said: Hello, how are you today?"

async def get_llm_response(text: str) -> str:
    """Your LLM implementation"""
    return f"Thank you for saying: {text}. How can I help you further?"

# Store active calls
active_calls = {}

class CallSession:
    def __init__(self, call_sid: str, customer_phone: str):
        self.call_sid = call_sid
        self.customer_phone = customer_phone
        self.audio_buffer = []
        self.is_recording = False
        self.last_speech_time = None
        self.conversation_turn = 1

class CallRequest(BaseModel):
    customer_phone: str

class AgentResponse(BaseModel):
    response_text: str
    action: str = "speak"  # speak, hangup,

@app.get("/")
async def root():
    return {"message": "Hello from BELLa!"}
   
# === INITIATE OUTBOUND CALL ===
@app.post("/initiate-call")
async def initiate_outbound_call(request: CallRequest):
    """Start an outbound call"""
    # data = await request.json()
    customer_phone = request.customer_phone
    
    if not customer_phone:
        return {"error": "customer_phone is required"}
    
    try:
        call = client.calls.create(
            url=f"{SERVER_URL}/start-conversation",
            to=customer_phone,
            from_=TWILIO_PHONE_NUMBER,
            method='POST'
        )
        
        logger.info(f"Outbound call initiated: {call.sid} to {customer_phone}")
        return {"call_sid": call.sid, "status": "call_initiated"}
        
    except Exception as e:
        logger.error(f"Error initiating call: {e}")
        return {"error": str(e)}

# === CONVERSATION FLOW ===
@app.post("/start-conversation")
async def start_conversation(request: Request):
    """Initial TwiML when call connects"""
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        to_number = form_data.get("To")
        from_number = form_data.get("From")

        logger.info(f"=== CALL CONNECTED ===")
  
        active_calls[call_sid] = CallSession(call_sid, to_number)


        # Start with greeting and first turn
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Hello, Bella here from A J Bell. I am calling as we 
    need to ensure your details are up-to-date on our system. How are you today?</Say>
    <Start>
        <Transcription 
            name="test_transcription"
            statusCallbackUrl="{TRANSCRIPTION_CALLBACK_URL}/{call_sid}"
            track="inbound_track"
            partialResults="true"
            languageCode="en-GB" />
    </Start>
    <Pause length="600"/>
</Response>"""
        
        return PlainTextResponse(twiml, media_type="application/xml")

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return PlainTextResponse("<Response><Say>Sorry. An error occurred</Say></Response>", media_type="application/xml")

# === AGENT RESPONSE ENDPOINT ===
@app.post("/respond/{call_sid}")
async def handle_agent_response(call_sid: str, response: AgentResponse):
    """Receive agent response and make Twilio speak to customer"""
    try:
        if call_sid not in active_calls:
            logger.error(f"Call {call_sid} not found in active calls")
            return {"error": "Call not found"}
        
        session = active_calls[call_sid]
        response_text = response.response_text
        action = response.action
        
     
        
        if action == "speak":
            # Update call with agent response and continue listening
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <Response>
                        <Say voice="Polly.Joanna">{response_text}</Say>
                        <Pause length="600"/>
                    </Response>"""
            
        elif action == "hangup":
            # Say goodbye and hang up
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <Response>
                        <Say voice="Polly.Joanna">{response_text}</Say>
                        <Hangup/>
                    </Response>"""
        
        else:
            # Default to speak
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <Response>
                        <Say voice="Polly.Joanna">{response_text}</Say>
                        <Pause length="600"/>
                    </Response>"""
        
        # Update the call with new TwiML
        call = client.calls(call_sid).update(twiml=twiml)
        
    
        
        # Clean up session if hanging up
        if action == "hangup":
            if call_sid in active_calls:
                del active_calls[call_sid]
       
        
        return {"status": "success", "action": action}
        
    except Exception as e:
        logger.error(f"Error handling agent response: {e}")
        return {"error": str(e)}

# === AGENT HOLD ENDPOINT ===
@app.post("/hold/{call_sid}")
async def play_hold_music(call_sid: str):
    """Tell Twilio to play hold music for the given call"""
    try:
        hold_url = f"{SERVER_URL}/static/hold-music.mp3"

        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{hold_url}</Play>
    <Pause length="600"/>
</Response>"""

        client.calls(call_sid).update(twiml=twiml)
        logger.info(f"Playing hold music for {call_sid}")
        return {"status": "playing_hold_music"}
    except Exception as e:
        logger.error(f"Error playing hold music: {e}")
        return {"error": str(e)}

# === UTILITY ENDPOINTS ===
@app.post("/call-status")
async def call_status_callback(request: Request):
    """Handle call status updates from Twilio"""
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus")
    
    
    if call_status in ["completed", "failed", "busy", "no-answer"]:
        if call_sid in active_calls:
            del active_calls[call_sid]
    
    return PlainTextResponse("OK")

@app.get("/active-calls")
async def get_active_calls():
    return {
        "active_calls": len(active_calls),
        "calls": list(active_calls.keys())
    }

@app.post("/end-call/{call_sid}")
async def end_call(call_sid: str):
    try:
        client.calls(call_sid).update(status='completed')
        if call_sid in active_calls:
            del active_calls[call_sid]
        return {"status": "call_ended"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)