import hashlib
from domain.experiment import ExperimentStatus
from domain.feature import FeatureStatus
from domain.variant import Variant
from services.feature import feat_svc
from services.experiment import exp_svc
from services.variant import var_svc
from repositories.decisions import dec_table
from utils.errors import ValidationError
from utils.logger import logger


class DecisionService:
    def __init__(self) -> None:
        self._feat_svc = feat_svc
        self._exp_svc = exp_svc
        self._var_svc = var_svc
        self._dec_table = dec_table

    def decide(self, request_id: str, feature_key: str, user_id: str, context: dict | None) -> dict:
        # 获取对应功能记录
        feature = self._feat_svc.get_by_key(feature_key)

        # 记录请求走向
        existing = self._dec_table.get_by_request_id(request_id)

        if existing:
            return self._resp(
                    existing.request_id,
                    existing.feature_key,
                    existing.experiment_id,
                    existing.variant_key,
                    existing.variant_payload,
                    existing.reason,
                    )

        # 检查实验是否启动并返回记录
        if feature.status == FeatureStatus.OFF:
            result = self._resp(request_id, feature_key, None, "control", {}, "feature_off")
            return self._record_and_return(feature, user_id, result)
        if feature.status == FeatureStatus.ON:
            result = self._resp(request_id, feature_key, None, "enabled", {}, "feature_on")
            return self._record_and_return(feature, user_id, result)

        # 检查是否存在激化的实验
        if not feature.active_experiment_id:
            result = self._resp(request_id, feature_key, None, "control", {}, "experiment_inactive")
            return self._record_and_return(feature, user_id, result)

        exp = self._exp_svc.get(feature.active_experiment_id)

        # 检查实验状态是否运行
        if exp.status != ExperimentStatus.RUNNING:
            result = self._resp(request_id, feature_key, exp.id, "control", {}, "experiment_inactive")
            return self._record_and_return(feature, user_id, result)

        # 检查实验的变量分组
        variants = list(self._var_svc.list_by_experiment(exp.id))
        if not variants:
            raise ValidationError("variant required")

        # 检查分桶
        if exp.rollout_percent < 100:
            bucket = self._bucket(exp.seed, user_id, f"rollout:{exp.id}", 100)
            if bucket >= exp.rollout_percent:
                result = self._resp(request_id, feature_key, exp.id, "control", {}, "not_in_rollout")
                return self._record_and_return(feature, user_id, result)
        chosen = self._choose_variant(exp.seed, user_id, exp.id, variants)

        result = self._resp(request_id, feature_key, exp.id, chosen.key, chosen.payload, "assigned")
        return self._record_and_return(feature, user_id, result)

    def _record_and_return(self, feature, user_id: str, result: dict) -> dict:
        self._dec_table.record(
                request_id=result["request_id"],
                feature_id=feature.id,
                feature_key=feature.key,
                experiment_id=result["experiment_id"],
                user_id=user_id,
                variant_key=result["variant_key"],
                variant_payload=result["variant_payload"],
                reason=result["reason"],
                )
        return result

    # 计算hash让某个用户在桶中保持文档的分组
    def _bucket(self, seed: str, user_id: str, salt: str, modulo: int) -> int:
        raw = f"{seed}:{salt}:{user_id}".encode("utf-8")
        digest = hashlib.sha256(raw).digest()
        return int.from_bytes(digest, "big") % modulo

    def list_audits(self, feature_id: str, limit: int, cursor: str | None) -> dict:
        items, next_cursor = self._dec_table.list_by_feature(feature_id, limit, cursor)
        return {"items": items, "next_cursor": next_cursor}

    # 选择变量
    def _choose_variant(self, seed: str, user_id: str, exp_id: str, variants: list[Variant]) -> Variant:
        # 计算分组权重是否有效
        total_weight = sum(max(0, v.weight) for v in variants)
        if total_weight <= 0:
            raise ValidationError("variant weight required")

        # 计算hash选择合适的分桶
        pick = self._bucket(seed, user_id, f"variant:{exp_id}", total_weight)
        for v in variants:
            w = max(0, v.weight)
            if pick < w:
                return v
            pick -=w
        return variants[-1]

    # _resp 返回当前请求的字典
    def _resp(self, request_id: str, feature_key: str, experiment_id: str | None, variant_key: str, payload: dict, reason: str) -> dict:
        return {
                "request_id": request_id,
                "feature_key": feature_key,
                "experiment_id": experiment_id,
                "variant_key": variant_key,
                "variant_payload": payload,
                "reason": reason,
                }
dec_svc: DecisionService = DecisionService() 
