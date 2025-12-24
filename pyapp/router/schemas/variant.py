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

class VariantPatch(BaseModel):
    weight: int | None = None
    is_control: bool | None = None
    payload: Mapping[str, Any] | None = None
