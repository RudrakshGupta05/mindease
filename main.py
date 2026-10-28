import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, HTTPException
from models import ChatRequest
from chat_engine import get_response
from crisis import contains_crisis_keywords,SAFETY_MESSAGE
from logger import log_chat
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app=FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

if os.path.exists("ui"):
    app.mount("/app", StaticFiles(directory="ui", html=True), name="ui")

@app.get("/")
def read_root():
    if os.path.exists("ui/index.html"):
        return RedirectResponse(url="/app/")
    return {"message":"Welcome to MindEase AI"}

@app.get("/health")
def health_check():
    """Health check endpoint for Docker, Cloud Run, and container platforms."""
    return {"status": "ok", "service": "MindEase"}

@app.get("/config")
def get_config():
    pk = os.getenv("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY") or os.getenv("CLERK_PUBLISHABLE_KEY") or ""
    return {
        "clerk_publishable_key": pk
    }

import storage
from datetime import datetime
from models import ChatRequest, CreateConversationRequest

@app.get("/conversations")
def get_user_conversations(user_id: str):
    """Retrieve all conversations for the authenticated user."""
    if not user_id or user_id.startswith("guest"):
        raise HTTPException(status_code=401, detail="Authentication required. Please sign in.")
    return storage.list_conversations(user_id)

@app.get("/conversations/{conv_id}")
def get_conversation_details(conv_id: str, user_id: str):
    """Retrieve messages for a specific conversation."""
    if not user_id or user_id.startswith("guest"):
        raise HTTPException(status_code=401, detail="Authentication required. Please sign in.")
    conv = storage.get_conversation(user_id, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@app.post("/conversations")
def create_new_conversation(request: CreateConversationRequest):
    """Create a new isolated conversation thread for user."""
    if not request.user_id or request.user_id.startswith("guest"):
        raise HTTPException(status_code=401, detail="Authentication required. Please sign in.")
    return storage.create_conversation(request.user_id, request.title or "New Conversation")

@app.delete("/conversations/{conv_id}")
def delete_user_conversation(conv_id: str, user_id: str):
    """Delete a conversation belonging to user."""
    if not user_id or user_id.startswith("guest"):
        raise HTTPException(status_code=401, detail="Authentication required. Please sign in.")
    success = storage.delete_conversation(user_id, conv_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted"}

@app.post("/chat")
async def chat_with_memory(request: ChatRequest):
    if not request.user_id or request.user_id.startswith("guest"):
        raise HTTPException(status_code=401, detail="Authentication required. Please sign in.")
    user_id = request.user_id
    conv_id = request.conversation_id or request.session_id or f"conv_{user_id}"
    user_query = request.query
    time_str = datetime.now().strftime("%I:%M %p")

    # Save user message
    storage.add_message(user_id, conv_id, "user", user_query, time_str)

    if contains_crisis_keywords(user_query):
        log_chat(conv_id, user_query, SAFETY_MESSAGE, is_crisis=True)
        storage.add_message(user_id, conv_id, "ai", SAFETY_MESSAGE, time_str, is_crisis=True)
        return {"response": SAFETY_MESSAGE, "conversation_id": conv_id}

    response = get_response(conv_id, user_query)
    log_chat(conv_id, user_query, response, is_crisis=False)
    storage.add_message(user_id, conv_id, "ai", response, time_str, is_crisis=False)
    return {"response": response, "conversation_id": conv_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)