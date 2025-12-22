from domain.variant import Variant
from repositories.variant import var_table
from utils.errors import ValidationError


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


var_svc: VariantService = VariantService()
