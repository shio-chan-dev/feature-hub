from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select

from domain.experiment import Experiment, ExperimentStatus
from repositories.db.models import ExperimentORM
from repositories.db.init import get_db
from utils.errors import NotFoundError
from utils.logger import logger
from utils.misc import new_id


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

class ExperimentTable(BaseExperimentTable):
    def create(self, experiment: Experiment) -> Experiment:
        logger.info(
            "[repo.exp] create start feature_id=%s name=%s",
            experiment.feature_id,
            experiment.name,
        )
        experiment_id = experiment.id or new_id("exp")
        logger.debug("[repo.exp] create prepared id=%s", experiment_id)
        try:
            with get_db() as db:
                orm = ExperimentORM(
                        id=experiment_id,
                        feature_id=experiment.feature_id,
                        name=experiment.name,
                        status=experiment.status.value,
                        seed=experiment.seed,
                        rollout_percent=experiment.rollout_percent,
                        )
                logger.debug("[repo.exp] create persist id=%s", experiment_id)
                db.add(orm)
                db.commit()
                db.refresh(orm)
                logger.info(
                    "[repo.exp] create success id=%s feature_id=%s",
                    orm.id,
                    orm.feature_id,
                )
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.exp] create error id=%s feature_id=%s err=%s",
                experiment_id,
                experiment.feature_id,
                exc,
                exc_info=True,
            )
            raise

    def list_by_feature(self, feature_id: str) -> Sequence[Experiment]:
        logger.info("[repo.exp] list_by_feature start feature_id=%s", feature_id)
        try:
            with get_db() as db:
                logger.debug("[repo.exp] list_by_feature query feature_id=%s", feature_id)
                items = db.scalars(
                        select(ExperimentORM).where(ExperimentORM.feature_id == feature_id)
                        ).all()
                logger.info(
                    "[repo.exp] list_by_feature success feature_id=%s count=%s",
                    feature_id,
                    len(items),
                )
                return [_to_domain(i) for i in items]
        except Exception as exc:
            logger.error(
                "[repo.exp] list_by_feature error feature_id=%s err=%s",
                feature_id,
                exc,
                exc_info=True,
            )
            raise

    def get(self, experiment_id: str) -> Experiment:
        logger.info("[repo.exp] get start id=%s", experiment_id)
        try:
            with get_db() as db:
                logger.debug("[repo.exp] get query id=%s", experiment_id)
                orm = db.get(ExperimentORM, experiment_id)
                if not orm:
                    raise NotFoundError("experiment not found")
                logger.info("[repo.exp] get success id=%s", experiment_id)
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.exp] get error id=%s err=%s",
                experiment_id,
                exc,
                exc_info=True,
            )
            raise


    def update(self, experiment: Experiment) -> Experiment:
        logger.info(
            "[repo.exp] update start id=%s status=%s",
            experiment.id,
            experiment.status.value,
        )
        try:
            with get_db() as db:
                logger.debug("[repo.exp] update load id=%s", experiment.id)
                orm = db.get(ExperimentORM, experiment.id)
                if not orm:
                    raise NotFoundError("experiment not found")
                orm.feature_id = experiment.feature_id
                orm.name = experiment.name
                orm.status = experiment.status.value
                orm.seed = experiment.seed
                orm.rollout_percent = experiment.rollout_percent
                logger.debug("[repo.exp] update persist id=%s", experiment.id)
                db.commit()
                db.refresh(orm)
                logger.info("[repo.exp] update success id=%s", experiment.id)
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.exp] update error id=%s err=%s",
                experiment.id,
                exc,
                exc_info=True,
            )
            raise

def _to_domain(orm: ExperimentORM) -> Experiment:
    return Experiment(
            id=orm.id,
            feature_id=orm.feature_id,
            name=orm.name,
            status=ExperimentStatus(orm.status),
            seed=orm.seed,
            rollout_percent=orm.rollout_percent,
            )

experiment_table: BaseExperimentTable = ExperimentTable()
