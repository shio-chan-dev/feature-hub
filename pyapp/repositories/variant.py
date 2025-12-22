from abc import ABC, abstractmethod
from collections.abc import Sequence
from domain.variant import Variant


class BaseVariantTable(ABC):
    @abstractmethod
    def add(self, variant: Variant) -> Variant:
        ...

    @abstractmethod
    def list_by_experiment(self, experiment_id: str) -> Sequence[Variant]:
        ...

class FakeVariantTable(BaseVariantTable):
    def __init__(self) -> None:
        self._items: dict[str, list[Variant]] = {}
        self._seq = 0

    def add(self, variant: Variant) -> Variant:
        if not variant.id:
            self._seq += 1
            variant.id = f"var-{self._seq:03d}"
        self._items.setdefault(variant.experiment_id, []).append(variant)
        return variant

    def list_by_experiment(self, experiment_id: str) -> Sequence[Variant]:
        return list(self._items.get(experiment_id, []))

var_table: BaseVariantTable = FakeVariantTable()
