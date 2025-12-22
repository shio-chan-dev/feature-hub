from fastapi import APIRouter, HTTPException, status

from domain.variant import Variant
from router.schemas.variant import VariantCreate, VariantOut
from services.variant import var_svc

router = APIRouter(tags=["variants"])

@router.post("/experiments/{experiment_id}/variants", response_model=VariantOut)
def create_variant(experiment_id: str, payload: VariantCreate):
    try:
        var = var_svc.add(experiment_id, payload.key, payload.weight, payload.is_control, dict(payload.payload))
        return _out(var)
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"创建变量失败 {str(e)}"
                )


@router.get("/experiments/{experiment_id}/variants", response_model=list[VariantOut])
def list_variants(experiment_id: str):
    return [_out(v) for v in var_svc.list_by_experiment(experiment_id)]

def _out(var: Variant) -> VariantOut:
    return VariantOut(
            id=var.id,
            experiment_id=var.experiment_id,
            key=var.key,
            weight=var.weight,
            is_control=var.is_control,
            payload=var.payload,
            )
