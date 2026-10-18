# Reverse Engineer Anything (REA) — Shared Capabilities Brief

**Date:** 2026-10-17
**Prepared by:** Agentic Research Lead (Pharos)
**Purpose:** Single source of truth for downstream feasibility analysis agents evaluating `morluto/rea`. All agents cite this document rather than re-fetching primary sources. Facts below were verified against primary sources on 2026-10-17; anything not verified is explicitly marked **UNVERIFIED**.

## Sources

| # | Source | URL |
|---|--------|-----|
| S1 | GitHub repository (main) | https://github.com/morluto/rea |
| S2 | README.md (main branch) | https://raw.githubusercontent.com/morluto/rea/main/README.md |
| S3 | LICENSE (MIT) | https://raw.githubusercontent.com/morluto/rea/main/LICENSE |
| S4 | SECURITY.md | https://raw.githubusercontent.com/morluto/rea/main/SECURITY.md |
| S5 | THIRD_PARTY_NOTICES.md | https://raw.githubusercontent.com/morluto/rea/main/THIRD_PARTY_NOTICES.md |
| S6 | docs/cli.md | https://raw.githubusercontent.com/morluto/rea/main/docs/cli.md |
| S7 | docs/mcp-contracts.md | https://raw.githubusercontent.com/morluto/rea/main/docs/mcp-contracts.md |
| S8 | docs/installation.md | https://raw.githubusercontent.com/morluto/rea/main/docs/installation.md |
| S9 | docs/windows-ghidra-p0.md | https://raw.githubusercontent.com/morluto/rea/main/docs/windows-ghidra-p0.md |
| S10 | docs/ida-provider.md | https://raw.githubusercontent.com/morluto/rea/main/docs/ida-provider.md |
| S11 | docs/kuna-provider.md | https://raw.githubusercontent.com/morluto/rea/main/docs/kuna-provider.md |
| S12 | docs/javascript-application-workflows.md | https://raw.githubusercontent.com/morluto/rea/main/docs/javascript-application-workflows.md |
| S13 | docs/javascript-artifact-reconstruction.md | https://raw.githubusercontent.com/morluto/rea/main/docs/javascript-artifact-reconstruction.md |
| S14 | GitHub API — repository metadata | https://api.github.com/repos/morluto/rea |
| S15 | GitHub API — releases | https://api.github.com/repos/morluto/rea/releases |
| S16 | GitHub API — top contributors | https://api.github.com/repos/morluto/rea/contributors |
| S17 | npm package `rea-agents` | https://www.npmjs.com/package/rea-agents |

**Ecosystem sources (secondary, for §6 only):** reamcp.dev alternatives page; rea-reverse.com comparison (2026-10-13); reversedwithai.com comparison; ai.dosa.dev comparison (2026-10-15); plus upstream repos `LaurieWired/GhidraMCP`, `mrexodia/ida-pro-mcp`, `HexRaysSA/ida-mcp`, `radareorg/radare2-mcp`, `fosdickio/binary_ninja_mcp`, `jtsylve/re-mcp`. Star counts and release dates from these secondary pages were **not independently re-verified** except where noted.

---

## 1. Capability Inventory

**What it is:** REA is a local MCP server **and** CLI (`rea`) that gives an AI agent a uniform investigation surface over many target types. The agent asks questions via MCP; REA inspects/traces the target using per-target analysis engines; it returns findings wrapped in an Evidence record with stated limitations (S1, S2, S7).

**Install / entry points (verified):**
- npm package: `rea-agents`; agent setup: `npx rea-agents setup` (interactive, previews config changes, requires approval before applying) (S2, S8).
- Global CLI: `npm install --global rea-agents` → `rea` command; one-shot: `npx -y rea-agents@latest <cmd>` (S2, S6).
- Supported agent auto-registration: Claude Code, Codex, Cursor, Gemini CLI, Grok Build + others via manual MCP registration (S2, S8). Note: README's IMPORTANT banner warns that look-alike repos/READMEs are not official download channels (S2).

**Target coverage (README "What you can analyze" table, S2):** Node.js 22.x (≥22.19), 24.x (≥24.11), or 26+ required universally; then per-target:

| Target | Returns | Extra requirements |
|---|---|---|
| Native binaries | Pseudocode, assembly, strings, symbols, calls, references | Hopper, Ghidra, or IDA (an existing install; setup can install Hopper with approval) |
| Offline ELF layout | Sections, segments, symbols/relocations, static mitigation candidates | caller-supplied pwntools, Linux x64 |
| Go binaries | Embedded compiler version, modules, replacements, build settings | built-in static ELF/PE/thin Mach-O parsing; no Go toolchain needed |
| Rust binaries | cargo-auditable crate names/versions/sources/dependency edges | built-in static parsing |
| WASM artifacts | Validation, sections, exact import/export WAT forms, decoded WAT | caller-supplied WABT 1.0.42 |
| EVM bytecode | Dispatch selectors, byte offsets, inferred arguments, mutability | local raw/hex carrier, Linux x64 |
| SQLite databases | Tables, columns, indexes, views, triggers, sample rows | Node.js 24.x ≥24.15 or 26+ with native SQLite |
| Recorded Linux crashes | Registers/signals per recorded thread, optional mapping candidates | pwntools; optional GDB/pwndbg |
| JavaScript / Electron | Modules, imports, source maps, routes, IPC + native add-on relationships | **no native engine required** (static analysis never executes the app) |
| Websites | Page structure, scripts, network observations, requested screenshots | Chrome-family browser |
| Saved network captures | Requests, responses, exposed payloads, source locations | HAR or Fiddler SAZ; mitmdump on Linux for live mitmproxy |
| .NET assemblies | Metadata, CIL instructions, native deps, build comparisons | none (static only; PE/CLI read without loading/executing the assembly) |
| Android APKs | Manifest declarations, classes, decompiled methods, references | headless JADX + full JDK (Linux/macOS/Windows x64) |
| Android devices | Devices, packages, processes, logs, dumps, screenshots, APK/file transfers | caller-supplied adb |
| JEB projects | Engine-backed project units, artifact digests, type/method pseudo-code | caller-started JEB client MCP, `REA_JEB_MCP_URL` |
| Android resources | Decoded manifest, string tables, locales, version facts | caller-supplied Apktool |
| Flutter apps | Dart snapshot hash, per-ABI library digests, engine build provenance | none (static APK parsing) |
| Firmware | Regions, extraction results, native-analysis handoffs | Binwalk/Unblob, **Linux only** |
| Recorded packets | Selected fields, repeated values, filters, decode-as rules | Linux: TShark 4.x + prlimit |
| Packet summaries | Endpoints, DNS, TLS SNI, protocol distribution, HTTP requests | caller-supplied tshark + capinfos (Linux-verified) |
| Recorded logic signals | Decoder annotations, sample ranges, diagnostics | Linux: sigrok-cli 0.7.2 + prlimit |
| Packages / Apple resources | File inventories, digests, plists, bundle anatomy, extracted resources | none |
| Process behavior | Terminal output, interactions, exit + filesystem observations, run comparisons | Linux/macOS with native PTY (runtime capture executes the target) |

Also documented: 16-bit DOS analysis via Ghidra (docs/ghidra-dos.md), Ghidra MIPS/PPC/RISC-V/PSP/NativeAOT variants, Harmony instrumentation, Apple applications, web runtime/source-location tracing, offline objdump/Rizin inspection (docs/reverse-engineering-tools.md) — full docs listing at docs/ (verified via GitHub contents API).

**Native analysis providers (verified):**
- **Hopper** — REA starts it on demand; setup can install it with approval; first-run macOS dialog may require demo-vs-license choice (S2, S8).
- **Ghidra** — uses existing install; **ephemeral project per target** (imported into a temporary database, deleted on close; executable bytes never modified; naming edits discarded) (S9, ecosystem comparison).
- **IDA** — REA adapts the upstream `mrexodia/ida-pro-mcp` server; configured via `REA_IDA_MCP_CONFIG` JSON; selected via `REA_ANALYSIS_PROVIDER=ida`, `--provider ida`, or MCP `open_binary.provider_id`; lifecycle modes `attached` (legacy GUI tool names; upstream 2.0.0 renamed tools → fails closed) and `headless` (database-supervisor API; upstream snapshot `c133c385` has `idb_close`/`idb_open`/`idb_list`); input SHA-256 checked against IDA's recorded hash. REA does not install or license IDA (S10).
- **Kuna** — Apache-2.0 decompiler (github.com/Noelo-Lab/kuna), single `kuna` executable, user-supplied; verified with Kuna 1.833 (other versions reported unverified by `rea doctor`); static only; `REA_KUNA_COMMAND` required, `REA_KUNA_CACHE_DIR` optional; `--provider kuna`; when two providers are configured for a target, `auto` reports `ambiguous` (S11).

**Key MCP tools (verified, non-exhaustive):** `analyze_function`, `compare_functions`, `inspect_artifact`, `compare_artifacts`, `get_evidence_bundle`, `analyze_javascript_application`, `inspect_analysis_view`, `trace_application_feature`, `trace_javascript_semantics`, `compare_application_versions`, `compare_source_to_bundle`, `compare_javascript_export_shapes`, `reconcile_javascript_runtime`, `inspect_wasm_artifact` (S7, S12, S13). A generated full tool catalog exists at docs/mcp-contracts.md#generated-catalog. Tool count: **UNVERIFIED** (not fetched this session).

**CLI surface (verified):** `rea analyze PATH` (generic — picks the JS workflow for directories and `.asar` when no `--provider`/`--snapshot` given), `rea analyze-javascript-application <dir> --json`, `rea update`, `rea doctor`, plus native commands documented in docs/cli.md. JSON output goes to stdout; `rea_progress` JSON lines on stderr (S6, S13).

**Explicit non-goals (verified):** Static JS and .NET inspection never execute the target. Runtime capture *does* run/interact with the target under the operator's user permissions. REA is not a decompiler itself — it drives existing engines. (S2; corroborated by secondary sources.)

---

## 2. Prerequisites & Licensing

| Component | License / Cost | Notes |
|---|---|---|
| REA itself (`rea-agents` npm) | **MIT**, Copyright (c) 2026 morluto | Free (S3) |
| Third-party deps in REA |各自 retain own licenses | THIRD_PARTY_NOTICES.md inventories locked npm graph, derived code/assets, separately obtained engines; "listing ≠ bundled" (S5) |
| Node.js | 22.x ≥22.19 / 24.x ≥24.11 / 26+ + npm | Hard prerequisite (S2) |
| Ghidra | Apache-2.0, **free** (NSA Research Directorate) | User installs; REA does not install it |
| Hopper | Commercial (demo mode available) | Setup may install with approval; licensing is the user's responsibility |
| IDA Pro / Hex-Rays | Commercial (secondary sources: IDA Home from $365/yr non-commercial; Pro from €1,099/yr; IDA Free lacks idalib) | **Prices UNVERIFIED against Hex-Rays pricing page this session** |
| Kuna | Apache-2.0, free | User-supplied executable (S11) |
| JEB | Commercial | User-started client (S2) |
| JADX / Apktool / Binwalk / Unblob / TShark / sigrok-cli / WABT / pwntools / adb / browser | Mixed OSS, caller-supplied | Per-target requirements above |

**Licensing rule (README, S2):** "You must legally obtain and be authorized to use commercial tools… REA grants no tool license, key, or activation entitlement. … Cracked copies, stolen keys, unauthorized key sharing, and bypassing license restrictions are not authorized."

**Responsible use (README Disclaimer, S2):** REA is positioned for lawful research, education, interoperability, software preservation, and analysis of software you own or are authorized to examine; full text in DISCLAIMER.md (**DISCLAIMER.md contents not fetched — UNVERIFIED beyond the README summary**).

**Platform prerequisites (verified):**
- Linux: procps-compatible `ps` on PATH needed for Ghidra/JADX/firmware launches and static JS/Electron analysis (ownership checks) (S2).
- Windows: native analysis supported; Ghidra on Windows is **experimental P0** (see §3/§5) (S9).
- macOS: Hopper first-run dialog handling noted (S2).

---

## 3. Security Model

From SECURITY.md (S4) — verified claims:

1. **Session isolation:** each session gets a **random capability token** for the Hopper/Ghidra bridges; tokens delivered via **private session descriptors, not argv or env** (avoids process-list leakage).
2. **IPC locality:** POSIX uses **current-user Unix sockets**; Windows Ghidra bridge uses **authenticated loopback TCP** with a **private NTFS runtime directory** (DACL = current user + SYSTEM only).
3. **NOT a sandbox:** SECURITY.md explicitly states REA provides **no protection against malicious same-user processes** — a compromised process running as the same user is out of scope.
4. **Ghidra hardening:** uses the **packaged Java `HeadlessScript`** runner, an **isolated temp project**, and **private home/cache/runtime directories** (no contamination of the operator's Ghidra settings).
5. **Windows native controls (S9):** Windows npm builds **bundle native process/filesystem/DACL controls** used automatically; supports Windows 10+ x64, NTFS targets, operator-installed Ghidra 12.1.x (verified against 12.1.4), JDK 21+; supports native x86/x86-64/ARMNT/ARM64 PE + raw NMOS 6502; 26 read-only Ghidra operations. npm releases through 5.0.0 are x86-64-PE-only on Windows (x86 support landed on main afterwards).
6. **Data egress:** analysis runs locally; "REA does not upload your app" — but **tool results flow to the agent's model provider**, whose data policy applies (S2 FAQ). This matters for Lightspeed: decompiled code reaching a third-party LLM is a policy decision, not REA's.
7. **Vulnerability reporting:** via SECURITY.md (**contact channel details UNVERIFIED — not fetched this session**).
8. **Update provenance:** official channels only (morluto/rea, rea.tools, npm `rea-agents`); look-alike repos explicitly called out as unofficial (S2).

---

## 4. Evidence / Output Format

Verified from docs/mcp-contracts.md (S7), docs/cli.md (S6):

- **Canonical Evidence record:** every MCP tool returns findings in **both** plain `text` and `structuredContent` (MCP convention), containing at minimum:
  - `normalized_result` — the structured conclusion
  - `evidence_id` — stable identifier for the evidence
  - `raw_result` — raw engine output backing the conclusion
  - `analysis_profile` — **required field, may be `null`** (declares the settings/profile used)
- **Artifact inventories** carry `coverage.scope` (`root` | `container-entries`) and `coverage.status` (`complete` | `unknown`) — consumers must check coverage before treating an inventory as exhaustive.
- **Volume:** Evidence can be **hundreds of MB** for large targets (documented example: 334 MB Obsidian analysis → ~10 KB summary view). Evidence supports paged retrieval: views of type `summary`, `page` (params `collection`, `offset`, `limit`), and `module`. Downstream agents MUST page rather than load raw Evidence wholesale.
- **Snapshots:** results are keyed by **target bytes + operation + parameters + provider + settings** (S6) — reproducibility anchor. Import/export of snapshots supported.
- **CLI JSON:** `rea ... --json` emits structured output on stdout; `rea_progress` JSON lines on stderr (S13). Exit statuses documented in docs/cli.md (values **UNVERIFIED** — not enumerated this session).
- **Error contract:** docs/error-contract.schema.json exists in the repo (verified by contents listing) — schema contents **UNVERIFIED**.
- **Semantic vs structural graphs (JS):** the JS semantic graph is separate from the structural graph; `import type` / `export type` are **source facts, not runtime relationships** — a correctness caveat for any downstream consumer (S12).
- **Coverage limitations:** providers report what they could not resolve alongside what they found (README positioning, S2); native provider depth differs (Ghidra adapter ≈ 25 read-only ops + session-scoped naming edits per secondary source — **UNVERIFIED against docs/ghidra-provider.md this session**).

---

## 5. Maturity

Verified via GitHub API on 2026-10-17:

| Signal | Value |
|---|---|
| Stars | **296,983** (README celebrates 250,000) |
| Forks | 75,000 |
| Open issues | 1,207 |
| Subscribers (watchers) | 1,043 |
| Created | 2026-04-14 (~6 months old) |
| Last push | 2026-10-17 (same day — actively developed) |
| License (GitHub-detected) | MIT |
| Archived | No |
| Top contributors | morluto (1,790 commits), N0zoM1z0 (579), kaoru0822-kitauji (496), rudycelekli (91), github-actions[bot] (42) |
| Recent releases | rea-agents 6.5.0 (2026-10-14), 6.4.0 (10-11), 6.3.0 (10-09), 6.2.0 (10-09), 6.1.0 (10-09) |
| Latest observed commit | `f85a932d` (2026-10-17) — Windows path-separator normalization test pinning a 6.5.0 bug (issue #4707) |

**Assessment (evidence-based):**
- **Release cadence:** multiple releases per week; secondary source counts "31 npm versions since July 2026" (**UNVERIFIED**). Breaking-surface risk is real: docs contain a `migration-6.2.md`, and the IDA provider documents fail-closed behavior against upstream tool renames — **pin versions for any production use**.
- **Breadth vs depth trade-off:** one server covers many target types, but several target classes are Linux-only (firmware, packet captures, signal recordings, recorded crashes per secondary source; README table corroborates Linux-only rows) — **Windows-native coverage is narrower**.
- **Windows status:** Ghidra provider explicitly **experimental P0 read-only** (S9). Hopper is macOS-first. For a Windows 11 team, the free native stack is Ghidra-on-Windows (experimental) — plan validation accordingly.
- **Validation evidence:** three published showcases (DX-Ball reconstruction passing 3,205 original-x86 cases and reproducing all 63 compiled function bytes; Notion clipboard-bridge trace; TH04 DOS bullet-ring recovery) with reconstruction repos (S2). Docs tree includes `verification/`, `testing.md`, `reconstruction-coverage.md`, `obligation-ledgers.md` — a mature evidence posture for a 6-month-old project.
- **Community:** ~300k stars / 75k forks is exceptionally high; Discord community linked; translation into ~20 languages. Caution: star counts on very new viral repos are a weak proxy for production hardening; pair with the 1,207 open issues figure.
- **Single-maintainer concentration:** primary author holds ~53% of commits (1,790 of top-4 total ≈ 2,956) — bus-factor risk.

---

## 6. Ecosystem / Competitors

Category: **MCP bridges between AI coding agents and reverse-engineering tools.** None of these is a new decompiler — all wrap existing engines.

| Project | Maintainer | Connects to | Bridge license | Standout | REA relationship |
|---|---|---|---|---|---|
| **REA** | morluto | Hopper + Ghidra + IDA + Kuna, plus non-native analyzers (JS/Electron, .NET, APK, web, firmware, pcap, SQLite, WASM, EVM…) | MIT | Breadth + Evidence/snapshots; one MCP registration switching providers per target | — |
| **GhidraMCP** | LaurieWired | Ghidra 12.1.4 only | Apache-2.0 | Free end-to-end; v2.0 (2026-10-10) added PyGhidra headless; attaches to *your* GUI project (shared state) vs REA's ephemeral import; ~11.3k stars | Complementary: same engine, different project model |
| **Hex-Rays IDA MCP (official)** | Hex-Rays | IDA 9.4+ via idalib | MIT | Vendor-official; headless multi-agent; ships 2026-09-25, updated 10-08; claims ~20% token reduction in "code mode"; ~1,067 stars | Competes/complements; REA does not wrap it (wraps mrexodia's) |
| **IDA Pro MCP (ida-pro-mcp)** | mrexodia | IDA Pro 8.3+ (Free unsupported) | MIT | Deepest IDA surface (stack frames, types, debugger, `py_eval`); ~12,885 stars; README now recommends the official Hex-Rays server | **Upstream dependency** — REA's IDA provider adapts this server |
| **r2mcp** | radareorg | radare2 | MIT | Small C server on native r2 APIs; stdio/plugin/HTTP; sandbox + read-only modes; release 1.8.8 (2026-09-06); ~275 stars | Alternative free stack; not used by REA |
| **Binary Ninja MCP** | fosdickio | Binary Ninja | GPL-3.0 | All three IL levels, patching, multi-binary; v1.2.1 (2026-03); needs paid BN (Free has no plugins) | Not an REA engine |
| **Binary Ninja 6.0 first-party MCP** | Vector35 | Binary Ninja 6.0 (2026-09-03) | closed source | Built-in; GUI server in every edition incl. Free; headless server Commercial/Ultimate, macOS/Linux | Not an REA engine |
| **re-mcp** | jtsylve | IDA Pro 9+ **and** Ghidra 12+ (dual backend, shared tool interface) | UNVERIFIED | Supervisor/worker, multi-database, meta-tools (`search_tools`/`call`/`execute`/`batch`) to control token use | Closest structural analogue (multi-backend) |
| **bethington/ghidra-mcp** | bethington | Ghidra | Apache-2.0 | 209 tools, P-code emulation, debugger integration, Ghidra Server | Competes for Ghidra users |
| **mcpyghidra / MCPyIDA** | — | Ghidra / IDA via pyghidra-decaf | UNVERIFIED | 26 tools, sister projects with feature parity | Smaller alternatives |

**Positioning consensus across three independent secondary comparisons (2026-10-13 → 10-15):**
- Pick a **single-engine** server (GhidraMCP / official IDA MCP / r2mcp / BN MCP) when you live inside one disassembler and want the agent in *your* open database, including edits, types, debugger.
- Pick **REA** when targets are **mixed** (native + Electron + APK + captures), when you need **reproducible Evidence/snapshots**, or when you want one MCP registration that switches engines per target.
- **Stacking two servers over the same engine is advised against** (agent confusion; Hex-Rays says to disable other IDA MCP servers first).
- These servers **do not confer any license** to the tools they wrap.
- **Local analysis ≠ local privacy:** results still flow to the model provider.

---

## Shared Facts Summary

Verbatim-citable bullets for downstream artifacts:

1. REA is a **local MCP server + CLI (`rea`)**, npm package `rea-agents`, MIT-licensed (Copyright 2026 morluto), set up via `npx rea-agents setup` with approval-gated config changes.
2. It requires **Node.js 22.x ≥22.19, 24.x ≥24.11, or 26+ with npm**; runs analysis on the operator's machine.
3. One server covers **native binaries, JS/Electron, websites, .NET, Android APK/devices, firmware, pcap, SQLite, WASM, EVM bytecode, Go/Rust metadata, Flutter, process behavior**, and more — 23 rows in the README target table.
4. Native analysis **drives existing engines** — Hopper, Ghidra, or IDA (via upstream `mrexodia/ida-pro-mcp`) — plus the Apache-2.0 **Kuna** decompiler; **static JavaScript and .NET inspection need no native engine and never execute the target**.
5. Deep native analysis on Windows is **experimental (Ghidra P0, read-only)**, documented in docs/windows-ghidra-p0.md; several target classes (firmware, packet captures, signal recordings, recorded crashes) are **Linux-only**.
6. Every MCP tool returns a canonical **Evidence record** (`normalized_result`, `evidence_id`, `raw_result`, `analysis_profile`) in both `text` and `structuredContent`; Evidence can reach **hundreds of MB** and must be paged (`summary`/`page`/`module` views).
7. Results are **snapshot-keyed by target bytes + operation + parameters + provider + settings**, making runs reproducible and comparable across versions.
8. Security posture: **per-session random capability tokens** (never in argv/env), current-user Unix sockets / authenticated loopback TCP with DACL'd NTFS runtime dir on Windows, isolated Ghidra headless temp projects — and an explicit statement that **REA is not a sandbox** against same-user processes.
9. Analysis runs locally, but **tool results are delivered to the agent's model provider**, whose data policy governs what leaves the machine.
10. Maturity (2026-10-17): **~297k stars, ~75k forks, created 2026-04-14, actively pushed same-day, npm v6.5.0 (2026-10-14), multiple releases per week, 1,207 open issues**, three published reconstruction showcases; primary author holds ~53% of top-contribution commits (bus-factor risk).
11. Licensing rule: **REA grants no license to commercial engines** — operators must legally obtain IDA/Hopper/JEB themselves; cracked copies and key sharing are explicitly unauthorized.
12. In the MCP reverse-engineering ecosystem, REA is the **breadth-first** option vs single-engine servers (GhidraMCP, official Hex-Rays IDA MCP, r2mcp, Binary Ninja MCP); it **depends on** mrexodia/ida-pro-mcp for IDA and can **combine** with existing disassemblers rather than replace them.
13. Consumers must check **`coverage.scope`/`coverage.status`** on artifact inventories before treating them as exhaustive, and respect the JS caveat that `import type`/`export type` are source facts, not runtime edges.

## Open Questions / UNVERIFIED

- **Tool count** of the MCP catalog (docs/mcp-contracts.md#generated-catalog not fetched).
- **`DISCLAIMER.md` full text** and **SECURITY.md contact/reporting channel** — not fetched; only README's summary of responsible-use position is verified.
- **`docs/cli.md` exit-status codes** — file was fetched earlier in research but exit-code enumeration was not captured here.
- **`docs/error-contract.schema.json`** contents.
- **`docs/ghidra-provider.md` exact operation count** (secondary sources say 25 read-only ops; windows-ghidra-p0.md says 26 Windows P0 ops — reconcile before citing a single number).
- **Commercial pricing** (IDA Home/Pro, Hopper, Binary Ninja, JEB) — quoted figures come from secondary comparison articles, not vendor pricing pages.
- **Downstream Linux-only claim set** — README table marks specific rows Linux-only; secondary sources add "some verified only on Linux x64" broadly — verify per target before asserting.
- **"31 npm versions since July 2026"** and secondary star counts for competitors — secondary-source only.
- **Whether REA supports the official Hex-Rays IDA MCP** — verified only that it adapts mrexodia's; no evidence it wraps Hex-Rays'.
- **Skills.sh distribution** (`npx rea-agents` skill install) — badge present in README; mechanics not investigated.
- **Supply-chain posture** — dependency review, npm provenance/signing, and CI hardening were not audited this session.

---

*End of shared brief. Downstream agents: cite section + source ID (e.g., "§1 / S12"). Re-verify UNVERIFIED items against primary sources before publication.*
