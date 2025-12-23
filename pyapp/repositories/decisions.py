# pyapp/repositories/decisions.py

from abc import ABC, abstractmethod
from datetime import timezone, datetime
from typing import Sequence

from domain.decisions import DecisionAudit

class BaseDecisionTable(ABC):
    @abstractmethod
    def record(
            self,
            request_id: str,
            feature_id: str,
            feature_key: str,
            experiment_id: str | None,
            user_id: str,
            variant_key: str,
            variant_payload: dict,
            reason: str,
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
        self._seq = 0

    def record(self, request_id: str, feature_id: str, feature_key: str, experiment_id: str | None, user_id: str, variant_key: str, variant_payload: dict, reason: str) -> DecisionAudit:
        existing = self._by_request.get(request_id)
        if existing:
            return existing

        self._seq += 1
        audit = DecisionAudit(
                id=f"dec-{self._seq:06d}",
                request_id=request_id,
                feature_id=feature_id,
                feature_key=feature_key,
                experiment_id=experiment_id,
                user_id=user_id,
                variant_key=variant_key,
                variant_payload=variant_payload,
                reason=reason,
                decided_at=datetime.now(timezone.utc),
                )
        self._items.append(audit)
        self._by_request[request_id] = audit
        return audit

    def get_by_request_id(self, request_id: str) -> DecisionAudit | None:
        return self._by_request.get(request_id)

    def list_by_feature(self, feature_id: str, limit: int, cursor: str | None) -> tuple[Sequence[DecisionAudit], str | None]:
        items = [a for a in self._items if a.feature_id == feature_id]
        start = int(cursor) if cursor else 0
        page = items[start:start + limit]
        next_cursor = str(start + len(page)) if start + len(page) < len(items) else None
        return page, next_cursor

dec_table: BaseDecisionTable = FakeDecisionTable()
