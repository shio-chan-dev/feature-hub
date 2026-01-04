from uuid import uuid4
from domain.feature import Feature, FeatureStatus
from repositories.feature import feature_table
from utils.errors import ConflictError, NotFoundError, ValidationError


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


class FeatureService:
    def __init__(self) -> None:
        self._table = feature_table

    def create(self, key: str, name: str) -> Feature:
        if not key or not name:
            raise ValidationError
        try:
            self._table.get_by_key(key)
            raise ConflictError("feature key exists")
        except NotFoundError:
            pass

        feat = Feature(
               id = None,
               key=key,
               name=name,
               status=FeatureStatus.OFF,
               active_experiment_id=None,
                )
        return self._table.create(feat)

    def list(self, status: str | None = None, limit: int | None = None) -> list[Feature]:
        items = list(self._table.list())
        if status is not None:
            try:
                status_enum = FeatureStatus(status)
            except ValueError:
                raise ValidationError("invalid_status")
            items = [item for item in items if item.status == status_enum]
        if limit is not None:
            if limit <= 0:
                raise ValidationError("limit_range")
            items = items[:limit]
        return items

    def update(
        self,
        feature_id: str,
        status: str | None,
        active_experiment_id: str | None,
        name: str | None,
    ) -> Feature:
        feat = self._table.get(feature_id)
        if name is not None:
            feat.name = name

        if status is not None:
            try:
                status_enum = FeatureStatus(status)
            except ValueError:
                raise ValidationError("invalid_status")

            if status_enum != FeatureStatus.EXPERIMENT:
                active_experiment_id = None
            if status_enum == FeatureStatus.EXPERIMENT and not active_experiment_id:
                raise ValidationError("acitve experiment id required")

            feat.status = status_enum
            feat.active_experiment_id = active_experiment_id
        elif active_experiment_id is not None:
            if feat.status != FeatureStatus.EXPERIMENT:
                raise ValidationError("active experiment id requires experiment status")
            feat.active_experiment_id = active_experiment_id
        return self._table.update(feat)

    def get_by_key(self, key: str) -> Feature:
        return self._table.get_by_key(key)

    def get(self, feature_id: str) -> Feature:
        return self._table.get(feature_id)


feat_svc: FeatureService = FeatureService()
