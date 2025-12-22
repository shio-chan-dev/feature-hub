# Feature Hub

Feature Hub is a lightweight FastAPI service for managing feature flags and
experiments, then returning a runtime decision for a user request.

It focuses on decision logic only. Metrics collection and analytics should be
handled by your existing tracking stack.

## Scope (current)
- REST APIs for features, experiments, and variants.
- Decision endpoint that resolves a feature + user into a variant.
- In-memory storage (data resets on restart).
- Basic health check and an audit endpoint stub.

## Core concepts
- Feature: A top-level flag that can be off, on, or in experiment mode.
- Experiment: A configuration under a feature with status and rollout percent.
- Variant: A concrete treatment with a key, weight, and payload.
- Decision: The response returned to clients for a given request.

Statuses:
- Feature: `off`, `on`, `experiment`
- Experiment: `draft`, `running`, `paused`

## API overview
Start the service and view interactive docs at `http://localhost:8000/docs`.

- GET `/health` - Health check.
- POST `/features` - Create a feature.
- GET `/features` - List features.
- GET `/features/{feature_id}` - Get a feature.
- PATCH `/features/{feature_id}` - Update a feature status/active experiment.
- POST `/features/{feature_id}/experiments` - Create an experiment.
- GET `/features/{feature_id}/experiments` - List experiments for a feature.
- GET `/experiments/{experiment_id}` - Get an experiment.
- PATCH `/experiments/{experiment_id}` - Update an experiment.
- POST `/experiments/{experiment_id}/variants` - Create a variant.
- GET `/experiments/{experiment_id}/variants` - List variants.
- POST `/decisions` - Resolve a decision.
- GET `/audits?feature_id=...&limit=...&cursor=...` - Audit stub.

## Quick start
Dependencies live in `pyapp/pyproject.toml`. A minimal run flow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
python -m uvicorn pyapp.main:app --reload
```

## Example flow
Create a feature:

```bash
curl -X POST http://localhost:8000/features \
  -H "Content-Type: application/json" \
  -d '{"key":"new_checkout","name":"New Checkout"}'
```

Create an experiment for the feature:

```bash
curl -X POST http://localhost:8000/features/feat-001/experiments \
  -H "Content-Type: application/json" \
  -d '{"name":"checkout-test","seed":"2024q4","rollout_percent":50}'
```

Add variants:

```bash
curl -X POST http://localhost:8000/experiments/exp-001/variants \
  -H "Content-Type: application/json" \
  -d '{"key":"control","weight":50,"is_control":true,"payload":{}}'

curl -X POST http://localhost:8000/experiments/exp-001/variants \
  -H "Content-Type: application/json" \
  -d '{"key":"treatment","weight":50,"is_control":false,"payload":{"ui":"v2"}}'
```

Activate the experiment on the feature:

```bash
curl -X PATCH http://localhost:8000/features/feat-001 \
  -H "Content-Type: application/json" \
  -d '{"status":"experiment","active_experiment_id":"exp-001"}'
```

Request a decision:

```bash
curl -X POST http://localhost:8000/decisions \
  -H "Content-Type: application/json" \
  -d '{"request_id":"req-001","feature_key":"new_checkout","user_id":"u-123","context":{}}'
```

Example response:

```json
{
  "request_id": "req-001",
  "feature_key": "new_checkout",
  "experiment_id": "exp-001",
  "variant_key": "control",
  "variant_payload": {},
  "reason": "assigned"
}
```

## Current behavior and limitations
- Storage is in-memory only; all data resets on service restart.
- Decision logic picks the first variant only; weights, rollout percent, and
  seed are not yet applied.
- The audit endpoint returns an empty list.
- The database scaffolding in `pyapp/repositories/db` is not wired in.
- The feature PATCH route path uses `{feture_id}` in `pyapp/router/feature.py`,
  while the handler expects `feature_id`; align them if you hit routing errors.

## Project layout
- `pyapp/` - FastAPI application code.
- `pyapp/router/` - API routes and request/response schemas.
- `pyapp/services/` - Business logic.
- `pyapp/repositories/` - In-memory repositories.
- `agent-collab/` - Multi-agent collaboration docs.
