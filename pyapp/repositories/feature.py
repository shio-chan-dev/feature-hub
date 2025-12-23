from uuid import uuid4
from typing import Sequence
from abc import ABC, abstractmethod

from sqlalchemy import select

from domain.feature import Feature, FeatureStatus
from repositories.db.models import FeatureORM
from repositories.db.init import get_db
from utils.errors import NotFoundError
from utils.logger import logger
from utils.misc import new_id


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

class FeatureTable(BaseFeatureTable):
    def create(self, feature: Feature) -> Feature:
        logger.info(
            "[repo.feat] create start key=%s name=%s",
            feature.key,
            feature.name,
        )
        feature_id = feature.id or new_id("feat")
        logger.debug("[repo.feat] create prepared id=%s", feature_id)
        try:
            with get_db() as db:
                orm = FeatureORM(
                        id=feature_id,
                        key=feature.key,
                        name=feature.name,
                        status=feature.status.value,
                        active_experiment_id=feature.active_experiment_id,
                        )
                logger.debug("[repo.feat] create persist id=%s", feature_id)
                db.add(orm)
                db.commit()
                db.refresh(orm)
                logger.info(
                    "[repo.feat] create success id=%s key=%s",
                    orm.id,
                    orm.key,
                )
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.feat] create error id=%s key=%s err=%s",
                feature_id,
                feature.key,
                exc,
                exc_info=True,
            )
            raise

    def list(self) -> Sequence[Feature]:
        logger.info("[repo.feat] list start")
        try:
            with get_db() as db:
                logger.debug("[repo.feat] list query")
                items = db.scalars(select(FeatureORM)).all()
                logger.info("[repo.feat] list success count=%s", len(items))
                return [_to_domain(i) for i in items]
        except Exception as exc:
            logger.error("[repo.feat] list error err=%s", exc, exc_info=True)
            raise

    def get(self, feature_id: str) -> Feature:
        logger.info("[repo.feat] get start id=%s", feature_id)
        try:
            with get_db() as db:
                logger.debug("[repo.feat] get query id=%s", feature_id)
                orm = db.get(FeatureORM, feature_id)
                if not orm:
                    raise NotFoundError("feature not found")
                logger.info("[repo.feat] get success id=%s", feature_id)
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.feat] get error id=%s err=%s",
                feature_id,
                exc,
                exc_info=True,
            )
            raise


    def get_by_key(self, key: str) -> Feature:
        logger.info("[repo.feat] get_by_key start key=%s", key)
        try:
            with get_db() as db:
                logger.debug("[repo.feat] get_by_key query key=%s", key)
                orm = db.scalar(select(FeatureORM).where(FeatureORM.key == key))
                if not orm:
                    raise NotFoundError("feature not found")
                logger.info("[repo.feat] get_by_key success key=%s", key)
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.feat] get_by_key error key=%s err=%s",
                key,
                exc,
                exc_info=True,
            )
            raise

    def update(self, feature: Feature) -> Feature:
        logger.info(
            "[repo.feat] update start id=%s status=%s",
            feature.id,
            feature.status.value,
        )
        try:
            with get_db() as db:
                logger.debug("[repo.feat] update load id=%s", feature.id)
                orm = db.get(FeatureORM, feature.id)
                if not orm:
                    raise NotFoundError("feature not found")
                orm.key = feature.key
                orm.name = feature.name
                orm.status = feature.status.value
                orm.active_experiment_id = feature.active_experiment_id
                logger.debug("[repo.feat] update persist id=%s", feature.id)
                db.commit()
                db.refresh(orm)
                logger.info("[repo.feat] update success id=%s", feature.id)
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.feat] update error id=%s err=%s",
                feature.id,
                exc,
                exc_info=True,
            )
            raise


def _to_domain(orm: FeatureORM) -> Feature:
    return Feature(
            id=orm.id,
            key=orm.key,
            name=orm.name,
            status=FeatureStatus(orm.status),
            active_experiment_id=orm.active_experiment_id,
            )

feature_table: BaseFeatureTable = FeatureTable()
