# Security Audit Report — Light Speed Holdings

**Audit Date:** 2026-09-10
**Scope:** Last 3 commits + uncommitted working tree
**Auditor:** Security Architect (AI)
**Methodology:** Bandit static analysis, manual code review, Three-Tier Boundary System

---

## Executive Summary

| Severity | Count | Key Findings |
|----------|-------|--------------|
| **Critical** | 1 | Generator uses Jinja2 with `autoescape=False` — XSS in generated agent markdown |
| **High** | 5 | SSRF vulnerabilities via `urllib.request.urlopen` with user-controlled URLs (4 locations) |
| **Medium** | 12 | SQL injection vectors via string-based query construction (7 files) |
| **Low** | 8 | Missing security hardening, placeholder secrets, information disclosure |

**Overall Risk:** **HIGH** — Multiple exploitable SSRF vectors and XSS in agent generation pipeline require immediate remediation.

---

## Three-Tier Boundary System Assessment

### ✅ Always Do Checks (Passing)
- [x] HTTPS enforcement via HSTS (configurable)
- [x] Security headers (CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- [x] Password hashing not applicable (API key auth)
- [x] Audit logging for auth failures and rate limits
- [x] `httpOnly` cookies not used (stateless API key auth)

### ⚠️ Ask First Areas (Needs Review)
- [ ] **CORS changes** — `DASHBOARD_CORS_ORIGINS` allows comma-separated origins; wildcard `*` is rejected but custom origins need review
- [ ] **File uploads** — No file upload endpoints found in current codebase
- [ ] **New auth flows** — RBAC is solid; session tokens (ADR-013) need penetration testing
- [ ] **Sensitive data handling** — Memory encryption uses AES-256-GCM with HKDF key derivation ✅

### ❌ Never Do Violations (Found)
- [x] **Secrets in code** — No hardcoded secrets found in source; `.env` is gitignored ✅
- [x] **`eval()`/`innerHTML` with user data** — Dashboard uses Alpine.js `x-html` with server-rendered data; needs review
- [ ] **Disabled security headers** — Headers are enabled by default ✅

---

## Detailed Findings

### CRITICAL: XSS in Agent Generator (generator.py:72)

**Location:** `src/ai_company/generator.py:72-76`

```python
self.env = Environment(
    loader=FileSystemLoader(str(self.templates_dir)),
    keep_trailing_newline=True,
    autoescape=False,  # DANGEROUS
)
```

**Impact:** Generated agent markdown files (`.opencode/agents/*.md`) are rendered by OpenCode. If agent registry contains malicious content in fields like `description`, `mission`, `responsibilities`, it could inject HTML/JS into the agent cards.

**Attack Vector:** Malicious `company-registry.yaml` entry → generated `.md` file → rendered in OpenCode UI or dashboard.

**Remediation:**
```python
from jinja2 import select_autoescape
self.env = Environment(
    loader=FileSystemLoader(str(self.templates_dir)),
    keep_trailing_newline=True,
    autoescape=select_autoescape(['html', 'xml', 'md']),  # or True for all
)
```

**Note:** Since output is Markdown (not HTML), `autoescape=True` may over-escape. Use `select_autoescape(['html', 'xml'])` or implement custom Markdown-safe escaping.

---

### HIGH: SSRF via Unrestricted `urlopen()` (4 Locations)

#### 1. Executor Tool Runner — `webfetch` tool (tool_runner.py:863)
```python
with urllib.request.urlopen(url, timeout=30) as resp:
```
**Validation:** Only checks `url.startswith(("http://", "https://"))` — **allows internal IPs, localhost, metadata services**

#### 2. Bootstrap Dev Setup — Ollama check (dev_setup.py:395)
```python
with urllib.request.urlopen(f"{host}/api/tags", timeout=3) as resp:
```
**Source:** `host` from `OLLAMA_HOST` env var (default `http://localhost:11434`)

#### 3. FX Rate Service (fx_rate.py:83)
```python
with urllib.request.urlopen(req, timeout=5) as resp:
```
**URL:** Hardcoded `https://v6.exchangerate-api.com/...` — **low risk** (fixed external API)

#### 4. CLI Models Check (cli/models.py:98)
```python
resp = urllib.request.urlopen(req, timeout=5)
```
**Source:** Provider `api_base` from `company/models.yaml` — **user-controlled config**

#### 5. Approval Notifier Webhooks (notifier.py:159)
```python
with urlopen(req, timeout=5) as resp:
```
**Source:** `company/config/webhooks.yaml` — **user-controlled config**

**SSRF Risk Matrix:**
| Location | User Control | Internal Network Access | Metadata Service Access |
|----------|--------------|------------------------|------------------------|
| tool_runner `_webfetch` | High (agent tool arg) | ✅ Yes | ✅ Yes (169.254.169.254) |
| dev_setup `_ollama_reachable` | Medium (env var) | ✅ Yes | ✅ Yes |
| cli_models check | Medium (config file) | ✅ Yes | ✅ Yes |
| notifier webhooks | Medium (config file) | ✅ Yes | ✅ Yes |

**Remediation — Implement SSRF Protection:**
```python
# Add to a shared security utility
import ipaddress
from urllib.parse import urlparse

BLOCKED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),      # Loopback
    ipaddress.ip_network("10.0.0.0/8"),        # RFC1918
    ipaddress.ip_network("172.16.0.0/12"),     # RFC1918
    ipaddress.ip_network("192.168.0.0/16"),    # RFC1918
    ipaddress.ip_network("169.254.0.0/16"),    # Link-local (AWS metadata)
    ipaddress.ip_network("::1/128"),           # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),          # IPv6 ULA
]

def validate_url_no_ssrf(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https allowed")
    try:
        ip = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        # Hostname — resolve and check (with timeout)
        import socket
        try:
            ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
        except socket.gaierror:
            raise ValueError("Hostname resolution failed")
    for blocked in BLOCKED_NETWORKS:
        if ip in blocked:
            raise ValueError(f"Access to {blocked} is blocked")
```

---

### MEDIUM: SQL Injection Vectors (7 Files)

All use f-string query construction with user-controlled values. **Current mitigation:** Parameters are passed separately to `fetchone`/`fetchall`/`execute` — **but table/column names are interpolated directly.**

#### 1. audit_store.py (5 locations: lines 312, 358, 422, 426, 430)
```python
where = " AND ".join(filters)  # filters from user input
count_sql = f"SELECT COUNT(*) as cnt FROM ({base})" + (f" WHERE {where}" if where else "")
```

#### 2. task_store.py (lines 301, 331)
```python
cursor = self._db.execute(f"DELETE FROM tasks WHERE {_TEST_TASK_WHERE}")
```

#### 3. etl/extractors/sqlite_extractor.py (line 77)
```python
sql = f"SELECT {col_sql} FROM {self.table}{where_sql} ORDER BY {self.timestamp_column} ASC{limit_sql}"
```

#### 4. etl/loaders/sqlite_loader.py (lines 75, 166, 177)
```python
sql = f"INSERT INTO {self.table} ({col_list}) VALUES ({placeholders})"
```

#### 5. etl/pipelines/governance.py (line 69)
```python
f"SELECT COUNT(*) as cnt FROM {table} WHERE {ts_col} < ? AND {ts_col} != ''"
```

#### 6. data/kpi_pipeline.py (bandit flagged but uses params)

**Risk Assessment:** Table/column names come from internal constants (`_TEST_TASK_WHERE`, `self.table`, etc.) — **LOW exploitability** but violates secure coding standards.

**Remediation:** Use allow-lists for table/column names or validate against schema:
```python
ALLOWED_TABLES = {"audit_events", "tasks", "cost_records", "kpi_snapshots"}
assert table in ALLOWED_TABLES, f"Table {table} not allowed"
```

---

### MEDIUM: Dashboard Template XSS Risk (base.html)

**Locations:** `base.html` lines 150-155, 266, 478-484

```html
<div class="command-bar-result-icon" :class="result.entity_type" x-html="getIcon(result.entity_type)"></div>
<div class="command-bar-result-title" x-html="highlightMatch(result.title, query)"></div>
<div class="command-bar-result-description" x-html="highlightMatch(result.description, query)"></div>
```

**Risk:** Alpine.js `x-html` renders raw HTML. If `result.title`, `result.description`, or `getIcon()` return user-controlled data with HTML, XSS executes.

**Data Source:** Command bar search results come from backend API (`/api/v1/command-bar/search`). Need to verify server-side sanitization.

**Remediation:**
- Use `x-text` instead of `x-html` where possible
- Sanitize server-side with `bleach` or similar
- Implement Content Security Policy with `'unsafe-inline'` removed (currently required for Alpine.js)

---

### LOW: Placeholder Secrets in .env.example

**File:** `.env.example` contains empty values — **acceptable** as template.

**But:** `.env` file exists in working tree (2977 bytes). **Verify it's gitignored:**
```bash
git check-ignore .env  # Should return .env
```

**Status:** ✅ `.gitignore` contains:
```
# Secrets — never commit
.env
.env.*
!.env.example
!.env.staging.example
```

---

### LOW: Encryption Key Management

**File:** `src/ai_company/security/encryption_key_manager.py`

**Strengths:**
- HKDF-SHA256 key derivation ✅
- AES-256-GCM for encryption ✅
- Dual-key rotation window ✅
- Keys encrypted at rest with secondary derivation ✅
- Master secret from env vars (`MEMORY_ENCRYPTION_KEY` or `JWT_SECRET_KEY`) ✅

**Concern:** Line 125 uses `secrets.token_bytes(16)` as salt — good. But key derivation mixes salt with master secret in HKDF, which is correct.

---

### LOW: Prompt Injection Protection

**File:** `src/ai_company/security/content_filter.py`

**Strengths:**
- Regex patterns for injection detection ✅
- Execution attempt blocking ✅
- XSS pattern detection ✅
- Security audit logging ✅

**Gaps:**
- Only scans **output**, not input (prompt injection happens at input)
- No integration with LLM client — `content_filter.scan()` not called in `LLMClient.execute_task()`

**Recommendation:** Add input scanning in `LLMClient.execute_task()` before sending to provider.

---

### LOW: CORS Configuration (app.py:427-442)

```python
_DEFAULT_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]
origins_raw = os.environ.get("DASHBOARD_CORS_ORIGINS", "")
origins = [o.strip() for o in origins_raw.split(",") if o.strip()]
if not origins:
    origins = _DEFAULT_ORIGINS
if "*" in origins:
    logger.warning("DASHBOARD_CORS_ORIGINS contained '*'; ignoring wildcard for security.")
    origins = [o for o in origins if o != "*"]
```

**Assessment:** Secure defaults, wildcard rejected. **Risk:** If `DASHBOARD_CORS_ORIGINS` is misconfigured with a broad domain (e.g., `https://*.example.com`), it could expose API. Consider validating origin format.

---

### LOW: RBAC Implementation (security/rbac.py)

**Strengths:**
- Three-tier roles (run < approve < admin) ✅
- Fail-closed default (`api_key` mode) ✅
- Loopback-only for `open` mode (ADR-012) ✅
- Session tokens IP-bound (ADR-013) ✅
- Key verification on startup (`verify_keys()`) ✅
- Placeholder detection ✅

**Gap:** No rate limiting on auth attempts (but dashboard has global rate limiter).

---

## Bandit Summary (High/Medium Only)

| File | Severity | Confidence | Issue |
|------|----------|------------|-------|
| generator.py:72 | HIGH | HIGH | Jinja2 `autoescape=False` |
| tool_runner.py:863 | MEDIUM | HIGH | `urlopen` with user URL |
| notifier.py:159 | MEDIUM | HIGH | `urlopen` with config URL |
| dev_setup.py:395 | MEDIUM | HIGH | `urlopen` with env var URL |
| fx_rate.py:83 | MEDIUM | HIGH | `urlopen` (fixed URL — low risk) |
| cli/models.py:98 | MEDIUM | HIGH | `urlopen` with config URL |
| audit_store.py (5x) | MEDIUM | LOW | SQL string construction |
| task_store.py (2x) | MEDIUM | LOW/MEDIUM | SQL string construction |
| etl/extractors/sqlite_extractor.py | MEDIUM | LOW | SQL string construction |
| etl/loaders/sqlite_loader.py (3x) | MEDIUM | LOW | SQL string construction |
| etl/pipelines/governance.py | MEDIUM | LOW | SQL string construction |

---

## Remediation Priority

### P0 — Immediate (This Week)
1. **Fix generator.py autoescape** — Enable Jinja2 autoescape or use safe template rendering
2. **Implement SSRF protection** — Add `validate_url_no_ssrf()` utility and apply to all 5 `urlopen` locations
3. **Add input validation for webfetch tool** — Block private IPs, metadata endpoints

### P1 — This Sprint
4. **Parameterize SQL queries** — Replace f-string table/column interpolation with allow-lists
5. **Integrate content_filter** — Scan LLM inputs in `LLMClient.execute_task()`
6. **Review Alpine.js x-html usage** — Replace with `x-text` or sanitize server-side

### P2 — Next Sprint
7. **Add origin validation** to CORS config
8. **Penetration test** RBAC + session token flow
9. **Add security headers test** to CI pipeline
10. **Document key rotation procedure** (see `scripts/rotate-secrets.py` and `docs/DASHBOARD_KEY_ROTATION.md`)

---

## Security Test Recommendations

```bash
# 1. Run bandit on every CI build
uv run bandit -r src/ -f json -o bandit-report.json

# 2. Check for secrets in git history (run periodically)
git log --all --oneline --grep="secret\|key\|password\|token"

# 3. Verify .env gitignore
git check-ignore .env && echo "OK" || echo "MISSING"

# 4. Test SSRF protection (manual)
curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" http://localhost:8420/api/v1/webfetch?url=http://169.254.169.254/latest/meta-data/

# 5. Test XSS in command bar (manual)
# Inject <script>alert(1)</script> via search API and verify it's escaped

# 6. Verify RBAC key verification
uv run python -c "from ai_company.security.rbac import verify_keys; verify_keys()"
```

---

## Appendix: Files Requiring Security Review

| File | Reason |
|------|--------|
| `src/ai_company/generator.py` | XSS via autoescape=False |
| `src/ai_company/executor/tool_runner.py` | SSRF in webfetch |
| `src/ai_company/orchestrator/notifier.py` | SSRF in webhooks |
| `src/ai_company/bootstrap/dev_setup.py` | SSRF in Ollama check |
| `src/ai_company/cli/models.py` | SSRF in provider check |
| `src/ai_company/data/audit_store.py` | SQL injection vectors |
| `src/ai_company/data/task_store.py` | SQL injection vectors |
| `src/ai_company/data/etl/` | SQL injection vectors (4 files) |
| `src/ai_company/dashboard/templates/base.html` | XSS via x-html |
| `src/ai_company/llm/client.py` | Missing input content filtering |
| `src/ai_company/security/content_filter.py` | Not integrated with LLM client |

---

**End of Report**
*Generated by Security Architect agent — review findings with human security team before production deployment.*
