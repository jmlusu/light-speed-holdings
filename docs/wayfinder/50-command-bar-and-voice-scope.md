# Issue #50 — Command Bar & Voice Scope (F10)

**Requirement F10**: Persistent command bar via keyboard shortcut or voice to re-assign
workloads / query org memory / set operational states.

**Status**: Design — open for implementation
**Date**: 2026-08-19
**Owner**: Software Architect
**Related files**: `command-bar-service.js`, `command-bar.js`, `command-center.js`

---

## 1. Command Vocabulary

The command bar supports two input modes: **typed query** (fuzzy search + command prefix)
and **voice** (natural language parsed into commands). Commands are grouped into five
categories. Every command has a `commandId` used in the `quickActions` registry and
an optional RBAC gate (see §4).

### 1.1 Task Management

| Command | Aliases (voice) | Endpoint | RBAC | Description |
|---------|----------------|----------|------|-------------|
| `task.new` | "new task", "create task" | `POST /api/v1/tasks` | `run` | Open new-task modal (already wired via `openTaskModal()`) |
| `task.assign` | "assign task", "reassign" | `PATCH /api/v1/tasks/:id/assign` | `run` | Assign or reassign a task to an agent |
| `task.cancel` | "cancel task", "abort" | `PATCH /api/v1/tasks/:id/cancel` | `approve` | Cancel a running or pending task |
| `task.priority` | "set priority", "high priority" | `PATCH /api/v1/tasks/:id` | `run` | Change task priority (low/normal/high/critical) |
| `task.list` | "tasks", "show tasks" | Navigate `/tasks` | None | Navigate to task board |

### 1.2 Agent Control

| Command | Aliases (voice) | Endpoint | RBAC | Description |
|---------|----------------|----------|------|-------------|
| `agent.pause` | "pause agent" | `POST /api/v1/agents/:id/pause` | `approve` | Pause an active agent |
| `agent.resume` | "resume agent" | `POST /api/v1/agents/:id/resume` | `approve` | Resume a paused agent |
| `agent.restart` | "restart agent" | `POST /api/v1/agents/:id/restart` | `admin` | Restart agent process |
| `agent.status` | "agent status" | `GET /api/v1/agents/:id` | None | Show agent status detail |
| `agent.list` | "agents", "show agents" | Navigate `/agents` | None | Navigate to agent fleet view |

### 1.3 Navigation

| Command | Aliases (voice) | Target | RBAC | Description |
|---------|----------------|--------|------|-------------|
| `nav.tasks` | "go to tasks" | `/tasks` | None | Task board |
| `nav.agents` | "go to agents" | `/agents` | None | Agent fleet |
| `nav.kpis` | "go to KPIs", "view metrics" | `/kpis` | None | KPI dashboard |
| `nav.timeline` | "timeline", "activity" | `/command-center` | None | Activity timeline / war room |
| `nav.approvals` | "approvals", "pending" | `/escalations` | None | Pending approvals queue |
| `nav.onboarding` | "onboarding" | `/onboarding` | None | Onboarding studio |
| `nav.costs` | "costs", "spending" | `/kpis#costs` | None | Cost breakdown (anchor on KPI page) |

### 1.4 Memory / Org

| Command | Aliases (voice) | Endpoint | RBAC | Description |
|---------|----------------|----------|------|-------------|
| `memory.search` | "search memory", "find in history" | `GET /api/v1/memory/search?q=` | `run` | Search org memory store |
| `memory.recent` | "recent decisions" | `GET /api/v1/memory/recent` | `run` | List recent memory entries |
| `memory.add` | "remember that", "save to memory" | `POST /api/v1/memory` | `approve` | Add entry to org memory |

### 1.5 Operational

| Command | Aliases (voice) | Endpoint | RBAC | Description |
|---------|----------------|----------|------|-------------|
| `ops.state` | "set state", "operational" | `PATCH /api/v1/system/state` | `admin` | Set org operational state (normal/degraded/emergency) |
| `ops.health` | "health check" | `GET /api/v1/health` | None | Trigger and display health check |
| `ops.deploy` | "deploy", "ship it" | `POST /api/v1/deploy` | `admin` | Trigger deployment (if CI wired) |

### 1.6 Summary counts

- **Total commands**: 22
- **`run` level**: 7 (read-heavy, low-risk mutations)
- **`approve` level**: 5 (cancellation, memory writes, agent lifecycle)
- **`admin` level**: 3 (restart, deploy, ops state)
- **No gate**: 7 (navigation + health check)

---

## 2. Voice Scope Decision

### Recommendation: Ship voice as **feature-flagged beta** in v0.5.1, not deferred.

**Rationale:**

1. **The wiring already exists.** `CommandBarService` already detects `SpeechRecognition`
   support, initializes it, and has `toggleVoice()` wired into the Alpine component.
   The voice icon is rendered in `command-bar.js` (microphone SVG). Shipping means
   testing what's already built, not building from scratch.

2. **Browser support is sufficient.** Web Speech API works in Chrome 33+, Edge 79+,
   Safari 14.1+, and Firefox behind a flag. The feature-degrade path is clean:
   `this.supportsVoice` gates the mic button — unsupported browsers see no button.

3. **Voice scope is read-only for v0.5.1.** Voice input maps to the same fuzzy search
   pipeline as typed queries. There is no voice-only mutation path. A spoken phrase
   like "assign task" populates the search box, which surfaces the matching
   `task.assign` action. The user still confirms with Enter/click.

4. **Risk is low.** Voice is a search accelerator, not an autonomous execution path.
   The RBAC enforcement lives on the API endpoint, not in the voice parser.

### Implementation pattern

```
Voice input → Web Speech API transcript → populates query input →
  → fuzzy search hits quickActions[] → user selects and confirms →
  → execute() dispatches to endpoint with RBAC check
```

### Feature flag

Wrap voice initialization in a dashboard config flag:

```javascript
// In command-bar-service.js constructor
this.supportsVoice = dashboardConfig.enableVoice !== false &&
    ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window);
```

The flag `dashboardConfig.enableVoice` defaults to `true`. If a voice-related bug
is reported post-release, set `enableVoice: false` in the dashboard config to hide
the mic button without a code deploy.

### What's explicitly deferred to v0.6

- **Multi-turn voice conversations** (e.g., "assign task" → "which agent?" → "the
  financial analyst"). The current implementation is single-shot: speak, populate
  search box, done.
- **Wake word** ("Hey Lighthouse"). Requires continuous audio streaming and is not
  supported by Web Speech API without a custom grammar.

---

## 3. Keyboard Shortcut Map

### Global shortcuts (active on all dashboard pages)

| Shortcut | Action | Source |
|----------|--------|--------|
| `⌘/Ctrl + K` | Toggle command bar open/close | `command-bar.js:56`, `command-center.js:84` |
| `Escape` | Close command bar (when open) | `command-bar.js:62` |
| `⌘/Ctrl + 1` | Switch to variant A ("The Bridge") | `command-center.js:94` |
| `⌘/Ctrl + 2` | Switch to variant B ("The War Room") | `command-center.js:94` |
| `⌘/Ctrl + 3` | Switch to variant C ("The Cockpit") | `command-center.js:94` |

### In-command-bar navigation

| Shortcut | Action |
|----------|--------|
| `Arrow Down` | Move selection down |
| `Arrow Up` | Move selection up |
| `Enter` | Execute selected command |
| `Tab` | Cycle through grouped sections (actions → agents → tasks) |
| `Escape` | Close command bar |

### Reserved for future (do not bind yet)

| Shortcut | Planned use |
|----------|-------------|
| `⌘/Ctrl + Shift + V` | Toggle voice input from anywhere |
| `⌘/Ctrl + /` | Open keyboard shortcut cheat sheet |
| `⌘/Ctrl + Shift + K` | Open command bar in "action mode" (skip search, show only commands) |

---

## 4. RBAC Integration

The command bar runs entirely in the browser. RBAC enforcement happens at two layers:

### Layer 1: Command filtering (client-side)

Commands the user lacks permissions for are **hidden** from the command palette,
not shown and rejected on execute. This avoids UX friction.

The Alpine component reads `window.dashboardUserRole` (set in `base.html` from the
session token's resolved role) and filters the quickActions list:

```javascript
// In command-bar.js groupedResults getter
const userRole = window.dashboardUserRole || 'run';
const minRank = { run: 0, approve: 1, admin: 2 };
return this.results.filter(r => {
    const reqRank = r.minRole ? minRank[r.minRole] : 0;
    return minRank[userRole] >= reqRank;
});
```

### Layer 2: Server-side enforcement

Every mutation endpoint (`task.assign`, `agent.pause`, `ops.state`, etc.) uses
the existing `require_role()` FastAPI dependency. The command bar is a convenience
layer; the API remains the authority.

### RBAC matrix

| Minimum Role | Commands |
|-------------|----------|
| *(none)* | `task.list`, `agent.list`, `agent.status`, `nav.*`, `ops.health` |
| `run` | `task.new`, `task.assign`, `task.priority`, `memory.search`, `memory.recent` |
| `approve` | `task.cancel`, `agent.pause`, `agent.resume`, `memory.add` |
| `admin` | `agent.restart`, `ops.state`, `ops.deploy` |

---

## 5. Implementation Pattern

### Current state

The `quickActions` array in `command-bar-service.js` (line 9-16) holds six entries:
`new-task`, `tasks`, `kpis`, `agents`, `onboarding`, `approvals`. Each entry has
`id`, `label`, `icon`, and either a `url` (navigation) or `action` (callback).

### Target state

Expand `quickActions` to hold all 22 commands. Add two new properties per entry:

- **`minRole`**: The minimum RBAC role required (used for client-side filtering)
- **`category`**: One of `task`, `agent`, `nav`, `memory`, `ops` (used for grouped display)

### Schema

```javascript
{
    id: 'task.assign',            // unique command ID (dot notation)
    label: 'Assign Task',         // display label
    icon: 'user-plus',            // SVG icon key
    category: 'task',             // grouping key
    minRole: 'run',               // RBAC gate (null = no gate)
    aliases: ['assign', 'reassign'], // optional voice/text aliases
    action: () => ...,            // callback OR
    url: '/tasks?action=assign',  // navigation target
}
```

### Wiring to `execute()`

The existing `execute()` method (line 92-98) already handles both `url` navigation
and `action` callbacks. No changes needed — new commands that require API calls
use the `action` callback pattern:

```javascript
{
    id: 'task.cancel',
    label: 'Cancel Task',
    action: () => {
        window.dispatchEvent(new CustomEvent('command-bar:cancel-task', {
            detail: { taskId: this.selectedTaskId }
        }));
    },
}
```

The Alpine component listens for these custom events and opens the appropriate
modal or confirmation dialog. The actual API call happens from the modal's
submit handler, which carries the user's session token and is subject to server-side
RBAC.

### Voice alias matching

When voice input lands in the search box, the fuzzy search in `search()` (line 66-81)
hits the `/api/v1/search/quick` endpoint. The server-side search index should also
match against the `aliases` array for each command, so "assign task" maps to
`task.assign` with the same score as a label match.

---

## 6. Open Questions

| # | Question | Proposed resolution |
|---|----------|-------------------|
| 1 | Should voice commands require confirmation before executing mutations? | Yes for all `approve`+ gated commands. No for read-only navigation. |
| 2 | What happens if voice transcription is ambiguous? | Populate search box with transcript, let user correct before confirming. |
| 3 | Should the command bar remember recent commands? | Yes — store last 5 executed `commandId`s in `localStorage` and show them at the top when the bar opens. |
| 4 | Should `ops.deploy` exist in the command bar? | Only if CI webhook is wired. Otherwise defer to v0.6. |

---

## Appendix A: Voice Phrase → Command Mapping

The server-side search endpoint should index these voice aliases alongside the label:

| Spoken phrase | Matches command |
|---------------|----------------|
| "new task" | `task.new` |
| "assign task" / "reassign" | `task.assign` |
| "cancel task" / "abort task" | `task.cancel` |
| "set priority high" / "high priority" | `task.priority` |
| "show tasks" / "go to tasks" | `task.list` |
| "pause agent" | `agent.pause` |
| "resume agent" | `agent.resume` |
| "restart agent" | `agent.restart` |
| "agent status" | `agent.status` |
| "show agents" / "go to agents" | `agent.list` |
| "go to KPIs" / "view metrics" | `nav.kpis` |
| "timeline" / "activity" | `nav.timeline` |
| "approvals" / "pending" | `nav.approvals` |
| "search memory" / "find in history" | `memory.search` |
| "recent decisions" | `memory.recent` |
| "remember that" / "save to memory" | `memory.add` |
| "set state" / "operational state" | `ops.state` |
| "health check" / "system health" | `ops.health` |
| "deploy" / "ship it" | `ops.deploy` |
