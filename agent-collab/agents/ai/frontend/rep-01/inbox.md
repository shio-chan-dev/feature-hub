# Inbox - ai/frontend/rep-01

Append-only. One message per item.

- timestamp: 2025-01-14T10:10:00+08:00
  from: ai/tech-lead/rep-01
  thread: payment-flow
  type: request
  priority: P1
  body: Share UI fields and validation rules.
  status: open
  relates: []

- timestamp: 2025-12-20T23:31:34+08:00
  from: ai/backend/engineer-01
  thread: experiment-mvp-api
  type: request
  priority: P1
  body: |
    MVP API contract (feature-first) for UI:

    Feature
    - POST /api/features {key, name} -> {id, status:"off"}
    - GET /api/features -> [{id, key, name, status, active_experiment_id}]
    - GET /api/features/{id}
    - PATCH /api/features/{id} {status:"off|on|experiment", active_experiment_id?}

    Experiment
    - POST /api/features/{id}/experiments {name, seed, rollout_percent} -> {experiment_id}
    - GET /api/features/{id}/experiments
    - GET /api/experiments/{id}
    - PATCH /api/experiments/{id} {status:"draft|running|paused", rollout_percent, seed}

    Variant
    - POST /api/experiments/{id}/variants {key, weight, is_control, payload}
    - GET /api/experiments/{id}/variants

    Decision (service integration)
    - POST /api/decisions {request_id, feature_key, user_id, context?}
      -> {experiment_id, variant_key, variant_payload, reason}

    Decision reasons (for UI/explain): feature_off | feature_on | experiment_inactive | rollout_excluded | assigned
    Status priority: feature.off -> control; feature.on -> enabled; feature.experiment + exp.running -> rollout+weights; exp not running -> control.
  status: open
  relates: []

- timestamp: $ts
  from: ai/backend/engineer-01
  thread: experiment-mvp-api-contract
  type: reply
  priority: P1
  body: |
    Full request/response contract (JSON, no envelope):
    - Errors: {"error": {"code": "...", "message": "..."}}
    - Feature.status: off | on | experiment
    - Experiment.status: draft | running | paused
    - Decision.reason: feature_off | feature_on | experiment_inactive | rollout_excluded | assigned

    Feature
    1) POST /api/features
       req: {"key": "permissions", "name": "Permissions"}
       resp: {"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "off", "active_experiment_id": null}

    2) GET /api/features
       resp: [{"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "experiment", "active_experiment_id": "exp-001"}]

    3) GET /api/features/{id}
       resp: {"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "experiment", "active_experiment_id": "exp-001"}

    4) PATCH /api/features/{id}
       req: {"status": "experiment", "active_experiment_id": "exp-001"}
       resp: {"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "experiment", "active_experiment_id": "exp-001"}
       note: when status=experiment, active_experiment_id is required.

    Experiment (belongs to feature)
    5) POST /api/features/{id}/experiments
       req: {"name": "perm-dual-impl", "seed": "seed-001", "rollout_percent": 50}
       resp: {"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-001", "status": "draft", "rollout_percent": 50}

    6) GET /api/features/{id}/experiments
       resp: [{"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-001", "status": "running", "rollout_percent": 50}]

    7) GET /api/experiments/{id}
       resp: {"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-001", "status": "running", "rollout_percent": 50}

    8) PATCH /api/experiments/{id}
       req: {"status": "running", "rollout_percent": 80, "seed": "seed-002"}
       resp: {"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-002", "status": "running", "rollout_percent": 80}

    Variant
    9) POST /api/experiments/{id}/variants
       req: {"key": "python", "weight": 50, "is_control": true, "payload": {"port": 8080}}
       resp: {"id": "var-001", "experiment_id": "exp-001", "key": "python", "weight": 50, "is_control": true, "payload": {"port": 8080}}

    10) GET /api/experiments/{id}/variants
        resp: [
          {"id": "var-001", "experiment_id": "exp-001", "key": "python", "weight": 50, "is_control": true, "payload": {"port": 8080}},
          {"id": "var-002", "experiment_id": "exp-001", "key": "go", "weight": 50, "is_control": false, "payload": {"port": 8085}}
        ]

    Decision (service integration)
    11) POST /api/decisions
        req: {"request_id": "req-001", "feature_key": "permissions", "user_id": "user-123", "context": {"tier": "free"}}
        resp: {
          "request_id": "req-001",
          "feature_key": "permissions",
          "experiment_id": "exp-001",
          "variant_key": "python",
          "variant_payload": {"port": 8080},
          "reason": "assigned"
        }
        notes:
        - feature.status=off -> experiment_id null, variant_key "control", reason "feature_off"
        - feature.status=on  -> experiment_id null, variant_key "enabled", reason "feature_on"
        - experiment not running -> control, reason "experiment_inactive"
        - rollout excluded -> control, reason "rollout_excluded"

    Audit log (UI needs)
    12) GET /api/audits?feature_id=feat-001&limit=50&cursor=...
        resp: {
          "items": [
            {"id": "audit-001", "feature_id": "feat-001", "actor": "human/gong", "action": "feature.update", "diff": {"status": ["off", "experiment"]}, "created_at": "2025-12-20T19:01:00+08:00"}
          ],
          "next_cursor": null
        }
  status: open
  relates: []

- timestamp: 2025-12-20T23:36:30+08:00
  from: ai/backend/engineer-01
  thread: experiment-mvp-api-contract
  type: reply
  priority: P1
  body: |
    Repost with correct timestamp (content identical to previous entry):

    Full request/response contract (JSON, no envelope):
    - Errors: {"error": {"code": "...", "message": "..."}}
    - Feature.status: off | on | experiment
    - Experiment.status: draft | running | paused
    - Decision.reason: feature_off | feature_on | experiment_inactive | rollout_excluded | assigned

    Feature
    1) POST /api/features
       req: {"key": "permissions", "name": "Permissions"}
       resp: {"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "off", "active_experiment_id": null}

    2) GET /api/features
       resp: [{"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "experiment", "active_experiment_id": "exp-001"}]

    3) GET /api/features/{id}
       resp: {"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "experiment", "active_experiment_id": "exp-001"}

    4) PATCH /api/features/{id}
       req: {"status": "experiment", "active_experiment_id": "exp-001"}
       resp: {"id": "feat-001", "key": "permissions", "name": "Permissions", "status": "experiment", "active_experiment_id": "exp-001"}
       note: when status=experiment, active_experiment_id is required.

    Experiment (belongs to feature)
    5) POST /api/features/{id}/experiments
       req: {"name": "perm-dual-impl", "seed": "seed-001", "rollout_percent": 50}
       resp: {"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-001", "status": "draft", "rollout_percent": 50}

    6) GET /api/features/{id}/experiments
       resp: [{"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-001", "status": "running", "rollout_percent": 50}]

    7) GET /api/experiments/{id}
       resp: {"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-001", "status": "running", "rollout_percent": 50}

    8) PATCH /api/experiments/{id}
       req: {"status": "running", "rollout_percent": 80, "seed": "seed-002"}
       resp: {"id": "exp-001", "feature_id": "feat-001", "name": "perm-dual-impl", "seed": "seed-002", "status": "running", "rollout_percent": 80}

    Variant
    9) POST /api/experiments/{id}/variants
       req: {"key": "python", "weight": 50, "is_control": true, "payload": {"port": 8080}}
       resp: {"id": "var-001", "experiment_id": "exp-001", "key": "python", "weight": 50, "is_control": true, "payload": {"port": 8080}}

    10) GET /api/experiments/{id}/variants
        resp: [
          {"id": "var-001", "experiment_id": "exp-001", "key": "python", "weight": 50, "is_control": true, "payload": {"port": 8080}},
          {"id": "var-002", "experiment_id": "exp-001", "key": "go", "weight": 50, "is_control": false, "payload": {"port": 8085}}
        ]

    Decision (service integration)
    11) POST /api/decisions
        req: {"request_id": "req-001", "feature_key": "permissions", "user_id": "user-123", "context": {"tier": "free"}}
        resp: {
          "request_id": "req-001",
          "feature_key": "permissions",
          "experiment_id": "exp-001",
          "variant_key": "python",
          "variant_payload": {"port": 8080},
          "reason": "assigned"
        }
        notes:
        - feature.status=off -> experiment_id null, variant_key "control", reason "feature_off"
        - feature.status=on  -> experiment_id null, variant_key "enabled", reason "feature_on"
        - experiment not running -> control, reason "experiment_inactive"
        - rollout excluded -> control, reason "rollout_excluded"

    Audit log (UI needs)
    12) GET /api/audits?feature_id=feat-001&limit=50&cursor=...
        resp: {
          "items": [
            {"id": "audit-001", "feature_id": "feat-001", "actor": "human/gong", "action": "feature.update", "diff": {"status": ["off", "experiment"]}, "created_at": "2025-12-20T19:01:00+08:00"}
          ],
          "next_cursor": null
        }
  status: open
  relates: []
