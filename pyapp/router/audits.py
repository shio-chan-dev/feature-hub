from fastapi import APIRouter
router = APIRouter(tags=["audits"])

@router.get("/audits")
def list_audits(feature_id: str, limit: int = 50, cursor: str | None = None):
    return {"items":[], "next_cursor": None}
