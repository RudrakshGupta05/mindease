import os
from typing import Dict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

load_dotenv()

SYSTEM_PROMPT = (
    "You are MindEase, a warm, compassionate, and supportive AI mental health companion. "
    "Listen actively, offer calm and comforting advice, and encourage mindfulness and self-care."
)

# Store per-user message history: session_id -> List[BaseMessage]
session_memory_map: Dict[str, List[BaseMessage]] = {}
_llm = None

def get_llm():
    global _llm
    if _llm is None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY not found in environment. Please add it to your environment variables.")
        model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        _llm = ChatGroq(api_key=key, temperature=0.7, model_name=model)
    return _llm

def get_response(session_id: str, user_query: str) -> str:
    if session_id not in session_memory_map:
        session_memory_map[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]

    history = session_memory_map[session_id]
    history.append(HumanMessage(content=user_query))

    llm = get_llm()
    response = llm.invoke(history)
    reply_text = str(response.content)

    history.append(AIMessage(content=reply_text))
    return reply_text