import os
from typing import Dict, List
from dotenv import load_dotenv
# pyrefly: ignore[missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore[missing-import]
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment")

llm = ChatGroq(api_key=GROQ_API_KEY, temperature=0.7, model_name="openai/gpt-oss-120b")

SYSTEM_PROMPT = (
    "You are MindEase, a warm, compassionate, and supportive AI mental health assistant. "
    "Listen actively, offer calm and comforting advice, and encourage mindfulness and self-care."
)

# Store per-user message history: session_id -> List[BaseMessage]
session_memory_map: Dict[str, List[BaseMessage]] = {}

def get_response(session_id: str, user_query: str) -> str:
    if session_id not in session_memory_map:
        session_memory_map[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]

    history = session_memory_map[session_id]
    history.append(HumanMessage(content=user_query))

    response = llm.invoke(history)
    reply_text = str(response.content)

    history.append(AIMessage(content=reply_text))
    return reply_text