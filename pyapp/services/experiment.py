
from domain.experiment import Experiment, ExperimentStatus
from repositories.experiment import experiment_table
from utils.errors import ValidationError

class ExperimentService:
    def __init__(self) -> None:
        self._table = experiment_table

    # create 创建一个新的实验任务,并返回对应的领域模型
    def create(self, feature_id: str, name: str, seed: str, roollout_percent: int) -> Experiment:
        if roollout_percent < 0 or roollout_percent > 100:
            raise ValidationError("rollout percent ragne")

        # 创建一个新的实验对象
        exp = Experiment(
                id=None,
                feature_id=feature_id,
                name=name,
                seed=seed,
                status=ExperimentStatus.DRAFT,
                rollout_percent=roollout_percent,
                )
        return self._table.create(exp)

    # list_by_feature 通过feature id获取对应的实验 
    def list_by_feature(self, feature_id: str) -> list[Experiment]:
        return list(self._table.list_by_feature(feature_id))

    # get 通过实验id获取对应实验记录
    def get(self, experiment_id: str) -> Experiment:
        return self._table.get(experiment_id)

    #
    def update(
        self,
        experiment_id: str,
        status: str | None,
        rollout_percent: int | None,
        seed: str | None,
        name: str | None,
    ) -> Experiment:
        exp = self._table.get(experiment_id)
        if name is not None:
            exp.name = name
        if status is not None:
            try:
                exp.status = ExperimentStatus(status)
            except ValueError:
                raise ValidationError("invalid status")

        if rollout_percent is not None:
            if rollout_percent < 0 or rollout_percent > 100:
                raise ValidationError("rollout_percent_range")
            exp.rollout_percent = rollout_percent

        if seed is not None:
            exp.seed = seed
        return self._table.update(exp)

exp_svc: ExperimentService = ExperimentService()


