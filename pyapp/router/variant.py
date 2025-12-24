from fastapi import APIRouter, HTTPException, status

from domain.variant import Variant
from router.schemas.variant import VariantCreate, VariantOut, VariantPatch
from services.variant import var_svc
from utils.logger import logger

router = APIRouter(tags=["variants"])

@router.post("/experiments/{experiment_id}/variants", response_model=VariantOut)
def create_variant(experiment_id: str, payload: VariantCreate):
    try:
        payload_keys = list(payload.payload.keys())
        logger.info(
                "[router.var] create_variant start experiment_id=%s key=%s weight=%s is_control=%s payload_keys=%s",
                experiment_id,
                payload.key,
                payload.weight,
                payload.is_control,
                payload_keys,
                )
        var = var_svc.add(experiment_id, payload.key, payload.weight, payload.is_control, dict(payload.payload))
        logger.info(
                "[router.var] create_variant success id=%s experiment_id=%s key=%s",
                var.id,
                var.experiment_id,
                var.key,
                )
        return _out(var)
    except Exception as e:
        logger.info(
                "[router.var] create_variant error experiment_id=%s err=%s",
                experiment_id,
                e,
                )
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"创建变量失败 {str(e)}"
                )


@router.get("/experiments/{experiment_id}/variants", response_model=list[VariantOut])
def list_variants(experiment_id: str):
    logger.info("[router.var] list_variants start experiment_id=%s", experiment_id)
    variants = list(var_svc.list_by_experiment(experiment_id))
    logger.info(
            "[router.var] list_variants success experiment_id=%s count=%s",
            experiment_id,
            len(variants),
            )
    return [_out(v) for v in variants]

@router.patch("/variants/{variant_id}", response_model=VariantOut)
def patch_variant(variant_id: str, payload: VariantPatch):
    try:
        logger.info(
                "[router.var] patch variant start id=%s weight=%s is_control=%s payload=%s",
                variant_id,
                payload.weight,
                payload.is_control,
                payload.payload,
                )
        updated = var_svc.update(
                variant_id=variant_id,
                weight=payload.weight,
                is_control=payload.is_control,
                payload=payload.payload,
                )
        logger.info(
                "[router.var] patch variant success id=%s key=%s payload=%s",
                updated.id,
                updated.key,
                updated.payload
                )
        return VariantOut(
                id=updated.id,
                experiment_id=updated.experiment_id,
                key=updated.key,
                weight=updated.weight,
                is_control=updated.is_control,
                payload=updated.payload
                )
    except Exception as e:
        logger.info("[router.var] patch variant error id=%s err=%s", variant_id, e)
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"update variant failed err={e}",
                )

def _out(var: Variant) -> VariantOut:
    return VariantOut(
            id=var.id,
            experiment_id=var.experiment_id,
            key=var.key,
            weight=var.weight,
            is_control=var.is_control,
            payload=var.payload,
            )
