# Research Question Decomposition

## Primary Research Question
What are the viable free-tier cloud stacks (compute + storage + secrets + automation) that can host a 24/7 "Lightspeed AI Company Builder" application WITHOUT requiring any credit card at signup, supporting data persistence, and allowing background processes?

## Sub-Questions

### Task 1: Hugging Face Spaces Free CPU Tier
- SQ1.1: What is the current RAM allocation for HF Spaces Free CPU tier (is it 16GB)?
- SQ1.2: What are the storage limits (ephemeral vs persistent)?
- SQ1.3: What is the sleep/idle policy - when does it sleep, can background processes keep it alive?
- SQ1.4: What does ToS say about long-running background processes?
- SQ1.5: What outbound network restrictions exist (blocked ports/protocols)?
- SQ1.6: What survives container restart (persistence model)?
- SQ1.7: Signup requirements - email/GitHub OAuth only? No card required?

### Task 2: Hugging8n Project Audit
- SQ2.1: What is the GitHub repo URL and last commit date?
- SQ2.2: What is the active maintenance status (issues, PRs, releases frequency)?
- SQ2.3: What is the installation path / Docker image?
- SQ2.4: Does it work as of 2026-10-02? Any breaking changes?
- SQ2.5: Any deprecation notices or known issues?

### Task 3: Alternative Free Compute Hosts Survey
For EACH of: Fly.io, Koyeb, Render, Glitch, Replit, Deta Space, Northflank, Val Town, Deno Deploy, Cloudflare Workers/Pages, GitHub Codespaces, Gitpod, Google Colab, Kaggle Notebooks, SageMaker Studio Lab, CodeSandbox:
- SQ3.1: Credit card required at signup? (Y/N)
- SQ3.2: Free tier specs (CPU, RAM, storage, bandwidth)
- SQ3.3: Sleep/idle policy
- SQ3.4: Persistence model (what survives restart)
- SQ3.5: Outbound network restrictions
- SQ3.6: ToS red flags for 24/7 background processes
- SQ3.7: Free tier only (no expiring trials)?

### Task 4: Alternative Automation Engines
For EACH of: Windmill, Activepieces, Node-RED, Apache Airflow, Prefect, Dagster, Temporal, Dagu, Tork:
- SQ4.1: Can it run in constrained containers (≤16GB RAM, limited CPU)?
- SQ4.2: Resource requirements (min RAM, CPU)
- SQ4.3: Persistence requirements (DB needed?)
- SQ4.4: Free/self-hosted licensing
- SQ4.5: Complexity to deploy on free tiers

### Task 5: Free Persistent Storage Options
For EACH of: HF Datasets (private), GitHub repos via API, Supabase, Neon, Turso, Cloudflare R2, Backblaze B2:
- SQ5.1: Free tier limits (storage, requests, bandwidth)
- SQ5.2: Private data support
- SQ5.3: API access (programmatic)
- SQ5.4: Persistence guarantees
- SQ5.5: Credit card required?

### Task 6: Free Secret Management
For EACH of: GitHub Secrets, HF Spaces secrets, Doppler, Infisical:
- SQ6.1: Free tier limits (secrets count, projects, team members)
- SQ6.2: Programmatic access (API/CLI)
- SQ6.3: Integration with target platforms
- SQ6.4: Credit card required?

## Ideal Answer Structure
A markdown report with:
1. Findings tables for each of the 6 tasks
2. Ranked shortlist of viable stacks scored against hard constraints
3. Every claim cited to a source (URL + date accessed)
4. "NEEDS VERIFICATION" markers for unconfirmed items

## Keyword Variations / Search Clusters
- "Hugging Face Spaces free tier RAM 2024 2025 2026"
- "Hugging Face Spaces sleep policy background process"
- "Hugging Face Spaces persistent storage limit"
- "Hugging Face Spaces terms of service background jobs"
- "Hugging8n GitHub n8n Hugging Face Spaces"
- "free cloud hosting no credit card 2024 2025 2026"
- "Fly.io free tier credit card required"
- "Koyeb free tier no credit card"
- "Render free tier sleep policy"
- "Glitch free tier 2024"
- "Replit free tier always on"
- "Deta Space shutdown"
- "Northflank free tier"
- "Val Town free tier"
- "Deno Deploy free tier limits"
- "Cloudflare Workers free tier limits"
- "GitHub Codespaces free hours per month"
- "Gitpod free tier"
- "Google Colab persistent runtime"
- "Kaggle Notebooks persistent storage"
- "SageMaker Studio Lab free tier"
- "CodeSandbox free tier"
- "Windmill self-hosted requirements RAM"
- "Activepieces self-hosted Docker"
- "Node-RED Docker RAM requirements"
- "Airflow minimal requirements"
- "Prefect self-hosted free"
- "Dagster self-hosted"
- "Temporal self-hosted requirements"
- "Dagu workflow engine"
- "Tork workflow engine"
- "Hugging Face Datasets private storage limit"
- "GitHub API storage limits free"
- "Supabase free tier Postgres storage"
- "Neon free tier Postgres"
- "Turso free tier libSQL"
- "Cloudflare R2 free tier"
- "Backblaze B2 free tier 10GB"
- "GitHub Secrets free tier limits"
- "Hugging Face Spaces secrets"
- "Doppler free tier secrets"
- "Infisical free tier"