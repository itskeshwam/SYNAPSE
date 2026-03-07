import json
import os
from pathlib import Path
from datetime import datetime

POST_OFFICE_PATH = Path(__file__).resolve().parent / "post_office.json"

def _ensure_file():
    if not POST_OFFICE_PATH.exists():
        POST_OFFICE_PATH.write_text("[]")

def send_message(message: dict):
    _ensure_file()
    messages = json.loads(POST_OFFICE_PATH.read_text())
    message["timestamp"] = datetime.utcnow().isoformat() + "Z"
    messages.append(message)
    POST_OFFICE_PATH.write_text(json.dumps(messages, indent=2))

def read_messages():
    _ensure_file()
    return json.loads(POST_OFFICE_PATH.read_text())

def clear_messages():
    _ensure_file()
    POST_OFFICE_PATH.write_text("[]")
