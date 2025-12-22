from abc import ABC, abstractmethod
from typing import Sequence

from domain.feature import Feature
from repositories.decisions import FakeDecisionTable
from utils.errors import NotFoundError


class BaseFeatureTable(ABC):
    @abstractmethod
    def create(self, feature: Feature) -> Feature:
        ...

    @abstractmethod
    def list(self) -> Sequence[Feature]:
        ...

    @abstractmethod
    def get(self, feature_id: str) -> Feature:
        ...

    @abstractmethod
    def get_by_key(self, key: str) -> Feature:
        ...

    @abstractmethod
    def update(self, feature: Feature) -> Feature:
        ...
    

class FakeFeatureTable(BaseFeatureTable):
    def __init__(self) -> None:
        self._items: dict[str, Feature] = {}
        self._seq = 0

    def create(self, feature: Feature) -> Feature:
        if not feature.id:
            self._seq += 1
            feature.id = f"feat-{self._seq:03d}"
        self._items[feature.id] = feature
        return feature

    def list(self) -> Sequence[Feature]:
        return list(self._items.values())

    def get(self, feature_id: str) -> Feature:
        try:
            return self._items[feature_id]
        except KeyError:
            raise NotFoundError("feature not found")

    def get_by_key(self, key: str) -> Feature:
        for f in self._items.values():
            if f.key == key:
                return f
        raise NotFoundError("feature not found")

    def update(self, feature: Feature) -> Feature:
        self._items[feature.id] = feature
        return feature

feature_table: BaseFeatureTable = FakeFeatureTable()
