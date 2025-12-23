from pydantic import BaseModel


# FeatureCreate construct a feature query request body
class FeatureCreate(BaseModel):
    key: str
    name: str

# FeatureOut define the output of the feature respoonse
class FeatureOut(BaseModel):
    id: str
    key: str
    name: str
    status: str
    active_experiment_id: str | None

class FeaturePatch(BaseModel):
    name: str | None = None
    status: str | None = None
    active_experiment_id: str | None = None
