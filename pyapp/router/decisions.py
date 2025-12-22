from fastapi import APIRouter, HTTPException, status

from router.schemas.decisions import DecisionRequest, DecisionResponse
from services.decision import dec_svc
from utils.logger import logger



router = APIRouter(tags=["decisions"])

@router.post("/decisions", response_model=DecisionResponse)
def decide(payload: DecisionRequest):
    try:
        context = dict(payload.context or {})
        logger.info(
                "[router.dec] decide start request_id=%s feature_key=%s user_id=%s context_keys=%s",
                payload.request_id,
                payload.feature_key,
                payload.user_id,
                list(context.keys()),
                )
        result = dec_svc.decide(
                payload.request_id,
                payload.feature_key,
                payload.user_id,
                context,
                )
        logger.info(
                "[router.dec] decide success request_id=%s feature_key=%s experiment_id=%s variant_key=%s",
                result.request_id,
                result.feature_key,
                result.experiment_id,
                result.variant_key,
                )
        return result
    except Exception as e:
        logger.info(
                "[router.dec] decide error request_id=%s feature_key=%s err=%s",
                payload.request_id,
                payload.feature_key,
                e,
                )
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"觉得用户使用方案失败 {str(e)}"
                )
