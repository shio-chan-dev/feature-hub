from pydantic import BaseModel
from typing import Any, Mapping

class VariantCreate(BaseModel):
    key: str
    weight: int
    is_control: bool
    payload: Mapping[str, Any]


class VariantOut(BaseModel):
    id: str
    experiment_id: str
    key: str
    weight: int
    is_control: bool
    payload: Mapping[str, Any]
