from abc import ABC, abstractmethod
from collections.abc import Sequence

from sqlalchemy import select


from domain.variant import Variant
from repositories.db.models import VariantORM
from repositories.db.init import get_db
from utils.logger import logger
from utils.misc import new_id


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

class VariantTable(BaseVariantTable):
    def add(self, variant: Variant) -> Variant:
        logger.info(
            "[repo.var] add start experiment_id=%s key=%s",
            variant.experiment_id,
            variant.key,
        )
        variant_id = variant.id or new_id("var")
        logger.debug("[repo.var] add prepared id=%s", variant_id)
        try:
            with get_db() as db:
                orm = VariantORM(
                        id=variant_id,
                        experiment_id=variant.experiment_id,
                        key=variant.key,
                        weight=variant.weight,
                        is_control=variant.is_control,
                        payload=dict(variant.payload),
                        )
                logger.debug("[repo.var] add persist id=%s", variant_id)
                db.add(orm)
                db.commit()
                db.refresh(orm)
                logger.info(
                    "[repo.var] add success id=%s experiment_id=%s",
                    orm.id,
                    orm.experiment_id,
                )
                return _to_domain(orm)
        except Exception as exc:
            logger.error(
                "[repo.var] add error id=%s experiment_id=%s err=%s",
                variant_id,
                variant.experiment_id,
                exc,
                exc_info=True,
            )
            raise


    def list_by_experiment(self, experiment_id: str) -> Sequence[Variant]:
        logger.info("[repo.var] list_by_experiment start experiment_id=%s", experiment_id)
        try:
            with get_db() as db:
                logger.debug(
                    "[repo.var] list_by_experiment query experiment_id=%s",
                    experiment_id,
                )
                items = db.scalars(
                        select(VariantORM).where(VariantORM.experiment_id == experiment_id)
                        ).all()
                logger.info(
                    "[repo.var] list_by_experiment success experiment_id=%s count=%s",
                    experiment_id,
                    len(items),
                )
                return [_to_domain(i) for i in items]
        except Exception as exc:
            logger.error(
                "[repo.var] list_by_experiment error experiment_id=%s err=%s",
                experiment_id,
                exc,
                exc_info=True,
            )
            raise


def _to_domain(orm: VariantORM) -> Variant:
    return Variant(
            id=orm.id,
            experiment_id=orm.experiment_id,
            key=orm.key,
            weight=orm.weight,
            is_control=orm.is_control,
            payload=orm.payload,
            )

var_table: BaseVariantTable = VariantTable()
