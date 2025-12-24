# pyapp/repositories/decisions.py

from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from domain.decisions import DecisionAudit
from repositories.db.init import get_db
from repositories.db.models import DecisionORM, VariantORM
from utils.logger import logger

class BaseDecisionTable(ABC):
    @abstractmethod
    def record(
            self,
            audit: DecisionAudit,
            ) -> DecisionAudit:
        ...

    @abstractmethod
    def get_by_request_id(self, request_id: str) -> DecisionAudit | None:
        ...

    @abstractmethod
    def list_by_feature(
            self, feature_id: str, limit: int, cursor: str | None
            ) -> tuple[Sequence[DecisionAudit], str | None]:
        ...

class FakeDecisionTable(BaseDecisionTable):
    def __init__(self) -> None:
        self._items: list[DecisionAudit] = []
        self._by_request: dict[str, DecisionAudit] = {}

    def record(self, audit: DecisionAudit) -> DecisionAudit:
        logger.info(
                "[fakerepo.decision] start record decision into memory feature_id=%s feature_key=%s",
                audit.feature_id,
                audit.feature_key,
                )
        existing = self._by_request.get(audit.request_id)
        if existing:
            return existing

        self._items.append(audit)
        self._by_request[audit.request_id] = audit
        logger.info("[fakerepo.decision] record into memory success")
        return audit

    def get_by_request_id(self, request_id: str) -> DecisionAudit | None:
        return self._by_request.get(request_id)

    def list_by_feature(self, feature_id: str, limit: int, cursor: str | None) -> tuple[Sequence[DecisionAudit], str | None]:
        logger.info("[fakerepo.decision] start get decision by feature from memory feature_id=%s", feature_id)
        items = [a for a in self._items if a.feature_id == feature_id]
        start = int(cursor) if cursor else 0
        page = items[start:start + limit]
        next_cursor = str(start + len(page)) if start + len(page) < len(items) else None
        logger.info("[fakerepo.dicision] get decision record from memory success")
        return page, next_cursor

class DecisionTable(BaseDecisionTable):
    def record(self, audit: DecisionAudit) -> DecisionAudit:
        logger.info(
                "[repo.decision] start record decision request_id=%s feature_id=%s",
                audit.request_id,
                audit.feature_id,
                )
        with get_db() as db:
            existing = db.scalar(
                    select(DecisionORM).where(DecisionORM.request_id == audit.request_id)
                    )
            if existing:
                return self._to_audit(existing)

            variant_id = None
            if audit.experiment_id and audit.variant_key:
                variant_id = db.scalar(
                        select(VariantORM.id).where(
                                VariantORM.experiment_id == audit.experiment_id,
                                VariantORM.key == audit.variant_key,
                                )
                        )

            orm = DecisionORM(
                    id=audit.id,
                    request_id=audit.request_id,
                    feature_id=audit.feature_id,
                    feature_key=audit.feature_key,
                    experiment_id=audit.experiment_id,
                    user_id=audit.user_id,
                    variant_id=variant_id,
                    variant_key=audit.variant_key,
                    variant_payload=audit.variant_payload,
                    reason=audit.reason,
                    decided_at=audit.decided_at,
                    )
            db.add(orm)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                existing = db.scalar(
                        select(DecisionORM).where(DecisionORM.request_id == audit.request_id)
                        )
                if existing:
                    return self._to_audit(existing)
                raise
            db.refresh(orm)
            logger.info(
                    "[repo.decision] record decision success request_id=%s",
                    audit.request_id,
                    )
            return self._to_audit(orm)

    def get_by_request_id(self, request_id: str) -> DecisionAudit | None:
        with get_db() as db:
            orm = db.scalar(
                    select(DecisionORM).where(DecisionORM.request_id == request_id)
                    )
            if not orm:
                return None
            return self._to_audit(orm)

    def list_by_feature(
            self, feature_id: str, limit: int, cursor: str | None
            ) -> tuple[Sequence[DecisionAudit], str | None]:
        logger.info("[repo.decision] list by feature start feature_id=%s", feature_id)
        start = int(cursor) if cursor else 0
        with get_db() as db:
            rows = db.scalars(
                    select(DecisionORM)
                    .where(DecisionORM.feature_id == feature_id)
                    .order_by(DecisionORM.decided_at.desc())
                    .offset(start)
                    .limit(limit)
                    ).all()
            items = [self._to_audit(row) for row in rows]
            next_cursor = str(start + len(items)) if len(items) == limit else None
            logger.info(
                    "[repo.decision] list by feature success feature_id=%s count=%s",
                    feature_id,
                    len(items),
                    )
            return items, next_cursor

    def _to_audit(self, orm: DecisionORM) -> DecisionAudit:
        return DecisionAudit(
                id=orm.id,
                request_id=orm.request_id,
                feature_id=orm.feature_id,
                feature_key=orm.feature_key,
                experiment_id=orm.experiment_id,
                user_id=orm.user_id,
                variant_key=orm.variant_key,
                variant_payload=orm.variant_payload or {},
                reason=orm.reason,
                decided_at=orm.decided_at,
                )

dec_table: BaseDecisionTable = DecisionTable()
