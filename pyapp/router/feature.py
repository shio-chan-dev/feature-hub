from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_404_NOT_FOUND

from domain.feature import Feature
from router.schemas.feature import FeatureCreate, FeatureOut, FeaturePatch
from services.feature import feat_svc


router = APIRouter(tags=["features"])

@router.post("/features", response_model=FeatureOut)
def create_feature(payload: FeatureCreate):
    try:
        feat = feat_svc.create(payload.key, payload.name)
        return _out(feat)
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"feature creating failure err={e}"
                )

@router.get("/features", response_model=list[FeatureOut])
def list_features():
    return [_out(f) for f in feat_svc.list()]

@router.get("/features/{feature_id}", response_model=FeatureOut)
def get_feature(feature_id: str):
    try:
        return _out(feat_svc.get(feature_id))
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"not found err={str(e)}"
                )

@router.patch("/features/{feture_id}", response_model=FeatureOut)
def patch_feature(feature_id: str, payload: FeaturePatch):
    try:
        updated = feat_svc.update(
                feature_id,
                payload.status,
                payload.active_experiment_id,
                )
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"更新功能记录失败 {str(e)}",
                )
    

def _out(feat: Feature) -> FeatureOut:
    return FeatureOut(
            id=feat.id,
            key=feat.key,
            name=feat.name,
            status=feat.status.value,
            active_experiment_id=feat.active_experiment_id,
            )
