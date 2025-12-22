from pydantic import BaseModel
from typing import Any, Mapping

class DecisionRequest(BaseModel):
    request_id: str
    feature_key: str
    user_id: str
    context: Mapping[str, Any] | None = None


class DecisionResponse(BaseModel):
    request_id: str
    feature_key: str
    experiment_id: str | None
    variant_key: str
    variant_payload: Mapping[str, Any]
    reason: str
