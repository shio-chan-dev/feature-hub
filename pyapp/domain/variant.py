from typing import Mapping
from dataclasses import dataclass

# JsonValue and Payload define a type alias
JsonValue = str | int | bool
Payload = Mapping[str, JsonValue]

# Variant Define the specific plan and parameters to switch to for this experiment
@dataclass
class Variant:
    id: str
    experiment_id: str
    key: str
    weight: int
    is_control: bool
    payload: Payload
