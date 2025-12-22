# Plan - ai/backend/engineer-02

## Objective
- Implement backend business logic to replace the mock store while keeping the API contract stable.

## Deliverables
- Domain rules + validation for Feature/Experiment/Variant (control required, weights sum=100, rollout 0..100).
- Decision engine (status priority, rollout gate, weighted assignment, stable bucket hash).
- Service/repo layer with a persistence seam to swap in behind existing APIs.
- Audit/decision/exposure logging hooks (MVP scope).

## Milestones
- [M1] Confirm targeting format, bucketing key, and idempotency policy with owner.
- [M2] Implement domain validation and decision flow.
- [M3] Integrate services with API routes while keeping contract unchanged.
- [M4] Wire audit/decision/exposure logging and kill-switch handling.

## Dependencies
- Targeting format + bucketing key decision.
- Idempotency/anonymous user policy confirmation.
- Mock API contract from ai/backend/engineer-01.

## Risks
- Contract drift between mock and business logic.
- Late targeting format changes impacting decision engine.

## Plan
- Sync with ai/backend/engineer-01 on API schemas and error formats.
- Build domain model validation + decision logic.
- Add repository/service layer and wire to routers.
- Add audit/decision/exposure logging.
