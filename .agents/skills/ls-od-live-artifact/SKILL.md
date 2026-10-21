---
name: ls-od-live-artifact
description: "Build live artifacts, dashboards, and interactive data views with Open Design, including data wiring, refresh behavior, and QA handoff. Trigger on: 'od live artifact', 'open design dashboard', 'live dashboard od', 'interactive artifact', 'od dashboard'."
---

# Open Design Live Artifacts

Use Open Design (OD) templates to produce refreshable, auditable artifacts. A live artifact is not a static mockup: its presentation is authored once and its data can be refreshed without rebuilding the design.

## When To Use

- A view must stay useful after first render: live dashboard, refreshable report, synced status page, auditable data view.
- Data provenance, last-updated time, or refresh cadence matters to the audience.
- Connector-backed data (Notion, Linear, Stripe, PostHog) or project-local JSON feeds the display.
- A static one-off page or image is requested instead — skip this skill and use a static artifact workflow.

If refresh intent is ambiguous, ask one question before authoring: "Should this refresh from data, or is it a static snapshot?"

## Template Families

Read the template's own `SKILL.md` before running it. Verified contracts:

| Template id | Scenario | Use |
|---|---|---|
| `live-artifact` | `live` | Refreshable data-backed artifact. Source files: `template.html`, `data.json`, `artifact.json`, `provenance.json`; `index.html` is derived by the daemon. |
| `live-dashboard` | `operation` | High-fidelity team/ops dashboard. Inputs include `workspace_name`, `page_title`, `connector` (`notion`, `linear`, `stripe`, `posthog`, `mock`), `refresh_seconds` (10–300, default 30), `stale_after_seconds` (30–600, default 90), `kpi_count` (2/4/6), `include_activity_feed`. |

Also present under `open-design/design-templates/`, but not validated for this workflow: `dashboard`, `github-dashboard`, `kanban-board`, `flowai-live-dashboard-template`, `social-media-dashboard`, `trading-analysis-dashboard-template`, `worker-visualizer`, `orbit-general`, `orbit-github`, `orbit-gmail`, `orbit-linear`, `orbit-notion`. Do not cite an id that is not in this list, and read its `SKILL.md` before use.

Load `ls-design-system` for brand tokens. OD templates still render LightSpeed navy `#070A40`, red `#E63946`, cyan `#00BFFF`, Arial, and the 4px spacing scale.

## Brief Structure

Capture these before authoring:

| Field | Content |
|---|---|
| Audience | Who reads it and at what cadence |
| Decision | The one decision or action the view supports |
| Metrics | Each KPI, formula, unit, owner, and target |
| Data source | Connector, endpoint, or local file — confirmed, not assumed |
| Refresh | Cadence, stale threshold, timezone of timestamps |
| Filters | Dimensions the reader may change, and defaults |
| States | Empty, loading, partial, error, stale |
| Export | Screenshot, PDF, or shared link requirement |

Reject vague metrics ("engagement", "performance") until a definition exists. If a metric cannot be computed from the available source, label it a demo value or remove it.

## Data Wiring

Classify every data source explicitly:

| Class | Contract |
|---|---|
| Static JSON | Authored `data.json`; real values, compact and preview-oriented |
| Fetched endpoint | Only when a real endpoint is supplied or confirmed; record URL, auth boundary, and shape |
| Computed demo | Derived sample values; label as demo in the UI and provenance |

Never invent a live endpoint, connector account, or data field. Never store credentials, tokens, cookies, auth headers, raw provider responses, or secret-like keys (`raw`, `payload`, `body`, `headers`, `token`, `secret`, `credential`, `password`) in persisted JSON.

Expected shape (adapt, do not invent fields the source lacks):

```json
{
  "generated_at": "2026-10-20T12:00:00Z",
  "kpis": [{ "label": "Open deals", "value": 42, "delta": "+3", "status": "ok" }],
  "activity": [{ "actor": "Sales", "action": "Closed Q3 renewal", "at": "2026-10-20T09:14:00Z" }]
}
```

Binding rules for `live-artifact` (`html_template_v1`):

- Scalars: `{{data.kpis.0.value}}`; paths start at `data`, numeric indexes allowed.
- Lists: `data-od-repeat="item in data.kpis"`, then `{{item.label}}` inside the element.
- One repeat level only; nested repeats, conditionals, filters, helpers, and raw/triple-brace interpolation fail.
- Every binding must resolve to a string or number; scripts are stripped from previews.

Connector work goes through daemon wrappers, not provider APIs:

```bash
"$OD_NODE_BIN" "$OD_BIN" tools connectors list --format compact
"$OD_NODE_BIN" "$OD_BIN" tools connectors execute --connector "$CONNECTOR_ID" --tool "$TOOL_NAME" --input input.json
```

Persist only normalized fields plus non-sensitive references (`connectorId`, `toolName`, `accountLabel`). If a connector is not connected, tell the user to connect it in the UI instead of requesting secrets.

## Refresh And States

- Set cadence from the brief: `refresh_seconds` and `stale_after_seconds` for `live-dashboard`; an explicit refresh contract for `live-artifact`.
- Always show "Last updated" with a timezone, and a stale badge once the threshold passes.
- Loading: skeleton or prior data with a progress indicator — never a blank flash.
- Empty: state what is missing and which source returned nothing.
- Error: banner with the failing source, last successful timestamp, and a retry control; keep the last good data visible.
- Partial: mark the affected KPI or panel rather than failing the whole view.
- Never present demo data as live. Never claim freshness that the data cannot support.

## Commands

The run scenario comes from the template's `od.scenario`; there is no `od run <scenario>` subcommand.

```bash
od run start --project <projectId> --skill live-dashboard --inputs '{"workspace_name":"Operations","connector":"mock"}' --json
od run start --project <projectId> --skill live-artifact --json --follow
od run watch <runId>
od run redesign --path <folder> --message "<change request>"
```

- `--json` returns machine-readable output; `--follow` streams an active run.
- `--inputs` takes a JSON object matching the template's declared inputs.
- `od run watch <runId>` attaches to a run started earlier.
- `--design-system` is attached at project creation, not on `od run`; `od run redesign` takes `--path`, not a run ID.

Register or update a `live-artifact` only through the daemon wrapper; `projectId` is derived from the token and must not be added:

```bash
"$OD_NODE_BIN" "$OD_BIN" tools live-artifacts create --input artifact.json
"$OD_NODE_BIN" "$OD_BIN" tools live-artifacts list --format compact
"$OD_NODE_BIN" "$OD_BIN" tools live-artifacts update --artifact-id "$ARTIFACT_ID" --input artifact.json
```

## Accessibility

- Full keyboard operation for filters, tabs, retry, and row expansion; visible focus states.
- Data tables use real `<table>`, `<th scope>`, and captions; charts carry a text summary or accessible table.
- Contrast meets WCAG AA: red `#E63946` is an accent, not body text on navy; do not set small text in red on navy.
- Never encode status by color alone — pair with text or an icon and label.
- Refresh must not steal focus; announce updates with a polite live region.
- Respect `prefers-reduced-motion` for refresh and chart animations.

## Handoff To QA

Provide `ls-artifact-qa` with:

- Artifact id, run id, and output paths (`index.html`, `template.html`, `data.json`, `artifact.json`, `provenance.json`).
- Data assumptions: source class, connector or endpoint, refresh cadence, demo labels.
- States to exercise: loading, empty, error, stale, partial.
- Screenshots at the target viewport plus one narrow viewport.
- Known gaps: unverified metrics, unavailable connectors, omitted template ids.

QA runs last; do not deliver a live artifact without its visual, brand, UX, accessibility, and content pass.

## Verification

- [ ] Template id exists in the verified list and its `SKILL.md` was read.
- [ ] Brief fields are complete; every KPI has a definition and unit.
- [ ] `data.json` values match the displayed values; demo data is labeled.
- [ ] All `{{…}}` bindings resolve; no visible tokens or unresolved repeats.
- [ ] Stale badge fires at the configured threshold; last-updated time is correct.
- [ ] Loading, empty, error, and partial states render without layout collapse.
- [ ] No credentials, raw payloads, or forbidden keys in any persisted JSON.
- [ ] Keyboard pass, table semantics, contrast, and non-color status cues verified.
- [ ] Brand tokens and official logo assets applied via `ls-design-system`.
- [ ] `ls-artifact-qa` returned APPROVE.
