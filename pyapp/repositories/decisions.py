# pyapp/repositories/decisions.py

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from domain.decisions import DecisionAudit, DecisionAuditView
from repositories.db.init import get_db
from repositories.db.models import DecisionORM, FeatureORM, ExperimentORM, VariantORM
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
            self,
            feature_id: str,
            limit: int,
            offset: int,
            experiment_id: str | None = None,
            variant_id: str | None = None,
            variant_key: str | None = None,
            reasons: Sequence[str] | None = None,
            user_id: str | None = None,
            request_id: str | None = None,
            from_ts: datetime | None = None,
            to_ts: datetime | None = None,
            ) -> tuple[Sequence[DecisionAuditView], int | None]:
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

    def list_by_feature(
            self,
            feature_id: str,
            limit: int,
            offset: int,
            experiment_id: str | None = None,
            variant_id: str | None = None,
            variant_key: str | None = None,
            reasons: Sequence[str] | None = None,
            user_id: str | None = None,
            request_id: str | None = None,
            from_ts: datetime | None = None,
            to_ts: datetime | None = None,
            ) -> tuple[Sequence[DecisionAuditView], int | None]:
        logger.info("[fakerepo.decision] start get decision by feature from memory feature_id=%s", feature_id)
        items: list[DecisionAudit] = []
        for audit in self._items:
            if audit.feature_id != feature_id:
                continue
            if experiment_id and audit.experiment_id != experiment_id:
                continue
            if variant_key and audit.variant_key != variant_key:
                continue
            if reasons and audit.reason not in reasons:
                continue
            if user_id and audit.user_id != user_id:
                continue
            if request_id and audit.request_id != request_id:
                continue
            if from_ts and audit.decided_at < from_ts:
                continue
            if to_ts and audit.decided_at > to_ts:
                continue
            if variant_id:
                continue
            items.append(audit)
        items.sort(key=lambda item: (item.decided_at, item.id), reverse=True)
        page = items[offset:offset + limit]
        next_offset = offset + len(page) if offset + len(page) < len(items) else None
        views = [
                DecisionAuditView(
                        id=audit.id,
                        decided_at=audit.decided_at,
                        request_id=audit.request_id,
                        user_id=audit.user_id,
                        feature_id=audit.feature_id,
                        feature_key=audit.feature_key,
                        feature_name=None,
                        experiment_id=audit.experiment_id,
                        experiment_name=None,
                        variant_id=None,
                        variant_key=audit.variant_key,
                        is_control=None,
                        reason=audit.reason,
                        variant_payload=dict(audit.variant_payload),
                        )
                for audit in page
                ]
        logger.info("[fakerepo.dicision] get decision record from memory success")
        return views, next_offset

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
            self,
            feature_id: str,
            limit: int,
            offset: int,
            experiment_id: str | None = None,
            variant_id: str | None = None,
            variant_key: str | None = None,
            reasons: Sequence[str] | None = None,
            user_id: str | None = None,
            request_id: str | None = None,
            from_ts: datetime | None = None,
            to_ts: datetime | None = None,
            ) -> tuple[Sequence[DecisionAuditView], int | None]:
        logger.info("[repo.decision] list by feature start feature_id=%s", feature_id)
        with get_db() as db:
            stmt = (
                    select(
                            DecisionORM,
                            FeatureORM.name,
                            ExperimentORM.name,
                            VariantORM.id,
                            VariantORM.is_control,
                            )
                    .join(FeatureORM, FeatureORM.id == DecisionORM.feature_id)
                    .outerjoin(ExperimentORM, ExperimentORM.id == DecisionORM.experiment_id)
                    .outerjoin(VariantORM, VariantORM.id == DecisionORM.variant_id)
                    .where(DecisionORM.feature_id == feature_id)
                    )
            if experiment_id:
                stmt = stmt.where(DecisionORM.experiment_id == experiment_id)
            if variant_id:
                stmt = stmt.where(DecisionORM.variant_id == variant_id)
            if variant_key:
                stmt = stmt.where(DecisionORM.variant_key == variant_key)
            if reasons:
                stmt = stmt.where(DecisionORM.reason.in_(reasons))
            if user_id:
                stmt = stmt.where(DecisionORM.user_id == user_id)
            if request_id:
                stmt = stmt.where(DecisionORM.request_id == request_id)
            if from_ts:
                stmt = stmt.where(DecisionORM.decided_at >= from_ts)
            if to_ts:
                stmt = stmt.where(DecisionORM.decided_at <= to_ts)
            rows = db.execute(
                    stmt
                    .order_by(DecisionORM.decided_at.desc(), DecisionORM.id.desc())
                    .offset(offset)
                    .limit(limit)
                    ).all()
            items: list[DecisionAuditView] = []
            for decision, feature_name, experiment_name, variant_id_val, is_control in rows:
                items.append(
                        DecisionAuditView(
                                id=decision.id,
                                decided_at=decision.decided_at,
                                request_id=decision.request_id,
                                user_id=decision.user_id,
                                feature_id=decision.feature_id,
                                feature_key=decision.feature_key,
                                feature_name=feature_name,
                                experiment_id=decision.experiment_id,
                                experiment_name=experiment_name,
                                variant_id=variant_id_val,
                                variant_key=decision.variant_key,
                                is_control=is_control,
                                reason=decision.reason,
                                variant_payload=decision.variant_payload or {},
                                )
                        )
            next_offset = offset + len(items) if len(items) == limit else None
            logger.info(
                    "[repo.decision] list by feature success feature_id=%s count=%s",
                    feature_id,
                    len(items),
                    )
            return items, next_offset

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
