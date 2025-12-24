# Feature Hub Frontend Handoff

This document helps a new frontend engineer take over the SvelteKit UI quickly.

## Project goals
- Provide a Feature-first console for managing features, experiments, variants, audits, and decisions.
- Keep UI logic thin and aligned to the API contract in `docs/api.md`.
- Support English and Chinese UI labels, with a header language switcher.

## Tech stack
- SvelteKit (Svelte 5 runes mode)
- Vite
- Tailwind plugin present, but UI is mostly custom CSS variables in `layout.css`.

## Quick start
1) Install deps
   - `npm install` (run inside `svelteapp/`)
2) Start the API
   - Default: `http://localhost:6789` (see `API_BASE_URL` below)
3) Run the UI
   - `npm run dev` then open the shown local URL

## Routes and pages
- `/` Feature dashboard
  - Create feature
  - List features
  - Link to detail and decisions
- `/features/[featureId]` Feature detail
  - Update feature status and active experiment
  - Create/update experiments
  - View/add variants
  - Variants load via `?experiment=<id>`
- `/audits` Audit log (stub)
  - Query by `feature_id`, optional `limit` and `cursor`
- `/decisions` Decision playground
  - Calls `/decisions` to preview variant selection
- `/docs` In-app usage guide
  - Includes service integration notes and a request/response example
- `/set-locale` POST-only endpoint for language switching

## Data flow
- All API calls are server-side via `+page.server.ts` (SvelteKit actions and loads).
- `apiRequest` in `svelteapp/src/lib/server/api.ts` is the single API client.
- Form actions return `form` data used by pages to show success/error banners.
- Layout SSR provides `data.locale` to every page.

## Locale and i18n
- Dictionary lives in `svelteapp/src/lib/i18n.ts`.
- Locale is resolved in `svelteapp/src/routes/+layout.server.ts`:
  - Cookie `locale` if set
  - Otherwise `Accept-Language` contains `zh`
  - Else `en`
- The header language switcher submits a form to `/set-locale`.
- Pages use `data.locale` from layout and build `copy` via `translations`.

To add a new language:
1) Add new locale to `locales`, `localeLabels`, and `translations`.
2) Update `resolveLocale` in `+layout.server.ts` to detect it.
3) Verify all pages render with the new locale.

## Svelte 5 runes rules
- Use `$props()`, `$derived`, `$effect`.
- Do not use legacy `$:` reactive statements.
- Avoid deprecated `on:` event directives; use `onclick`, `onchange`, etc.

## Configuration
- API base URL is set in `svelteapp/src/lib/server/api.ts`:
  - `API_BASE_URL` env var overrides default `http://localhost:6789`.
- Fonts are loaded via Google Fonts in `+layout.svelte`.

## Styling
- Global styles live in `svelteapp/src/routes/layout.css`.
- The theme uses CSS variables for colors, spacing, and typography.
- Add new component styles here or in component-level styles if needed.

## Testing
- Unit: `npm run test:unit`
- E2E: `npm run test:e2e`
- Lint: `npm run lint`

## Known limitations (MVP)
- Decision logic currently returns the first variant (weights/rollout TBD).
- Audit endpoint returns empty list (stub).
- Storage is in-memory; restarts reset data.

## Common tasks
- Add a new field in Feature/Experiment/Variant:
  1) Update `svelteapp/src/lib/types.ts`.
  2) Update the relevant server actions/loads.
  3) Update UI and translations.
- Add a new page:
  1) Create `+page.server.ts` (load/actions).
  2) Create `+page.svelte` using runes.
  3) Add nav item to `AppHeader` if needed.

## File map (core)
- `svelteapp/src/lib/server/api.ts` API client
- `svelteapp/src/lib/i18n.ts` translations
- `svelteapp/src/lib/components/AppHeader.svelte` header + locale switcher
- `svelteapp/src/routes/+layout.svelte` layout + head tags
- `svelteapp/src/routes/+layout.server.ts` locale load
- `svelteapp/src/routes/docs/+page.svelte` in-app docs

## Contact points
- API contract: `docs/api.md`
- Collaboration log: `agent-collab/channels/dept-frontend.md`
