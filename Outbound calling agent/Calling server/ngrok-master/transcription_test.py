from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Start, Transcription
import websockets
import json
import logging
from typing import Dict
from dataclasses import dataclass, field
from datetime import datetime
from twilio.rest import Client
import os
from pydantic import BaseModel
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    # handlers=[
    #     logging.FileHandler('transcription_test.log'),
    #     logging.StreamHandler()
    # ]
)


logger = logging.getLogger(__name__)

app = FastAPI()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
SERVER_URL = os.getenv("SERVER_URL")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")
# Construct WebSocket URL
websocket_url = SERVER_URL.replace('https://', 'wss://').replace('http://', 'ws://')


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@dataclass
class CallSession:
    call_sid: str
    customer_phone: str
    transcriptions: list = field(default_factory=list)

# Active sessions
active_calls: Dict[str, CallSession] = {}

class CallRequest(BaseModel):
    customer_phone: str

@app.post("/initiate-call")
async def initiate_outbound_call(request: CallRequest):
    """Start an outbound call for transcription testing"""
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
        
        logger.info(f"Call initiated: {call.sid} to {customer_phone}")
        return {"call_sid": call.sid, "status": "call_initiated"}
        
    except Exception as e:
        logger.error(f"Error initiating call: {e}")
        return {"error": str(e)}

@app.post("/start-conversation")
async def start_conversation(request: Request):
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        to_number = form_data.get("To")
        from_number = form_data.get("From")
        
        logger.info(f"=== CALL CONNECTED ===")
        logger.info(f"Call SID: {call_sid}")
        logger.info(f"From: {from_number}, To: {to_number}")
        
        active_calls[call_sid] = CallSession(call_sid, from_number)
        
        # Build WebSocket URL consistently with your working test
        callback_url = f"{SERVER_URL}/transcription-callback/{call_sid}"
        
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">Hello, this is a transcription test. Please start speaking.</Say>
    <Start>
        <Transcription 
            name="test_transcription"
            statusCallbackUrl="{callback_url}"
            track="both_tracks"
            inboundTrackLabel="agent"
            outboundTrackLabel="customer"
            partialResults="true"
            languageCode="en-GB" />
    </Start>
    <Pause length="60"/>
    <Say voice="alice">Test complete.</Say>
    <Hangup/>
</Response>"""

        logger.info(f"=== TWIML GENERATED ===")
        logger.info(f"TwiML: {twiml}")
        
        return PlainTextResponse(twiml, media_type="application/xml")

    except Exception as e:
        logger.error(f"Error starting conversation: {e}")
        return PlainTextResponse(
            "<Response><Say>Error occurred</Say><Hangup/></Response>", 
            media_type="application/xml"
        )

@app.get("/test-websocket/{call_sid}")
async def test_websocket_connection(call_sid: str):
    """Test the WebSocket transcription endpoint"""
    
    # Construct WebSocket URL
    websocket_url = SERVER_URL.replace('https://', 'wss://').replace('http://', 'ws://')
    full_ws_url = f"{websocket_url}/transcription-stream/{call_sid}"
    
    logger.info(f"Testing WebSocket connection to: {full_ws_url}")
    
    try:
        # Test connection
        async with websockets.connect(full_ws_url) as websocket:
            logger.info("WebSocket connection successful!")
            
            test_message = {
                "event": "transcription",
                "transcription": {
                    "transcript": "This is a test message",
                    "final": True,
                    "confidence": 0.95
                }
            }
            
            await websocket.send(json.dumps(test_message))
            logger.info("Test message sent successfully!")
            
            await asyncio.sleep(1)
            
            return {
                "status": "success",
                "message": "WebSocket connection and message sending successful",
                "websocket_url": full_ws_url
            }
            
    except Exception as e:
        logger.error(f"WebSocket test failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "websocket_url": full_ws_url
        }
@app.post("/transcription-callback/{call_sid}")
async def transcription_callback(call_sid: str, request: Request):
    """Handle transcription callbacks from Twilio"""
    try:
        # Parse form data from Twilio
        form_data = await request.form()
        
        event_type = form_data.get("Event")
        logger.info(f"=== TRANSCRIPTION EVENT ===")
        logger.info(f"Call SID: {call_sid}")
        logger.info(f"Event: {event_type}")
        
        if event_type == "transcription-started":
            logger.info(f"Transcription started for {call_sid}")
            
        elif event_type == "transcription-content":
            transcript = form_data.get("TranscriptionText", "")
            is_final = form_data.get("Final") == "true"
            confidence = float(form_data.get("Confidence", 0.0))
            
            if transcript.strip():
                status = "FINAL" if is_final else "PARTIAL"
                logger.info(f"[{call_sid}] {status} ({confidence:.2f}): {transcript}")
                
        elif event_type == "transcription-stopped":
            logger.info(f"Transcription stopped for {call_sid}")
            
        elif event_type == "transcription-error":
            error_msg = form_data.get("ErrorMessage", "Unknown error")
            logger.error(f"Transcription error for {call_sid}: {error_msg}")
        
        # Log all form data for debugging
        logger.info(f"All form data: {dict(form_data)}")
        
        return PlainTextResponse("OK")
        
    except Exception as e:
        logger.error(f"Error handling transcription callback: {e}")
        return PlainTextResponse("Error", status_code=500)

@app.post("/call-status")
async def call_status_callback(request: Request):
    """Handle call status updates"""
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus")
    
    logger.info(f"Call {call_sid} status: {call_status}")
    
    if call_status in ["completed", "failed", "busy", "no-answer"]:
        if call_sid in active_calls:
            del active_calls[call_sid]
    
    return PlainTextResponse("OK")

@app.get("/transcriptions/{call_sid}")
async def get_transcriptions(call_sid: str):
    """Get transcriptions for a call"""
    if call_sid not in active_calls:
        return {"error": "Call not found"}
    
    session = active_calls[call_sid]
    return {
        "call_sid": call_sid,
        "transcriptions": session.transcriptions
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)