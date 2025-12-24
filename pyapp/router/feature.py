from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_404_NOT_FOUND

from domain.feature import Feature
from router.schemas.feature import FeatureCreate, FeatureOut, FeaturePatch
from services.feature import feat_svc
from utils.logger import logger


router = APIRouter(tags=["features"])

@router.post("/features", response_model=FeatureOut)
def create_feature(payload: FeatureCreate):
    try:
        logger.info(
                "[router.feat] create_feature start key=%s name=%s",
                payload.key,
                payload.name,
                )
        feat = feat_svc.create(payload.key, payload.name)
        logger.info(
                "[router.feat] create_feature success id=%s key=%s",
                feat.id,
                feat.key,
                )
        return _out(feat)
    except Exception as e:
        logger.info(
                "[router.feat] create_feature error key=%s name=%s err=%s",
                payload.key,
                payload.name,
                e,
                )
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"feature creating failure err={e}"
                )

@router.get("/features", response_model=list[FeatureOut])
def list_features():
    logger.info("[router.feat] list_features start")
    features = feat_svc.list()
    logger.info("[router.feat] list_features success count=%s", len(features))
    return [_out(f) for f in features]

@router.get("/features/{feature_id}", response_model=FeatureOut)
def get_feature(feature_id: str):
    try:
        logger.info("[router.feat] get_feature start id=%s", feature_id)
        feat = feat_svc.get(feature_id)
        logger.info("[router.feat] get_feature success id=%s", feature_id)
        return _out(feat)
    except Exception as e:
        logger.info(
                "[router.feat] get_feature error id=%s err=%s",
                feature_id,
                e,
                )
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"not found err={str(e)}"
                )

@router.patch("/features/{feature_id}", response_model=FeatureOut)
def patch_feature(feature_id: str, payload: FeaturePatch):
    try:
        logger.info(
                "[router.feat] patch_feature start id=%s name=%s status=%s active_experiment_id=%s",
                feature_id,
                payload.name,
                payload.status,
                payload.active_experiment_id,
                )
        updated = feat_svc.update(
                feature_id,
                payload.status,
                payload.active_experiment_id,
                payload.name,
                )
        logger.info(
                "[router.feat] patch_feature success id=%s status=%s",
                updated.id,
                updated.status.value,
                )
        return _out(updated)
    except Exception as e:
        logger.info(
                "[router.feat] patch_feature error id=%s err=%s",
                feature_id,
                e,
                )
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
