import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_FILE = os.path.join(DATA_DIR, "conversations.json")

def normalize_user_id(uid: Optional[str]) -> str:
    """Normalize user id by removing redundant user_ prefixes so IDs consistently match."""
    if not uid:
        return ""
    uid = uid.strip()
    while uid.startswith("user_user_"):
        uid = uid[5:]
    return uid

def _user_matches(stored_uid: Optional[str], query_uid: Optional[str]) -> bool:
    if not stored_uid or not query_uid:
        return False
    if stored_uid == query_uid:
        return True
    return normalize_user_id(stored_uid) == normalize_user_id(query_uid)

def _ensure_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def _read_db() -> Dict[str, Any]:
    _ensure_db()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _write_db(data: Dict[str, Any]):
    _ensure_db()
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def list_conversations(user_id: str) -> List[Dict[str, Any]]:
    """Return all conversations belonging to user_id, newest first."""
    db = _read_db()
    user_convs = []
    norm_id = normalize_user_id(user_id)
    for conv_id, conv in db.items():
        if _user_matches(conv.get("user_id"), norm_id):
            user_convs.append({
                "id": conv_id,
                "title": conv.get("title", "New Conversation"),
                "created_at": conv.get("created_at"),
                "updated_at": conv.get("updated_at"),
                "message_count": len(conv.get("messages", []))
            })
    user_convs.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return user_convs

def get_conversation(user_id: str, conv_id: str) -> Optional[Dict[str, Any]]:
    """Get single conversation if owned by user_id."""
    db = _read_db()
    conv = db.get(conv_id)
    if not conv or not _user_matches(conv.get("user_id"), user_id):
        return None
    return conv

def create_conversation(user_id: str, title: str = "New Conversation") -> Dict[str, Any]:
    """Create a new conversation for user_id."""
    db = _read_db()
    now_str = datetime.now().isoformat()
    norm_id = normalize_user_id(user_id)
    conv_id = f"chat_{int(datetime.now().timestamp())}_{os.urandom(3).hex()}"
    new_conv = {
        "id": conv_id,
        "user_id": norm_id,
        "title": title,
        "created_at": now_str,
        "updated_at": now_str,
        "messages": []
    }
    db[conv_id] = new_conv
    _write_db(db)
    return new_conv

def add_message(user_id: str, conv_id: str, sender: str, text: str, time_str: str, is_crisis: bool = False):
    """Add a message to user's conversation."""
    db = _read_db()
    now_str = datetime.now().isoformat()
    norm_id = normalize_user_id(user_id)
    
    if conv_id not in db:
        db[conv_id] = {
            "id": conv_id,
            "user_id": norm_id,
            "title": text[:35] + ("..." if len(text) > 35 else ""),
            "created_at": now_str,
            "updated_at": now_str,
            "messages": []
        }
    
    conv = db[conv_id]
    # Ensure owner check using normalized match
    if not _user_matches(conv.get("user_id"), norm_id):
        return None

    # Keep user_id in normalized form
    conv["user_id"] = norm_id

    # Auto-generate title from first user message if default
    if conv.get("title") in ["New Conversation", "New Chat"] and sender == "user":
        conv["title"] = text[:38] + ("..." if len(text) > 38 else "")

    conv["updated_at"] = now_str
    if "messages" not in conv:
        conv["messages"] = []
    conv["messages"].append({
        "sender": sender,
        "text": text,
        "time": time_str,
        "is_crisis": is_crisis,
        "timestamp": now_str
    })
    _write_db(db)
    return conv

def delete_conversation(user_id: str, conv_id: str) -> bool:
    """Delete conversation if owned by user."""
    db = _read_db()
    if conv_id in db and _user_matches(db[conv_id].get("user_id"), user_id):
        del db[conv_id]
        _write_db(db)
        return True
    return False
