# Approved Vendors — Skill Third-Party Transmission

**Version:** 1.0
**Date:** 2026-09-23
**Owner:** Jack Mlusu (Human CEO = CISO of record)
**Related:** [`SKILL_CURATION_POLICY.md`](SKILL_CURATION_POLICY.md) § Skill Third-Party Transmission Ban · `AGENTS.md` §7 / §9.2

**Rule summary:** A skill may only send local data to a host listed below. Default exception window: **90 days** from `approved_at`. Renewal requires CEO/CISO re-record before expiry. Unknown hosts → stop skill, report to CEO.

---

## Allow-list (active or historical)

| Vendor | Endpoints (examples) | What is sent | Auth | Approved | Window ends | Status |
|--------|----------------------|--------------|------|----------|-------------|--------|
| **cmem.ai** | cmem.ai | Memory narratives + full prompts (claude-mem cloud sync) | account credentials / API | 2026-09-23 | 2026-12-22 | **RETIRED with skills** — do not reinstall |
| **0x0.st** | 0x0.st | Public screenshot/image uploads (anyone with URL) | none / short-lived URL | 2026-09-23 | 2026-12-22 | **Active allow-list** — used by `before-and-after` / evidence flows; treat uploads as public |
| **Telegram** | api.telegram.org | Chat ID + message text; bot token in headers (claude-mem mode creator) | bot token | 2026-09-23 | 2026-12-22 | **RETIRED with skills** — do not reinstall |
| **Google NotebookLM** | notebooklm.google.com | Uploaded source documents under Google account | Google auth | 2026-09-23 | 2026-12-22 | **RETIRED with skills** |
| **Workers (wowerpoint)** | wowerpoint-api.*.workers.dev | Multipart PDFs + Bearer token (claude-mem wowerpoint) | Bearer | 2026-09-23 | 2026-12-22 | **RETIRED with skills** |
| **kie.ai** | api.kie.ai · kieai.redpandaai.co | Base64 images + prompts (scroll-craft image gen) | `KIE_AI_API_KEY` | 2026-09-23 | 2026-12-22 | **RETIRED with skills** — do not reinstall |
| **Greptile** | greptile | PR bodies, diffs, comments, repo content (greploop review) | GitHub/Greptile token | 2026-09-23 | 2026-12-22 | **RETIRED with skills** — do not reinstall |

**Tier B (public research — generally OK, disclose in skill description):** webfetch to public docs, arXiv/OpenAlex/CrossRef/PubMed, Kroki diagram fallback, skills.sh / marketplace discovery (`find-skills`, `global-chat-agent-discovery`, `using-agent-skills`). Still subject to stop-and-report if they unexpectedly POST local project files.

**Not exfiltration (local-only CDN loads for assets):** Google Fonts / sheetjs CDN script loads used by `skill-creator` and similar — document if behavior changes.

---

## Retired skill families (deleted 2026-09-23)

| Family | Locations purged |
|--------|------------------|
| `claude-mem-*` (20 skills) | project `.agents\skills\`, global `~\.agents\skills\`, local `~\.claude-mem\`, plugin cache `~\.claude\plugins\cache\thedotmack\claude-mem\` |
| `scroll-craft` | project `.agents\skills\`, project `.opencode\skills\`, global `~\.agents\skills\`, workspace `scrollcraft\` (incl. `.env`) |
| `greploop`, `greploop-apps` | global `~\.agents\skills\` |

Git snapshot before purge: `a179b62e`.

---

## Exception procedure

1. Open a new row (or renew) with `approved_at`, data class, host, auth, and `window_end` (≤90 days).
2. CEO records approval (acting as CISO of record for Tier A).
3. Install skill only after the row is active.
4. On expiry without renewal → remove skill; treat as unauthorized.

## Change log

| Date | Change | Author |
|------|--------|--------|
| 2026-09-23 | Initial allow-list; retire claude-mem / scroll-craft / greploop | CEO / Chief of Staff |
