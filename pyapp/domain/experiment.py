"""
实验管理领域模型
"""
from enum import Enum
from dataclasses import dataclass

# ExperimentStatus 用于定义实验状态
class ExperimentStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"


# Experiment 定义一次实验的全局配置,决定实验是否生效以及参与比例
@dataclass
class Experiment:
    # 实验唯一标识
    id: str
    # 归属的feature,用于把实验挂在某个功能开关下,由feature active_experiment_id 进行指向
    feature_id: str
    # 名称
    name: str
    # 实验运行状态
    status: ExperimentStatus
    # 进行用户分桶
    seed: str
    # 灰度门槛比例
    rollout_percent: int
