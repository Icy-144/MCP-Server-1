# server/auth_utils.py
import os
import hmac
import hashlib
import time
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["MCP_SECRET_KEY"]


def generate_token(client_id: str) -> str:
    timestamp = str(int(time.time()))
    payload   = f"{client_id}:{timestamp}"
    sig       = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def verify_token(token: str) -> str | None:
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        client_id, timestamp, sig = parts
        if int(time.time()) - int(timestamp) > 2_592_000:
            return None
        expected = hmac.new(
            SECRET_KEY.encode(),
            f"{client_id}:{timestamp}".encode(),
            hashlib.sha256,
        ).hexdigest()
        if hmac.compare_digest(sig, expected):
            return client_id
        return None
    except Exception:
        return None