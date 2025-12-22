"""
业务开关容器领域模型
"""
from dataclasses import dataclass
from enum import Enum


class FeatureStatus(str, Enum):
    OFF = "off"
    ON = "on"
    EXPERIMENT = "experiment"

@dataclass
class Feature:
    id: str
    key: str
    name: str
    status: FeatureStatus
    active_experiment_id: str | None
