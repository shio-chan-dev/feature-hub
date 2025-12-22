from pydantic import BaseModel

class ExperimentCreate(BaseModel):
    name: str
    seed: str
    rollout_percent: int


class ExperimentPatch(BaseModel):
    status: str | None = None
    rollout_percent: int | None = None
    seed: str | None = None


class ExperimentOut(BaseModel):
    id: str
    feature_id: str
    name: str
    seed: str
    status: str
    rollout_percent: int
