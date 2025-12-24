from enum import Enum
from datetime import datetime
from dataclasses import dataclass

from domain import experiment


# DecisionReason define an experimental status
class DecisionReason(str, Enum):
    EXPERIMENT_INAVTIVE = "experiment_inactivate"
    ASSIGNED = "assigned"

# Decision is the criteria for defining how an experiment is allocated
@dataclass
class Decision:
    id: str
    request_id: str
    experiment_id: str
    user_id: str
    variant_id: str
    reason: DecisionReason
    decided_at: datetime


@dataclass
class DecisionAudit:
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
