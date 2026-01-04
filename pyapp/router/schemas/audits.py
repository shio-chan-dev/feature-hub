from datetime import datetime
from pydantic import BaseModel


class AuditItem(BaseModel):
    id: str
    decided_at: datetime
    request_id: str
    user_id: str
    feature_id: str
    feature_key: str
    feature_name: str | None
    experiment_id: str | None
    experiment_name: str | None
    variant_id: str | None
    variant_key: str
    is_control: bool | None
    reason: str
    variant_payload: dict | None

class AuditListResponse(BaseModel):
    items: list[AuditItem]
    next_cursor: str | None
