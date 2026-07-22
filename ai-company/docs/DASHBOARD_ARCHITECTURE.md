# Dashboard Architecture — Backend Interaction Diagram

> How the CEO Dashboard communicates with the backend.
> Generated 2026-07-22 from team review.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BROWSER (Client)                                    │
│                                                                             │
│  ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────────┐   │
│  │   Alpine.js       │◄───│  app.js         │◄───│  WebSocket Client    │   │
│  │   (Reactive UI)   │    │  (Data Store)   │    │  /ws/dashboard       │   │
│  └────────┬─────────┘    └───────┬─────────┘    └──────────┬───────────┘   │
│           │                      │                          │               │
│           │  x-data bindings     │  fetch() calls           │  onmessage   │
│           │  (x-text, x-show,   │  (REST API)              │              │
│           │   x-for, :class)    │                          │              │
│           ▼                      ▼                          ▼              │
│  ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────────┐   │
│  │   Jinja2          │    │  charts.js      │    │  Tailwind CSS        │   │
│  │   Templates       │    │  (Chart.js)     │    │  + style.css         │   │
│  │   (SSR HTML)      │    │                 │    │                      │   │
│  └──────────────────┘    └─────────────────┘    └──────────────────────┘   │
│                                                                             │
│  CDN Dependencies: tailwindcss, alpinejs, chart.js                         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                         HTTP REST + WebSocket (ws://)
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FastAPI SERVER (app.py)                                 │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      MIDDLEWARE STACK                                  │  │
│  │  ┌─────────┐  ┌──────────────┐  ┌────────────────────────────────┐  │  │
│  │  │ CORS    │──│ Rate Limiter │──│ API Key Guard (POST/DELETE)     │  │  │
│  │  └─────────┘  └──────────────┘  └────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────┬────────────────────────────────────────┐  │
│  │         ROUTERS (api.py)      │         WebSocket (ws.py)             │  │
│  │                               │                                        │  │
│  │  Page Routes:                 │  WS /ws/dashboard                     │  │
│  │  GET /        → index.html    │    ├── on message:                     │  │
│  │  GET /agents  → agents.html   │    │   ├── ping → pong                │  │
│  │  GET /tasks   → tasks.html    │    │   ├── subscribe topics            │  │
│  │  GET /kpis    → kpis.html     │    │   └── unsubscribe                 │  │
│  │  GET /costs   → costs.html    │    └── broadcast ←                     │  │
│  │                               │        ├── kpi_update                 │  │
│  │  API Routes:                  │        ├── alert                      │  │
│  │  GET /api/dashboard → KPIs    │        ├── task_update                 │  │
│  │  GET /api/agents   → List     │        ├── department_kpi              │  │
│  │  GET /api/tasks    → List     │        └── escalation                  │  │
│  │  POST /api/tasks   → Create   │                                        │  │
│  │  GET /api/approvals → List    │                                        │  │
│  │  POST /api/approvals/{id}/    │                                        │  │
│  │       approve                 │                                        │  │
│  │  POST /api/approvals/{id}/    │                                        │  │
│  │       reject                  │                                        │  │
│  │  GET /api/escalations → List  │                                        │  │
│  │  POST /api/escalations/{id}/  │                                        │  │
│  │       resolve                 │                                        │  │
│  │  GET /api/departments → List  │                                        │  │
│  │  GET /api/org-chart → Tree    │                                        │  │
│  │  GET /api/kpis/live → Live    │                                        │  │
│  │  GET /api/ceo-dashboard       │                                        │  │
│  │  GET /metrics → Prometheus    │                                        │  │
│  └───────────────────────────────┴────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                  DATA LAYER (repository.py → FileStore)               │  │
│  │                                                                       │  │
│  │  StateStore (allowlisted paths only)                                  │  │
│  │    ├── read_json() / write_json()                                     │  │
│  │    ├── read_yaml() / write_yaml()                                     │  │
│  │    ├── iter_jsonl() (audit log)                                       │  │
│  │    └── Atomic file I/O with validation                                │  │
│  │                                                                       │  │
│  │  Data Sources:                                                        │  │
│  │    ├── .opencode/inbox.json          (MessageBus → tasks)             │  │
│  │    ├── orchestrator/approvals.yaml   (approval queue)                 │  │
│  │    ├── orchestrator/escalation.yaml  (escalations)                    │  │
│  │    ├── orchestrator/scheduler.yaml   (scheduled tasks)                │  │
│  │    ├── orchestrator/cost_tracker.json (LLM costs)                     │  │
│  │    ├── company/config/kpis.yaml      (KPI definitions)                │  │
│  │    ├── company/departments.yaml      (departments)                    │  │
│  │    └── company/agent-registry.json   (agent metadata)                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   KPI COLLECTION PIPELINE                             │  │
│  │                                                                       │  │
│  │  7 Department Collectors (dashboard/kpis/)                            │  │
│  │    ├── engineering.py   (task rates, escalation rate)                 │  │
│  │    ├── finance.py       (budget, LLM spend, cost/agent)              │  │
│  │    ├── hr.py            (onboarding, turnover, satisfaction)          │  │
│  │    ├── legal.py         (compliance, contract processing)             │  │
│  │    ├── marketing.py     (campaigns, lead conversion)                  │  │
│  │    ├── sales.py         (pipeline, win rate, revenue)                 │  │
│  │    └── customer_success.py (NPS, churn, retention)                   │  │
│  │              │                                                        │  │
│  │              ▼                                                        │  │
│  │  collect_all_kpis() → /api/kpis/live → WS broadcast_kpi_update()     │  │
│  │                                                                       │  │
│  │  Analytics (dashboard/analytics.py)                                   │  │
│  │    ├── KPIHistoryStore (NDJSON + file locking)                        │  │
│  │    ├── AlertEngine (threshold rules)                                  │  │
│  │    ├── Trend Analysis (period-over-period)                            │  │
│  │    └── Summary Statistics (daily/weekly/monthly)                      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   ORCHESTRATION LAYER                                  │  │
│  │                                                                       │  │
│  │  MessageBus (orchestrator/message_bus.py)                             │  │
│  │    ├── Task distribution (inbox.json)                                 │  │
│  │    ├── WebSocket broadcast callback (sync→async bridge)               │  │
│  │    └── Dead-letter queue for stale tasks                              │  │
│  │                                                                       │  │
│  │  Executor (executor/loop.py)                                          │  │
│  │    ├── Polls MessageBus for pending tasks                             │  │
│  │    ├── Runs AgentLoop (ReAct pattern)                                 │  │
│  │    ├── Cost tracking per task                                         │  │
│  │    └── Broadcasts task_update via WS                                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   MONITORING (monitoring.py)                           │  │
│  │                                                                       │  │
│  │  Prometheus /metrics endpoint                                         │  │
│  │    ├── Dashboard page load latency                                    │  │
│  │    ├── WS broadcast latency                                           │  │
│  │    ├── KPI collection cycle time                                      │  │
│  │    └── Active WS clients gauge                                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Mermaid Diagram

```mermaid
graph TB
    %% ── Styling ──────────────────────────────────────────────
    classDef browser fill:#6B3FA0,stroke:#4A2D70,color:#FFFFFF,font-weight:bold
    classDef server fill:#2D7DD2,stroke:#1B5A96,color:#FFFFFF,font-weight:bold
    classDef data fill:#5B9E5E,stroke:#3A6B3C,color:#FFFFFF,font-weight:bold
    classDef ws fill:#D4A04A,stroke:#A07830,color:#FFFFFF,font-weight:bold
    classDef kpi fill:#9B59B6,stroke:#7D3C98,color:#FFFFFF,font-weight:bold
    classDef monitor fill:#E85D4A,stroke:#B8423A,color:#FFFFFF,font-weight:bold

    %% ── Browser ─────────────────────────────────────────────
    subgraph BROWSER ["🖥️ Browser (Client)"]
        ALPINE["Alpine.js<br/>Reactive UI Layer"]
        APPJS["app.js<br/>Data Store + Polling"]
        WSCLIENT["WebSocket Client<br/>ws://.../ws/dashboard"]
        CHARTS["charts.js<br/>Chart.js Integration"]
        TEMPLATES["Jinja2 Templates<br/>SSR HTML"]
    end

    %% ── Transport ───────────────────────────────────────────
    REST["REST API<br/>fetch() calls"]
    WSCONN["WebSocket<br/>/ws/dashboard"]

    %% ── Server ──────────────────────────────────────────────
    subgraph SERVER ["⚡ FastAPI Server"]
        MIDDLEWARE["Middleware<br/>CORS · Rate Limit · API Key"]
        API["REST Router<br/>api.py (1178 lines)"]
        WSR["WebSocket Hub<br/>ws.py (249 lines)"]
        REPO["StateStore<br/>repository.py"]
    end

    %% ── Data Layer ──────────────────────────────────────────
    subgraph DATA ["💾 Data Sources"]
        INBOX[".opencode/inbox.json<br/>MessageBus"]
        APPROVALS["orchestrator/approvals.yaml"]
        ESCALATIONS["orchestrator/escalation.yaml"]
        SCHEDULER["orchestrator/scheduler.yaml"]
        COSTS["orchestrator/cost_tracker.json"]
        KPIS["company/config/kpis.yaml"]
        DEPARTMENTS["company/departments.yaml"]
        REGISTRY["company/agent-registry.json"]
    end

    %% ── KPI Pipeline ────────────────────────────────────────
    subgraph KPI ["📊 KPI Pipeline"]
        COLLECT["collect_all_kpis()"]
        ENGINEERING["engineering.py"]
        FINANCE["finance.py"]
        HR["hr.py"]
        LEGAL["legal.py"]
        MARKETING["marketing.py"]
        SALES["sales.py"]
        CS["customer_success.py"]
        ANALYTICS["Analytics<br/>History · Trends · Alerts"]
    end

    %% ── Orchestration ───────────────────────────────────────
    subgraph ORCH ["🔄 Orchestration"]
        MBUS["MessageBus<br/>Task Distribution"]
        EXECUTOR["Executor<br/>AgentLoop + ReAct"]
    end

    %% ── Monitoring ──────────────────────────────────────────
    PROM["📈 Prometheus<br/>/metrics"]

    %% ── Connections ─────────────────────────────────────────
    ALPINE --> APPJS
    APPJS --> REST
    APPJS --> WSCLIENT
    WSCLIENT --> WSCONN
    CHARTS --> ALPINE
    TEMPLATES --> ALPINE

    REST --> MIDDLEWARE
    MIDDLEWARE --> API
    WSCONN --> WSR

    API --> REPO
    WSR --> REPO
    REPO --> DATA

    API --> MBUS
    MBUS --> EXECUTOR
    EXECUTOR -->|"broadcast_task_update"| WSR

    COLLECT --> ENGINEERING
    COLLECT --> FINANCE
    COLLECT --> HR
    COLLECT --> LEGAL
    COLLECT --> MARKETING
    COLLECT --> SALES
    COLLECT --> CS
    KPI --> COLLECT
    COLLECT --> ANALYTICS
    COLLECT -->|"broadcast_kpi_update"| WSR

    API --> PROM

    %% ── Apply styles ────────────────────────────────────────
    class ALPINE,APPJS,WSCLIENT,CHARTS,TEMPLATES browser
    class MIDDLEWARE,API,WSR,REPO server
    class INBOX,APPROVALS,ESCALATIONS,SCHEDULER,COSTS,KPIS,DEPARTMENTS,REGISTRY data
    class COLLECT,ENGINEERING,FINANCE,HR,LEGAL,MARKETING,SALES,CS,ANALYTICS kpi
    class MBUS,EXECUTOR server
    class PROM monitor
```

---

## Data Flow Sequence

```mermaid
sequenceDiagram
    autonumber

    participant Browser as 🖥️ Browser
    participant Alpine as ⚡ Alpine.js
    participant AppJS as 📋 app.js
    participant Charts as 📊 charts.js
    participant REST as 🌐 REST Router
    participant WS as 🔌 WebSocket Hub
    participant Store as 💾 StateStore
    participant KPI as 📈 KPI Pipeline
    participant Executor as 🔄 Executor

    Note over Browser,Executor: === Initial Page Load ===

    Browser->>Alpine: Render Jinja2 template
    Alpine->>AppJS: init() — loadPageData()
    AppJS->>REST: GET /api/dashboard
    REST->>Store: read_json(inbox.json)
    Store-->>REST: task data
    REST-->>AppJS: KPIs JSON
    AppJS->>Alpine: Object.assign(kpis)
    Alpine->>Charts: updateOrCreateChart()
    Charts-->>Browser: Charts rendered

    AppJS->>WS: connectWebSocket()
    WS-->>AppJS: connected message

    Note over Browser,Executor: === Ongoing Updates ===

    loop Every 15 seconds (polling)
        AppJS->>REST: GET /api/tasks, /api/agents
        REST->>Store: read_json / read_yaml
        Store-->>REST: data
        REST-->>AppJS: JSON response
        AppJS->>Alpine: batch state update
        Alpine->>Charts: chart.update('none')
    end

    loop WebSocket messages
        WS-->>AppJS: kpi_update / task_update / alert
        AppJS->>AppJS: saveScrollPosition()
        AppJS->>Alpine: Object.assign(state)
        Alpine->>Charts: chart.update('none')
        AppJS->>AppJS: restoreScrollPosition()
    end

    Note over Browser,Executor: === Executor Loop (Backend) ===

    Executor->>Store: get_pending_tasks()
    Store-->>Executor: [tasks]
    Executor->>Executor: AgentLoop.run()
    Executor->>Store: update_task_status(COMPLETED)
    Executor->>WS: broadcast_task_update()
    WS-->>Browser: task_update message
```

---

## Key Components

| Component | File | Purpose |
|-----------|------|---------|
| **Alpine.js** | Templates (`x-data`) | Reactive UI bindings for KPIs, tasks, agents |
| **app.js** | `static/js/app.js` | Data fetching, WebSocket, polling, scroll management |
| **charts.js** | `static/js/charts.js` | Chart.js wrapper with `updateOrCreateChart()` |
| **style.css** | `static/css/style.css` | Layout, CSS containment, scroll behavior, skeletons |
| **api.py** | `dashboard/api.py` | 70+ REST endpoints, CORS, rate limiting, API key auth |
| **ws.py** | `dashboard/ws.py` | WebSocket hub, topic-based broadcasting |
| **repository.py** | `dashboard/repository.py` | StateStore with atomic file I/O, path allowlist |
| **kpis/** | `dashboard/kpis/` | 7 department KPI collectors + `collect_all_kpis()` |
| **analytics.py** | `dashboard/analytics.py` | History store, trend analysis, alert engine |
| **message_bus.py** | `orchestrator/message_bus.py` | Task queue (inbox.json), broadcast callbacks |
| **monitoring.py** | `dashboard/monitoring.py` | Prometheus `/metrics` endpoint |

---

## Update Mechanisms

### REST Polling (Fallback)
- **Interval**: 15 seconds (was 10s — debounced for stability)
- **Trigger**: Page load + periodic `setInterval`
- **Suppressed**: When WebSocket is connected (avoids redundancy)
- **Scroll preservation**: `saveScrollPosition()` → fetch → `restoreScrollPosition()`

### WebSocket Push (Primary)
- **Endpoint**: `/ws/dashboard`
- **Topics**: `kpi_update`, `task_update`, `alert`, `department_kpi`, `escalation`
- **Reconnection**: Exponential backoff with jitter (max 30s)
- **Heartbeat**: Ping/pong every 25s

### Chart Updates
- **Method**: `chart.update('none')` — in-place data mutation, no destroy/recreate
- **Container**: `.chart-container` prevents layout collapse during updates
- **Debounce**: Max 2 updates per second via `_chartUpdatePending` flag

---

## CSS Containment Boundaries

The following elements use `contain: layout style` to prevent reflows from cascading to the viewport:

| Element | Class | Prevents |
|---------|-------|----------|
| KPI Cards | `.kpi-card` | Value updates → scroll jump |
| Chart Containers | `.chart-container` | Canvas resize → scroll jump |
| Table Wrappers | `.table-wrap` | Row changes → scroll jump |
| Kanban Columns | `.kanban-column` | Drag operations → scroll jump |
| WS Status Badge | `.ws-status` | "Live"↔"Offline" → header shift |
| Header | `<header>` | Sticky header → content shift |

---

## Security Layers

| Layer | Implementation | Scope |
|-------|----------------|-------|
| **CORS** | FastAPI CORSMiddleware | Allowed origins: `localhost:3000,5173` |
| **Rate Limiting** | Custom middleware | 100-200 req/min (configurable) |
| **API Key Auth** | Header-based (`X-API-Key`) | POST/DELETE endpoints only |
| **StateStore Allowlist** | Path validation | Only whitelisted directories accessible |
| **Input Validation** | Pydantic models | All request/response schemas validated |
