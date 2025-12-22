from abc import ABC, abstractmethod
from typing import Sequence

from domain.experiment import Experiment
from utils.errors import NotFoundError


class BaseExperimentTable(ABC):
    @abstractmethod
    def create(self, experiment: Experiment) -> Experiment:
        ...

    @abstractmethod
    def list_by_feature(self, feature_id: str) -> Sequence[Experiment]:
        ...

    @abstractmethod
    def get(self, experiment_id: str) -> Experiment:
        ...

    @abstractmethod
    def update(self, experiment: Experiment) -> Experiment:
        ...

class FakeExperimentTable(BaseExperimentTable):
    def __init__(self) -> None:
        self._items: dict[str, Experiment] = {}
        self._seq = 0

    def create(self, experiment: Experiment) -> Experiment:
        if not experiment.id:
            self._seq += 1
            experiment.id = f"exp-{self._seq:03d}"
        self._items[experiment.id] = experiment
        return experiment

    def list_by_feature(self, feature_id: str) -> Sequence[Experiment]:
        return [e for e in self._items.values() if e.feature_id == feature_id]

    def get(self, experiment_id: str) -> Experiment:
        try:
            return self._items[experiment_id]
        except:
            raise NotFoundError("experiment_not_found")

    def update(self, experiment: Experiment) -> Experiment:
        self._items[experiment.id] = experiment
        return experiment


experiment_table: BaseExperimentTable = FakeExperimentTable()
