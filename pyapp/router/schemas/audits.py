from datetime import datetime
from pydantic import BaseModel


class AuditItem(BaseModel):
    id: str
    request_id: str
    feature_id: str
    feature_key: str
    experiment_id: str | None
    user_id: str
    variant_key: str
    variant_payload: dict
    reason: str
    decided_at: datetime

class AuditListResponse(BaseModel):
    items:list[AuditItem]
    next_cursor: str | None
