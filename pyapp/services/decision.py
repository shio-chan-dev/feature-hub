import hashlib
from datetime import datetime, timezone
from domain.decisions import DecisionAudit
from domain.experiment import ExperimentStatus
from domain.feature import FeatureStatus
from domain.variant import Variant
from services.feature import feat_svc
from services.experiment import exp_svc
from services.variant import var_svc
from repositories.decisions import dec_table
from utils.errors import ValidationError
from utils.logger import logger
from utils.misc import new_id


class DecisionService:
    def __init__(self) -> None:
        self._feat_svc = feat_svc
        self._exp_svc = exp_svc
        self._var_svc = var_svc
        self._dec_table = dec_table

    def decide(self, request_id: str, feature_key: str, user_id: str, context: dict | None) -> dict:
        logger.info(
            "[svc.dec] decide start request_id=%s feature_key=%s user_id=%s",
            request_id,
            feature_key,
            user_id,
        )
        logger.debug("[svc.dec] load feature key=%s", feature_key)
        feature = self._feat_svc.get_by_key(feature_key)
        logger.debug(
            "[svc.dec] feature loaded id=%s status=%s active_experiment_id=%s",
            feature.id,
            feature.status.value,
            feature.active_experiment_id,
        )

        logger.debug("[svc.dec] check existing decision request_id=%s", request_id)
        # 如果出现了同样的request，走一样的分流进行返回
        existing = self._dec_table.get_by_request_id(request_id)
        if existing:
            logger.info(
                "[svc.dec] decide cached request_id=%s reason=%s",
                request_id,
                existing.reason,
            )
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
            logger.debug("[svc.dec] feature off request_id=%s", request_id)
            result = self._resp(request_id, feature_key, None, "control", {}, "feature_off")
            return self._record_and_return(feature, user_id, result)
        if feature.status == FeatureStatus.ON:
            logger.debug("[svc.dec] feature on request_id=%s", request_id)
            result = self._resp(request_id, feature_key, None, "enabled", {}, "feature_on")
            return self._record_and_return(feature, user_id, result)

        # 检查是否存在激化的实验
        if not feature.active_experiment_id:
            logger.debug("[svc.dec] no active experiment request_id=%s", request_id)
            result = self._resp(request_id, feature_key, None, "control", {}, "experiment_inactive")
            return self._record_and_return(feature, user_id, result)

        logger.debug(
            "[svc.dec] load experiment id=%s request_id=%s",
            feature.active_experiment_id,
            request_id,
        )
        exp = self._exp_svc.get(feature.active_experiment_id)
        logger.debug(
            "[svc.dec] experiment loaded id=%s status=%s rollout_percent=%s",
            exp.id,
            exp.status.value,
            exp.rollout_percent,
        )

        # 检查实验状态是否运行
        if exp.status != ExperimentStatus.RUNNING:
            logger.debug("[svc.dec] experiment not running id=%s", exp.id)
            result = self._resp(request_id, feature_key, exp.id, "control", {}, "experiment_inactive")
            return self._record_and_return(feature, user_id, result)

        # 检查实验的变量分组
        variants = list(self._var_svc.list_by_experiment(exp.id))
        logger.debug("[svc.dec] variants loaded experiment_id=%s count=%s", exp.id, len(variants))
        if not variants:
            raise ValidationError("variant required")

        # 检查分桶
        if exp.rollout_percent < 100:
            logger.debug(
                "[svc.dec] rollout gate experiment_id=%s percent=%s",
                exp.id,
                exp.rollout_percent,
            )
            bucket = self._bucket(exp.seed, user_id, f"rollout:{exp.id}", 100)
            logger.debug(
                "[svc.dec] rollout bucket=%s experiment_id=%s rollout_percent=%s",
                bucket,
                exp.id,
                exp.rollout_percent,
            )
            if bucket >= exp.rollout_percent:
                result = self._resp(request_id, feature_key, exp.id, "control", {}, "not in rollout")
                return self._record_and_return(feature, user_id, result)
        logger.debug("[svc.dec] choose variant experiment_id=%s", exp.id)
        chosen = self._choose_variant(exp.seed, user_id, exp.id, variants)
        logger.debug(
            "[svc.dec] variant chosen id=%s key=%s weight=%s",
            chosen.id,
            chosen.key,
            chosen.weight,
        )

        result = self._resp(request_id, feature_key, exp.id, chosen.key, chosen.payload, "assigned")
        return self._record_and_return(feature, user_id, result)

    def _record_and_return(self, feature, user_id: str, result: dict) -> dict:
        logger.debug(
            "[svc.dec] record start request_id=%s feature_id=%s experiment_id=%s variant_key=%s reason=%s",
            result["request_id"],
            feature.id,
            result["experiment_id"],
            result["variant_key"],
            result["reason"],
        )
        self._dec_table.record(
                DecisionAudit(
                        id=new_id("dec"),
                        request_id=result["request_id"],
                        feature_id=feature.id,
                        feature_key=feature.key,
                        experiment_id=result["experiment_id"],
                        user_id=user_id,
                        variant_key=result["variant_key"],
                        variant_payload=result["variant_payload"],
                        reason=result["reason"],
                        decided_at=datetime.now(timezone.utc),
                        )
                )
        logger.info(
            "[svc.dec] decide success request_id=%s feature_key=%s reason=%s",
            result["request_id"],
            result["feature_key"],
            result["reason"],
        )
        return result

    # 计算hash让某个用户在桶中保持文档的分组
    def _bucket(self, seed: str, user_id: str, salt: str, modulo: int) -> int:
        logger.debug(
            "[svc.dec] bucket start seed=%s salt=%s modulo=%s",
            seed,
            salt,
            modulo,
        )
        raw = f"{seed}:{salt}:{user_id}".encode("utf-8")
        digest = hashlib.sha256(raw).digest()
        value = int.from_bytes(digest, "big") % modulo
        logger.debug("[svc.dec] bucket result value=%s", value)
        return value

    def list_audits(self, feature_id: str, limit: int, cursor: str | None) -> dict:
        logger.info(
            "[svc.dec] list_audits start feature_id=%s limit=%s cursor=%s",
            feature_id,
            limit,
            cursor,
        )
        items, next_cursor = self._dec_table.list_by_feature(feature_id, limit, cursor)
        logger.info(
            "[svc.dec] list_audits success feature_id=%s count=%s next_cursor=%s",
            feature_id,
            len(items),
            next_cursor,
        )
        return {"items": items, "next_cursor": next_cursor}

    # 选择变量
    def _choose_variant(self, seed: str, user_id: str, exp_id: str, variants: list[Variant]) -> Variant:
        # 计算分组权重是否有效
        total_weight = sum(max(0, v.weight) for v in variants)
        logger.debug(
            "[svc.dec] choose_variant total_weight=%s experiment_id=%s",
            total_weight,
            exp_id,
        )
        if total_weight <= 0:
            raise ValidationError("variant weight required")

        # 计算hash选择合适的分桶
        pick = self._bucket(seed, user_id, f"variant:{exp_id}", total_weight)
        logger.debug(
            "[svc.dec] choose_variant pick=%s experiment_id=%s",
            pick,
            exp_id,
        )
        for v in variants:
            w = max(0, v.weight)
            logger.debug(
                "[svc.dec] choose_variant step pick=%s key=%s weight=%s",
                pick,
                v.key,
                w,
            )
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
