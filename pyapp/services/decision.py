from domain.experiment import ExperimentStatus
from domain.feature import FeatureStatus
from services.feature import feat_svc
from services.experiment import exp_svc
from services.variant import var_svc
from repositories.decisions import dec_table
from utils.errors import ValidationError


class DecisionService:
    def __init__(self) -> None:
        self._feat_svc = feat_svc
        self._exp_svc = exp_svc
        self._var_svc = var_svc
        self._dec_table = dec_table

    def decide(self, request_id: str, feature_key: str, user_id: str, context: dict | None) -> dict:
        # 获取对应功能记录
        feature = self._feat_svc.get_by_key(feature_key)

        # 检查实验是否启动并返回记录
        if feature.status == FeatureStatus.OFF:
            return self._resp(request_id, feature_key, None, "control", {}, "feature_off")
        if feature.status == FeatureStatus.ON:
            return self._resp(request_id, feature_key, None, "enabled", {}, "feature_on")

        if not feature.active_experiment_id:
            return self._resp(request_id, feature_key, None, "control", {}, "experiment_inactive")

        exp = self._exp_svc.get(feature.active_experiment_id)
        if exp.status != ExperimentStatus.RUNNING:
            return self._resp(request_id, feature_key, exp.id, "control", {}, "experiment_inactive")

        # 没有选定实验就默认使用第一个
        vars_ = self._var_svc.list_by_experiment(exp.id)
        if not vars_:
            raise ValidationError("variant required")

        chosen = vars_[0]
        return self._resp(request_id, feature_key, exp.id, chosen.key, chosen.payload, "assigned")


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
