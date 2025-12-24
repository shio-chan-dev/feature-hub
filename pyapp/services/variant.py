from domain.variant import Variant
from repositories.variant import var_table
from utils.errors import NotFoundError, ValidationError


class VariantService:
    def __init__(self) -> None:
        self._table = var_table

    def add(self, experiment_id: str, key: str, weight: int, is_control: bool, payload: dict) -> Variant:
        if weight < 0:
            raise ValidationError("weight range error")
        var = Variant(
                id=None,
                experiment_id=experiment_id,
                key=key,
                weight=weight,
                is_control=is_control,
                payload=payload,
                )
        return self._table.add(var)

    def list_by_experiment(self, experiment_id: str) -> list[Variant]:
        return list(self._table.list_by_experiment(experiment_id))

    def update(self, variant_id: str, weight: int | None, is_control: bool | None, payload: dict | None) -> Variant:
        # 业务校验
        if weight is not None and weight < 0:
            raise ValidationError("weight range error")

        var = self._table.get(variant_id)

        if not var:
            raise NotFoundError("variant not found")

        if weight is not None:
            var.weight = weight
        if is_control is not None:
            var.is_control = is_control
        if payload is not None:
            var.payload = payload

        return self._table.update(var)

var_svc: VariantService = VariantService()
