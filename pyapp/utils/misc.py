import base64
import json
from uuid import uuid4

def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"

def encode_cursor(offset: int) -> str:
    payload = json.dumps({"offset": offset}, separators=(",", ":"))
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("ascii")

def decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    if cursor.isdigit():
        return int(cursor)
    padded = cursor + "=" * (-len(cursor) % 4)
    raw = base64.urlsafe_b64decode(padded.encode("ascii"))
    data = json.loads(raw.decode("utf-8"))
    return int(data.get("offset", 0))
