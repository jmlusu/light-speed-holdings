# Open Design Integration

Open Design (`od`) is the render layer for LightSpeed Holdings creative
production: prototypes, live artifacts and dashboards, HTML decks, images, and
HyperFrames motion/video. It is wired through nine `ls-od-*` skills mapped onto
12 existing agents in `company-registry.yaml` (bindings:
`specs/open-design-integration.md`). This document is the single guide for the
integration; the integration package files are
`.opencode/integrations/open-design/{agent-config.yaml,config.json,team.json,README.md}`.

- **Agent source of truth:** `company-registry.yaml` (roster + roles; it has no
  `skills:` blocks — `ls-od-*` bindings are specified in
  `specs/open-design-integration.md`).
- **Design system:** `open-design/design-systems/lightspeed/` (submodule).
- **Render skills:** `.agents/skills/ls-od-*/SKILL.md`.
- **Verified daemon build:** `0.22.1` (integration config declares `0.9.0`).

## 1. Positioning

Open Design is a render layer, not a replacement for the creative stack. The
existing workflow is unchanged:

```
Brief → Creative Director (route) → Production skill → ls-artifact-qa → Deliver
```

The production skill chooses the artifact type; the matching `ls-od-*` skill
drives Open Design to render it. `ls-creative-director` still owns intake and
routing; `ls-artifact-qa` still owns the final APPROVE/FIX gate. No new agents
were added (Option B, 12 agents).

## 2. Prerequisites

- **Node ~24** — Node 22 is not supported; the lockfile and `better-sqlite3` ABI are pinned for 24.
- **pnpm 10.33.2** — `corepack enable` fails with EPERM on Windows; use `npm install -g pnpm@10.33.2`.
- **Visual Studio Build Tools 2022+ with the C++ workload** — `better-sqlite3` has no prebuilt win32/Node 24 binary, so `pnpm install` compiles it (~2 min). This is expected, not a version conflict.
- **WSL2 is the primary supported path**; Windows native is best-effort. In WSL2, a Linux `/usr/bin/od` may shadow the Open Design CLI — keep a WSL-native wrapper earlier in `PATH`.

The daemon's `od` bin (`open-design/apps/daemon/bin/od.mjs`) imports
`open-design/apps/daemon/dist/cli.js` and throws if it is missing. `pnpm install`
runs `scripts/postinstall.mjs`, which builds that dist. If it is still missing,
run `pnpm bootstrap` (or `pnpm --filter @open-design/daemon build`).

## 3. Install And Daemon Lifecycle

```bash
cd open-design
pnpm install          # postinstall builds apps/daemon/dist
pnpm bootstrap        # only if dist is missing
```

`od` is not on `PATH` in this source checkout. Invoke the built CLI directly:

```bash
node open-design/apps/daemon/dist/cli.js version
node open-design/apps/daemon/dist/cli.js daemon status --json
```

Start and inspect the daemon:

```bash
node open-design/apps/daemon/dist/cli.js daemon start --headless --no-open
node open-design/apps/daemon/dist/cli.js daemon status --json
```

- Port defaults to `7456` (`OD_PORT`); host defaults to `127.0.0.1` (`OD_BIND_HOST`).
- `daemon start` is **foreground and blocking**; in a script, launch it detached (e.g. `Start-Process`).
- `daemon status --json` on this machine returned: `version 0.22.1`, `port 7456`,
  `bindHost 127.0.0.1`, `dataDir open-design\.od`, `installedPlugins 460`.
- `daemon stop --daemon-url <url>` shuts it down; `daemon db status|verify|vacuum` manages the SQLite store.

## 4. MCP Wiring (OpenCode)

Run the stdio server:

```bash
od mcp [--daemon-url <url>]
```

Install into an agent config (the launch command is resolved from the running
daemon's `/api/mcp/install-info`):

```bash
od mcp install opencode --print --json   # preview, writes nothing
od mcp install opencode                  # writes the global config
od mcp install opencode --uninstall      # remove
```

- `--print` / `--dry-run` previews without writing; `--json` is machine-readable.
- `--name <name>` sets the server name (default `open-design`).
- For OpenCode, the installer writes the **global** config at
  `~/.config/opencode/opencode.json` under key `mcp` as
  `{ "type": "local", "command": [...], "enabled": true }`. A repo-local
  `opencode.json` (project scope) is **not** written by the installer; hand-edit
  it. Global and project config merge.

**Verified entry** (captured from `od mcp install opencode --print --json` on this
machine; paths are machine-specific):

```json
{
  "mcp": {
    "open-design": {
      "type": "local",
      "command": [
        "C:\\Program Files\\nodejs\\node.exe",
        "C:\\Users\\jmlus\\light-speed-holdings\\open-design\\apps\\daemon\\dist\\cli.js",
        "mcp",
        "--daemon-url",
        "http://127.0.0.1:7456"
      ],
      "enabled": true,
      "environment": {
        "OD_DATA_DIR": "C:\\Users\\jmlus\\light-speed-holdings\\open-design\\.od"
      }
    }
  }
}
```

Prefer running the installer (it resolves the live daemon URL and data dir). If
you hand-edit, do not commit machine-specific absolute paths to the repo — keep
them in the global config.

## 5. Two Catalogues

Open Design ships two separate catalogues. Pick the right one before naming an id.

| Catalogue | Location | API | What it gives |
|---|---|---|---|
| Functional skills | `open-design/skills/` | `/api/skills`, `/api/skills/:id` | Instructions only (design brief, review, brand extraction). |
| Design templates | `open-design/design-templates/` | `/api/design-templates`, `/api/design-templates/:id` | A `SKILL.md` plus assets/references. |

- `--skill` accepts an id from either catalogue (slugs are unique across both).
- `od skill list --json` lists **functional skills only**; a template id returns 404 from `od skill show`.
- `od templates` lists project snapshots, **not** the design-template catalogue. Do not use it for discovery.
- There is no `od design-templates` subcommand.

### Template selection

| Need | Verified ids |
|---|---|
| SaaS landing | `saas-landing`, `kami-landing`, `dating-web` |
| Conversion page | `pricing-page`, `waitlist-page` |
| Desktop product UI | `web-prototype`, `web-prototype-taste-*`, `orbit-general` |
| Mobile flow | `mobile-app`, `mobile-onboarding` |
| Early wireframe | `wireframe-annotated`, `wireframe-greybox`, `wireframe-mobile-flow`, `wireframe-sketch` |
| Analytics | `dashboard`, `live-dashboard`, `trading-analysis-dashboard-template` |
| Social analytics | `social-media-dashboard`, `github-dashboard` |
| Board or investor deck | `html-ppt`, `html-ppt-pitch-deck`, `ib-pitch-book`, `kami-deck` |
| Written report | `finance-report`, `eng-runbook`, `clinical-case-report`, `dcf-valuation` |
| Marketing collateral | `email-marketing`, `social-carousel`, `image-poster` |
| Motion | `video-shortform`, `motion-frames`, `sprite-animation` |

A template may require a design system (`design_system.requires: true`). Attach
one at project creation with `--design-system`; `od run start` does not accept it.

## 6. Render Skills

| Skill | Purpose | Owns |
|---|---|---|
| `ls-od-brand` | Apply/audit LightSpeed brand tokens, type, logo, design-system handoff. | Brand system attachment + brand QA rules |
| `ls-od-catalogue` | Choose a template or functional skill; map a request to a verified id. | Template/skill discovery |
| `ls-od-project` | Create, import, duplicate, inspect projects; attach the design system. | Project lifecycle |
| `ls-od-prototype` | Web, SaaS, mobile, and wireframe prototypes. | Prototype rendering |
| `ls-od-deck` | HTML presentation decks (`html-ppt`, `guizang-ppt`, `kami-deck`, `ib-pitch-book`, …). | Deck rendering + speaker notes |
| `ls-od-image` | Brand-consistent images, posters, social assets via the media pipeline. | Image generation + budget gate |
| `ls-od-video` | HyperFrames-first motion graphics and short video. | Scaffold, render loop, house style |
| `ls-od-live-artifact` | Live artifacts and dashboards with data wiring and refresh. | Data wiring + states |
| `ls-od-runtime` | Install, daemon lifecycle, SQLite, MCP wiring, troubleshooting. | Runtime operations |

## 7. Agent Bindings

The `ls-od-*` bindings are specified in `specs/open-design-integration.md`;
`company-registry.yaml` has no `skills:` field (its schema covers roster and
roles only). The integration package does not mirror them: its `team.json`
describes a different team (generic `ls-*` skills, an `artifact-qa-reviewer`
support agent, no `ls-od-*` entries).

| Agent | Role | `ls-od-*` skills |
|---|---|---|
| `creative_director` | orchestrator | runtime, catalogue, brand, project, prototype, live-artifact, deck, image, video |
| `cmo` | executive | runtime, catalogue, deck |
| `marketing_owner` | production | catalogue, deck, image |
| `social_media_manager` | production | image, deck |
| `technical_documentation_lead` | production | live-artifact, deck |
| `product_marketing_manager` | production | deck, image |
| `product_designer` | production | brand, prototype, live-artifact |
| `lead_frontend` | production | prototype, live-artifact |
| `senior_frontend_engineer` | production | prototype |
| `market_analyst` | production | live-artifact, deck |
| `content_creator` | production | image, video, deck |
| `media_generation_owner` | production | runtime, image, video |

`dashboard_owner` and `business_intelligence_engineer` have no `ls-od-*`
bindings. There is no separate artifact-qa-reviewer agent; the
`creative_director` runs `ls-artifact-qa`.

## 8. Workflows

### Prototype

```bash
od project create --name "Landing page" --skill web-prototype --design-system lightspeed
od run start --project <projectId> --skill web-prototype --prompt-file ./brief.md --agent opencode --json
od run watch <runId>
```

The daemon's `od run` surface is `start`, `redesign`, `watch`, `cancel`, and
`steer`; there is no `od run <scenario>` positional form. `--design-system` is a
project-creation flag, not a run flag.

### Deck

```bash
od run start --project <projectId> --skill html-ppt --json
```

`guizang-ppt` is the magazine deck (its frontmatter `name` is `magazine-web-ppt`,
but the folder and CLI id are `guizang-ppt`). For native PowerPoint, use
`ls-presentation-design` instead.

### Image

```bash
"$OD_NODE_BIN" "$OD_BIN" media generate \
  --project "$OD_PROJECT_ID" --surface image --model "gpt-image-2" \
  --aspect "1:1" --quality "high" --output "hero-poster.png" --prompt "<prompt>"
"$OD_NODE_BIN" "$OD_BIN" media wait "<taskId>" --since "<nextSince>"
```

**Budget gate:** `od media generate` has no dry-run/print flag; it submits a paid
job immediately. Confirm count, model, aspect, and variations with the human
first. Default to one image per request.

### Video

HyperFrames is the default engine; the composition lives under
`.hyperframes-cache/<id>/`, and only the finished `.mp4` belongs in the project root.

```bash
"$OD_NODE_BIN" "$OD_BIN" media scaffold --project "$OD_PROJECT_ID" --composition-dir ".hyperframes-cache/<slug>"
"$OD_NODE_BIN" "$OD_BIN" media generate --project "$OD_PROJECT_ID" --surface video \
  --model hyperframes-html --composition-dir ".hyperframes-cache/<slug>" --output "<name>.mp4"
"$OD_NODE_BIN" "$OD_BIN" media wait "<taskId>" --since "<nextSince>"
```

Do not run `hyperframes render` yourself; the daemon owns rendering. Read project
metadata first: `videoModel`, `videoLength`, and `videoAspect` are locked.

### Live artifact

```bash
od run start --project <projectId> --skill live-dashboard --inputs '{"workspace_name":"Operations","connector":"mock"}' --json
od run watch <runId>
```

Connectors: `notion|linear|stripe|posthog|mock`; `refresh_seconds` 10–300,
`stale_after_seconds` 30–600, `kpi_count` 2/4/6. Never invent a live endpoint or
store credentials in persisted JSON.

## 9. Brand System

- LightSpeed design system: `open-design/design-systems/lightspeed/DESIGN.md`.
- Attach at project creation: `od project create --name "<name>" --design-system lightspeed`.
- Confirm with `od design-systems list --json`; `--design-system` is a
  project-creation and import flag, not a run flag.
- Canonical brand files: `brand/tokens/brand-tokens.json` and
  `brand/CANONICAL_SOURCES.md`. `brand/**` is canonical; never hand-edit
  `static/brand/**` or `public/brand/**` mirrors — sync them with
  `pwsh scripts/build/sync-brand.ps1`.

Brand tokens: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, morning-mist
`#F7F8F9`, deep-mineral `#121518`, white `#FFFFFF`, grey-dark `#6B7280`. Type is
Arial; spacing is a 4px base scale. Full token table and logo rules:
`.agents/skills/ls-od-brand/SKILL.md`.

## 10. Output Locations

Projects write under `output/design` (`baseDir` in the integration config):

| Artifact | Path |
|---|---|
| Websites / prototypes | `output/design/websites` |
| Decks | `output/design/decks` |
| Documents | `output/design/documents` |
| Diagrams | `output/design/diagrams` |
| Infographics | `output/design/infographics` |
| Ads | `output/design/ads` |

## 11. Safety Boundaries

- Never invent `--skill` ids, CLI flags, or commands; run `od <cmd> --help` first.
- Never call `od media generate` without an approved budget.
- Never hand-edit a project's Design Files while a run is active.
- Never store credentials, tokens, or raw provider responses in persisted JSON.
- Never run `hyperframes render` directly; the daemon owns rendering.
- Never treat functional skills and design templates as interchangeable catalogues.
- `ls-artifact-qa` runs last; do not deliver on a FIX verdict.

## 12. Troubleshooting

| Symptom | Fix |
|---|---|
| `OpenDesign daemon dist entry not found at ...\dist\cli.js` | Run `pnpm bootstrap` or `pnpm --filter @open-design/daemon build` in `open-design` |
| `corepack enable` → EPERM | `npm install -g pnpm@10.33.2` |
| node-gyp / MSB error building `better-sqlite3` | Install VS Build Tools 2022+ with the C++ workload, or use WSL2 |
| `daemon start` appears hung | It is blocking by design; check `daemon status --json` from another shell or launch detached |
| Port 7456 in use / stale daemon | `daemon status --json`, then `daemon stop`, then start again |
| `od` in WSL runs the GNU coreutils tool | Put a WSL-native Open Design wrapper earlier in `PATH` |
| `od skill show <template-id>` → 404 | Templates resolve through `/api/design-templates`, not `/api/skills` |

## 13. Source Of Truth

| Concern | Source |
|---|---|
| Agent roster | `company-registry.yaml` |
| Skill bindings | `specs/open-design-integration.md` |
| Integration settings | `.opencode/integrations/open-design/{config.json,agent-config.yaml,team.json}` |
| Render procedures | `.agents/skills/ls-od-*/SKILL.md` |
| Brand tokens | `brand/tokens/brand-tokens.json` + `brand/guidelines/brand-guidelines.md` |
| Design system | `open-design/design-systems/lightspeed/` |
| CLI surface | `open-design/apps/daemon/src/cli.ts` (`SUBCOMMAND_MAP`) |
