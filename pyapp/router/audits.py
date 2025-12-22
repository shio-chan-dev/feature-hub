from fastapi import APIRouter
from utils.logger import logger
router = APIRouter(tags=["audits"])

@router.get("/audits")
def list_audits(feature_id: str, limit: int = 50, cursor: str | None = None):
    logger.info(
            "[router.audit] list_audits start feature_id=%s limit=%s cursor=%s",
            feature_id,
            limit,
            cursor,
            )
    result = {"items": [], "next_cursor": None}
    logger.info(
            "[router.audit] list_audits success feature_id=%s count=%s next_cursor=%s",
            feature_id,
            len(result["items"]),
            result["next_cursor"],
            )
    return result
