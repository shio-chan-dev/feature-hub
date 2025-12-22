from fastapi import APIRouter, HTTPException, status

from router.schemas.decisions import DecisionRequest, DecisionResponse
from services.decision import dec_svc



router = APIRouter(tags=["decisions"])

@router.post("/decisions", response_model=DecisionResponse)
def decide(payload: DecisionRequest):
    try:
        return dec_svc.decide(
                payload.request_id,
                payload.feature_key,
                payload.user_id,
                dict(payload.context or {}),
                )
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"觉得用户使用方案失败 {str(e)}"
                )
