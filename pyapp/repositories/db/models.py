from datetime import datetime, timezone
from time import timezone
from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from repositories.db.init import Base, JSONField

class FeatureORM(Base):
    __tablename__ = "features"
    __table_args__ = (
            UniqueConstraint("key", name="uq_feature_key"),
            {"comment": "Feature flags" }
            )
    id = Column(String(64), primary_key=True, comment="Primary key")
    key = Column(String(128), nullable=False, comment="Feature key")
    name = Column(String(255), nullable=False, comment="Display name")
    status = Column(String(32), nullable=False, comment="Status: off/on/experiment")
    active_experiment_id = Column(
            String(64),
            ForeignKey("experiments.id", name="fk_feature_active_experiment", use_alter=True),
            nullable=True,
            comment="active experiment id",
            )

    experiments = relationship(
            "ExperimentORM",
            back_populates="feature",
            foreign_keys="ExperimentORM.feature_id",
            cascade="all, delete-orphan",
            )

    active_experiment = relationship(
            "ExperimentORM",
            foreign_keys=[active_experiment_id],
            post_update=True,
            )

class ExperimentORM(Base):
    __tablename__ = "experiments"
    __table_args__ = (
            {"comment": "Experiment configuration"},
            )
    
    id = Column(String(64), primary_key=True, comment="Primary key")
    feature_id = Column(
            String(64),
            ForeignKey("features.id", name="fk_experiment_feature_id"),
            nullable=False,
            index=True,
            comment="Feature id",
            )
    name = Column(String(255), nullable=False, comment="Experiment name")
    status = Column(String(32), nullable=False, comment="Status: draft/running/paused")
    seed = Column(String(64), nullable=False, comment="Bucketing seed")
    rollout_percent = Column(Integer, nullable=False, default=0, comment="Rollout percent(0-100)")
    
    feature = relationship(
            "FeatureORM",
            back_populates="experiments",
            foreign_keys=[feature_id],
            )

    variants = relationship(
            "VariantORM",
            back_populates="experiment",
            cascade="all, delete-orphan"
            )

class VariantORM(Base):
    __tablename__ = "variants"
    __table_args__ = (
            UniqueConstraint("experiment_id", "key", name="uq_variant_experiment_key"),
            {
                "comment": "Experiment variants",
                }
            )

    id = Column(String(64), primary_key=True, comment="Primary key")
    experiment_id = Column(
            String(64),
            ForeignKey("experiments.id", name="fk_variant_experiment_id"),
            nullable=False,
            index=True,
            comment="Experiment id",
            )
    key = Column(String(64), nullable=False, comment="Variant key")
    weight = Column(Integer, nullable=False, comment="Allocation weight")
    is_control = Column(Boolean, nullable=False, default=False, comment="Is control variant")
    payload = Column(JSONField, nullable=False, comment="Variant payload JSON")

    experiment = relationship(
            "ExperimentORM",
            back_populates="variants",
            foreign_keys=[experiment_id],
            )


class DecisionORM(Base):
    __tablename__ = "decisions"
    __table_args__ = (
            UniqueConstraint("request_id", name="uq_decision_request_id"),
            {"comment": "Decision audit log"}
            )
    id = Column(String(64), primary_key=True, comment="Primary key")
    request_id = Column(String(64), nullable=False, comment="Idempotency request id")
    feature_id = Column(String(64), nullable=False, index=True, comment="Feature id")
    feature_key = Column(String(128), nullable=False, index=True, comment="Feature key")
    experiment_id = Column(
            String(64),
            ForeignKey("experiments.id", name="fk_decision_experiment_id"),
            nullable=True,
            index=True,
            comment="Experiment id",
            )
    user_id = Column(String(64), nullable=False, index=True, comment="User id")
    variant_id = Column(
            String(64),
            ForeignKey("variants.id", name="fk_decision_variant_id"),
            nullable=True,
            index=True,
            comment="Variant id",
            )
    variant_key = Column(String(64), nullable=False, comment="Variant key")
    variant_payload = Column(JSONField, nullable=False, comment="Variant payload JSON")
    reason = Column(String(32), nullable=False, comment="Decision reason")
    decided_at = Column(
            DateTime, 
            nullable=False, 
            default=lambda: datetime.now(timezone.utc), 
            comment="Decision time (UTC)"
            )

    experiment = relationship("ExperimentORM", foreign_keys=[experiment_id])
    variant = relationship("VariantORM",foreign_keys=[variant_id])
