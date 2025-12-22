from fastapi import APIRouter, HTTPException, status
from domain.experiment import Experiment
from router.schemas.experiment import ExperimentCreate, ExperimentOut, ExperimentPatch
from services.experiment import exp_svc
from utils.logger import logger


router = APIRouter(tags=["experiments"])


@router.post("/features/{feature_id}/experiments", response_model=ExperimentOut, summary="针对某个feature创建实验")
def create_experiment(feature_id: str, payload: ExperimentCreate):
    try:
        logger.info(
                "[router.exp] create_experiment start feature_id=%s name=%s seed=%s rollout_percent=%s",
                feature_id,
                payload.name,
                payload.seed,
                payload.rollout_percent,
                )
        exp = exp_svc.create(
                feature_id, 
                payload.name,
                payload.seed,
                payload.rollout_percent,
                )
        logger.info(
                "[router.exp] create_experiment success id=%s feature_id=%s",
                exp.id,
                exp.feature_id,
                )
        return _out(exp)
    except Exception as e:
        logger.info(
                "[router.exp] create_experiment error feature_id=%s err=%s",
                feature_id,
                e,
                )
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"创建实验失败"
                )

@router.get("/features/{feature_id}/experiments", response_model=list[ExperimentOut], summary="获取实验列表")
def list_experiments(feature_id: str):
    logger.info("[router.exp] list_experiments start feature_id=%s", feature_id)
    experiments = list(exp_svc.list_by_feature(feature_id))
    logger.info(
            "[router.exp] list_experiments success feature_id=%s count=%s",
            feature_id,
            len(experiments),
            )
    return [_out(e) for e in experiments]

@router.get("/experiments/{experiment_id}", response_model=ExperimentOut)
def get_experiment(experiment_id: str):
    try:
        logger.info("[router.exp] get_experiment start id=%s", experiment_id)
        exp = exp_svc.get(experiment_id)
        logger.info("[router.exp] get_experiment success id=%s", experiment_id)
        return _out(exp)
    except Exception as e:
        logger.info(
                "[router.exp] get_experiment error id=%s err=%s",
                experiment_id,
                e,
                )
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"获取实验记录失败 {str(e)}"
                )

@router.patch("/experiments/{experiment_id}", response_model=ExperimentOut)
def patch_experiment(experiment_id: str, payload: ExperimentPatch):
    try:
        logger.info(
                "[router.exp] patch_experiment start id=%s status=%s rollout_percent=%s seed=%s",
                experiment_id,
                payload.status,
                payload.rollout_percent,
                payload.seed,
                )
        exp = exp_svc.update(experiment_id, payload.status, payload.rollout_percent, payload.seed)
        logger.info(
                "[router.exp] patch_experiment success id=%s status=%s",
                exp.id,
                exp.status,
                )
        return _out(exp)
    except Exception as e:
        logger.info(
                "[router.exp] patch_experiment error id=%s err=%s",
                experiment_id,
                e,
                )
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"更新实验失败 err={str(e)}"
                )

# _out 把领域模型转换为对应的出参数据模型
def _out(exp: Experiment) -> ExperimentOut:
    return ExperimentOut(
            id=exp.id,
            feature_id=exp.feature_id,
            name=exp.name,
            seed=exp.seed,
            status=exp.status,
            rollout_percent=exp.rollout_percent,
            )
