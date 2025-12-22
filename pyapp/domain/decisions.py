from enum import Enum
from datetime import datetime
from dataclasses import dataclass


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
