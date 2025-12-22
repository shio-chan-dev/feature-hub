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
        if isinstance(result, dict):
            request_id = result.get("request_id")
            feature_key = result.get("feature_key")
            experiment_id = result.get("experiment_id")
            variant_key = result.get("variant_key")
        else:
            request_id = result.request_id
            feature_key = result.feature_key
            experiment_id = result.experiment_id
            variant_key = result.variant_key
        logger.info(
                "[router.dec] decide success request_id=%s feature_key=%s experiment_id=%s variant_key=%s",
                request_id,
                feature_key,
                experiment_id,
                variant_key,
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
