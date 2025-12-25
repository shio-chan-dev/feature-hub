# Feature Hub Decision API

## Base URL
- Default dev: `http://localhost:6789`
- Note: `README.md` examples use `http://localhost:8000` when running uvicorn. Confirm the actual port or set `API_BASE_URL`.

## Endpoint
`POST /decisions`

### Request body
```json
{"request_id":"req-001","feature_key":"new_checkout","user_id":"u-123","context":{}}
```

### Response fields
- `request_id`: string
- `feature_key`: string
- `experiment_id`: string | null
- `variant_key`: string
- `variant_payload`: object
- `reason`: `feature_off` | `feature_on` | `experiment_inactive` | `assigned`

### Example response
```json
{"request_id":"req-001","feature_key":"new_checkout","experiment_id":"exp-001","variant_key":"control","variant_payload":{},"reason":"assigned"}
```

## Decision behavior
- `feature.status = off` → `reason=feature_off`, `variant_key=control`
- `feature.status = on` → `reason=feature_on`, `variant_key=enabled`
- experiment missing or not `running` → `reason=experiment_inactive`
- experiment `running` → pick first variant, `reason=assigned`

## Typical setup flow (prerequisites)
1. `POST /features` (create feature)
2. `POST /features/{feature_id}/experiments` (create experiment)
3. `POST /experiments/{experiment_id}/variants` (add variants)
4. `PATCH /features/{feature_id}` set `status=experiment` and `active_experiment_id`
5. `PATCH /experiments/{experiment_id}` set `status=running`
6. `POST /decisions`

## Error format
- 400: business validation failed
- 404: not found
- 422: parameter validation (FastAPI default)
```json
{"detail":"..."}
```

## Known limitations
- In-memory storage; restarts reset data.
- Decision logic ignores `rollout_percent`, `weight`, `seed` and returns the first variant.
- `/audits` returns empty list (stub).

## Source
- `docs/api.md`
- `README.md`
