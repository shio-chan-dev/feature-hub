from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, status

from utils.logger import logger
from services.decision import dec_svc
from router.schemas.audits import AuditListResponse
from utils.errors import ValidationError

router = APIRouter(tags=["audits"])

@router.get("/audits", response_model=AuditListResponse)
def list_audits(
    feature_id: str,
    cursor: str | None = None,
    limit: int = 50,
    experiment_id: str | None = None,
    variant_id: str | None = None,
    variant_key: str | None = None,
    reason: list[str] | None = Query(None),
    user_id: str | None = None,
    request_id: str | None = None,
    from_ts: datetime | None = Query(None, alias="from"),
    to_ts: datetime | None = Query(None, alias="to"),
    include_payload: bool = True,
):
    logger.info(
        "[router.audit] list_audits start feature_id=%s limit=%s cursor=%s",
        feature_id,
        limit,
        cursor,
    )
    if variant_id and variant_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="variant_id and variant_key are mutually exclusive",
        )
    if from_ts and to_ts and from_ts > to_ts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="from must be earlier than to",
        )
    try:
        result = dec_svc.list_audits(
            feature_id=feature_id,
            limit=limit,
            cursor=cursor,
            experiment_id=experiment_id,
            variant_id=variant_id,
            variant_key=variant_key,
            reasons=reason,
            user_id=user_id,
            request_id=request_id,
            from_ts=from_ts,
            to_ts=to_ts,
            include_payload=include_payload,
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid query {exc}",
        )
    logger.info(
        "[router.audit] list_audits success feature_id=%s count=%s next_cursor=%s",
        feature_id,
        len(result["items"]),
        result["next_cursor"],
    )
    return result
