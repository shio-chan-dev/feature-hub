---
name: feature-hub-api
description: Use this skill to help customers integrate with Feature Hub (feature flags/experiments) and call the decision API (/decisions), including request/response shapes and decision behavior.
---

# Feature Hub API Integration

## Workflow
1. Confirm the environment and base URL. Default dev base URL is `http://localhost:6789`; if the service runs on another port (e.g., 8000), use that or set `API_BASE_URL`.
2. Confirm authentication (currently none) and required headers (`Content-Type: application/json`).
3. If the user asks about "decision", clarify whether they mean the API decision endpoint (`POST /decisions`) or a project governance decision log.
4. For API decisions, gather required inputs: `request_id`, `feature_key`, `user_id`, and optional `context`.
5. Explain prerequisites and typical flow: create feature → create experiment → add variants → set feature to `experiment` with `active_experiment_id` → set experiment to `running` → call `/decisions`.
6. Provide a concrete request example and expected response fields; call out the `reason` values.
7. Highlight current limitations (in-memory storage, decision logic picks first variant, audits are stubbed).
8. Link to references for full endpoint details.

## Required Inputs
- Base URL and environment (dev/staging/prod).
- Authentication method (if added later).
- Feature key, user id, request id, and context for a decision call.
- Rate limits or usage constraints (if any).

## Output Format
## Summary
## Decision Request (JSON + curl)
## Expected Response (fields + example)
## Notes / Limitations
## Next Steps

## Guardrails
- Do not invent endpoints or behavior. If docs conflict, flag and ask.
- Do not assume analytics or metrics collection; this service only returns decisions.
- Use TODOs for missing inputs and confirm with the user.
- Avoid proposing data mutations without explicit user approval.

## References
- `docs/api.md`
- `skills/feature-hub-api/references/api.md`
- `skills/feature-hub-api/references/decision.md`
