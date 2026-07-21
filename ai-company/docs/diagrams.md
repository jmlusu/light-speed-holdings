# Light Speed Holdings — System Diagrams

> Production-quality Mermaid diagrams for the AI Company Builder.
> Generated 2026-07-21 from codebase analysis.

---

## Diagram 1: System Context (C4 Level 1)

```mermaid
graph TB
    %% ── Styling ──────────────────────────────────────────────
    classDef human fill:#4A90D9,stroke:#2C5F8A,color:#FFFFFF,font-weight:bold
    classDef system fill:#5B9E5E,stroke:#3A6B3C,color:#FFFFFF,font-weight:bold
    classDef infra fill:#D4A04A,stroke:#A07830,color:#FFFFFF,font-weight:bold
    classDef central fill:#6B3FA0,stroke:#4A2D70,color:#FFFFFF,font-weight:bold,font-size:16px
    classDef subtitle fill:none,stroke:none,color:#E8DFF5,font-style:italic

    %% ── Human Users (Left) ───────────────────────────────────
    subgraph users ["👥 Human Stakeholders"]
        direction TB
        CEO["🧑‍💼 Human CEO / Operator<br/><i>Directs strategy & tasks</i>"]
        BOARD["🏛️ Board of Directors<br/><i>Governance & oversight</i>"]
        APPROVERS["✋ Human Approvers<br/><i>HITL approval gates</i>"]
    end

    %% ── Central System ───────────────────────────────────────
    ACB["🏗️ AI Company Builder<br/>Python CLI for AI Agent Orchestration"]
    ACB_DASH["📊 CEO Dashboard<br/><i>FastAPI · REST · WebSocket</i>"]

    %% ── External Systems (Right) ─────────────────────────────
    subgraph external ["🔌 External Systems"]
        direction TB
        OPENCODE["⚡ OpenCode Runtime<br/><i>Agent execution engine</i>"]
        subgraph llms ["🤖 LLM Providers"]
            direction LR
            OPENAI["OpenAI"]
            ANTHROPIC["Anthropic"]
            OLLAMA["Ollama"]
            DEEPSEEK["DeepSeek"]
        end
    end

    %% ── Infrastructure (Bottom) ──────────────────────────────
    subgraph infra ["💾 Infrastructure"]
        direction LR
        FS["📁 File System<br/><i>YAML configs · Agent .md files</i>"]
        BUS["📬 MessageBus<br/><i>inbox.json task queue</i>"]
        PROM["📈 Prometheus<br/><i>Metrics & alerting</i>"]
        AUDIT["📋 Audit Trail<br/><i>JSONL event log</i>"]
        MEM["🧠 Memory Store<br/><i>6 memory types</i>"]
    end

    %% ── Connections ──────────────────────────────────────────
    CEO -->|"creates tasks · runs CLI"| ACB
    BOARD -->|"sets governance rules"| ACB
    APPROVERS -->|"approves / rejects"| ACB_DASH

    ACB -->|"generates agents"| OPENCODE
    ACB -->|"routes prompts"| llms
    ACB -->|"writes configs"| FS
    ACB -->|"enqueues tasks"| BUS

    ACB_DASH -->|"serves KPIs"| PROM
    ACB_DASH -->|"reads tasks"| BUS
    ACB_DASH -->|"WebSocket live updates"| APPROVERS

    OPENCODE -->|"reads agent specs"| FS
    OPENCODE -->|"polls tasks"| BUS
    OPENCODE -->|"logs events"| AUDIT
    OPENCODE -->|"recalls context"| MEM

    %% ── Apply styles ─────────────────────────────────────────
    class CEO,BOARD,APPROVERS human
    class OPENCODE external
    class ACB,ACB_DASH central
    class FS,BUS,PROM,AUDIT,MEM infra
```

---

## Diagram 2: Agent Generation Pipeline

```mermaid
graph LR
    %% ── Styling ──────────────────────────────────────────────
    classDef input fill:#2D7DD2,stroke:#1B5A96,color:#FFFFFF,font-weight:bold
    classDef process fill:#6B3FA0,stroke:#4A2D70,color:#FFFFFF,font-weight:bold
    classDef template fill:#D4A04A,stroke:#A07830,color:#FFFFFF,font-weight:bold
    classDef output fill:#5B9E5E,stroke:#3A6B3C,color:#FFFFFF,font-weight:bold
    classDef decision fill:#E85D4A,stroke:#B8423A,color:#FFFFFF,font-weight:bold
    classDef stage fill:none,stroke:#4A5568,color:#CBD5E0,stroke-dasharray:5 5

    %% ── Input Stage ──────────────────────────────────────────
    subgraph input_stage ["📥 Input"]
        direction TB
        YAML["📄 company-registry.yaml<br/><i>Single source of truth</i>"]
        CONFIGS["⚙️ config/*.yaml<br/><i>19 configuration files</i>"]
        TYPES["🏷️ Agent Types<br/><i>executive · department · specialist<br/>board · workflow · config</i>"]
    end

    %% ── Processing Stage ─────────────────────────────────────
    subgraph process_stage ["⚙️ Processing"]
        direction TB
        REGISTRY["📚 RegistryLoader<br/><i>Load → Parse → Resolve → Validate</i>"]

        DECISION{{"🔀 Template Selection<br/><i>agent.type → template file</i>"}}

        subgraph paths ["Parallel Generation Paths"]
            direction LR
            DIRECT["🎯 AgentGenerator<br/><i>Direct YAML → .md rendering</i>"]
            BOOTSTRAP["🏗️ BootstrapEngine<br/><i>Full company generation<br/>+ directories + configs</i>"]
        end

        NORMALIZE["🔧 Tool Normalization<br/><i>registry names → OpenCode 1.18.4</i>"]
        RENDER["🎨 Jinja2 Rendering<br/><i>12 templates × agent data</i>"]
    end

    %% ── Output Stage ─────────────────────────────────────────
    subgraph output_stage ["📤 Output"]
        direction TB
        AGENTS["📄 .opencode/agents/*.md<br/><i>OpenCode-compatible agent files</i>"]
        DIRS["📂 .opencode/{dirs}/<br/><i>memory · knowledge · projects<br/>prompts · workflows · logs</i>"]
        YAMLS["📋 .opencode/config/*.yaml<br/><i>company · org_chart · workflows<br/>governance</i>"]
        VALIDATED["✅ Validation Report<br/><i>OpenCode 1.18.4 compliance check</i>"]
    end

    %% ── Flow ─────────────────────────────────────────────────
    YAML --> REGISTRY
    CONFIGS --> REGISTRY
    REGISTRY --> DECISION

    DECISION -->|"agent type match"| DIRECT
    DECISION -->|"full bootstrap"| BOOTSTRAP

    DIRECT --> NORMALIZE
    BOOTSTRAP --> NORMALIZE
    BOOTSTRAP --> DIRS
    BOOTSTRAP --> YAMLS

    NORMALIZE --> RENDER
    RENDER --> AGENTS
    RENDER --> VALIDATED

    %% ── Legend Callout ───────────────────────────────────────
    LEGEND["💡 Template Map<br/>executive → executive.md.j2<br/>department → department.md.j2<br/>specialist → specialist.md.j2<br/>board → board.md.j2<br/>default → base.md.j2"]

    %% ── Apply styles ─────────────────────────────────────────
    class YAML,CONFIGS,TYPES input
    class REGISTRY,NORMALIZE,RENDER process
    class DECISION decision
    class AGENTS,DIRS,YAMLS,VALIDATED output
    class LEGEND template
```

---

## Diagram 3: Executor Task Lifecycle (ReAct Loop)

```mermaid
sequenceDiagram
    autonumber

    %% ── Participants ─────────────────────────────────────────
    participant MB as 📬 MessageBus<br/><i>inbox.json</i>
    participant EXEC as 🔄 Executor<br/><i>tick() loop</i>
    participant MEM as 🧠 Memory<br/><i>recall + store</i>
    participant CTX as 📋 Context<br/><i>Agent spec parser</i>
    participant LOOP as 🎯 AgentLoop<br/><i>ReAct pattern</i>
    participant LLM as 🤖 LLM Client<br/><i>Multi-provider</i>
    participant TR as 🔧 ToolRunner<br/><i>Plan executor</i>
    participant HITL as ✋ HITL Gate<br/><i>Approval queue</i>
    participant AUD as 📋 Audit Trail<br/><i>JSONL events</i>

    %% ── Phase 1: Task Pickup ─────────────────────────────────
    rect rgb(45, 55, 72)
        Note over MB,EXEC: Phase 1 — Task Acquisition
        EXEC->>MB: get_pending_tasks()
        MB-->>EXEC: [task_1, task_2, ...]
        EXEC->>MB: detect_stale_tasks() → DLQ
        EXEC->>EXEC: _resume_parked_tasks()
    end

    %% ── Phase 2: Pre-Execution Setup ─────────────────────────
    rect rgb(55, 45, 72)
        Note over EXEC,MEM: Phase 2 — Context Loading
        EXEC->>MB: update_task_status(IN_PROGRESS)
        EXEC->>MEM: recall_context(instruction)
        MEM-->>EXEC: relevant memories (best-effort)
        EXEC->>CTX: parse_agent_spec(receiver_id)
        CTX-->>EXEC: AgentContext (type, tools, permissions)
    end

    %% ── Phase 3: ReAct Loop ──────────────────────────────────
    rect rgb(40, 55, 40)
        Note over LOOP,TR: Phase 3 — ReAct Iteration Loop (max 10)
        
        loop Each Iteration (i = 1..10)
            %% Budget check
            EXEC->>LOOP: run(agent, prompt, task_id)
            
            %% LLM Call
            LOOP->>LOOP: Build system + user prompt
            LOOP->>LLM: chat(system, conversation_history)
            LLM-->>LOOP: ChatResponse {content, usage, model}
            LOOP->>LOOP: parse_llm_json(response)

            alt Valid JSON with plan[]
                %% Tool Execution
                LOOP->>TR: run_plan(plan, hitl_gate)
                
                alt HITL-gated tool
                    TR->>HITL: request_and_wait(action)
                    HITL-->>TR: ⏸️ HITLParked (non-blocking)
                    TR-->>LOOP: HITLParked exception
                    LOOP-->>EXEC: PARK → WAITING_APPROVAL
                    Note right of EXEC: Task parked, executor<br/>continues with other tasks
                else Normal tool
                    TR->>TR: shlex.split() → execute
                    TR-->>LOOP: step_results[]
                end

                %% Feedback loop
                LOOP->>LOOP: build_iteration_feedback()
                LOOP->>LOOP: conversation_history.append(results)

                opt Agent signals done=true
                    LOOP-->>EXEC: LoopResult(done=true)
                end

            else No plan (raw text)
                LOOP-->>EXEC: LoopResult(done=true, text)
            end

            opt Budget exceeded
                LOOP-->>EXEC: LoopResult(error="Budget exceeded")
            end

            opt Max iterations reached
                LOOP-->>EXEC: LoopResult(error="Max iterations")
            end
        end
    end

    %% ── Phase 4: Completion ──────────────────────────────────
    rect rgb(55, 45, 35)
        Note over EXEC,AUD: Phase 4 — Completion & Audit
        
        alt Task Succeeded
            EXEC->>MB: update_task_status(COMPLETED)
            EXEC->>AUD: log_task_status(pending → completed)
            EXEC->>MEM: record_task_outcome(completed)
        else Task Failed
            EXEC->>MB: update_task_status(FAILED)
            EXEC->>AUD: log_task_status(pending → failed)
            EXEC->>MEM: record_task_outcome(failed)
        else HITL Parked
            EXEC->>MB: update_task_status(WAITING_APPROVAL)
            EXEC->>AUD: log_task_status(in_progress → waiting_approval)
        end

        EXEC->>EXEC: save_loop_artifacts() → results/{task_id}/
        EXEC->>EXEC: Update ExecutorStats
    end
```
