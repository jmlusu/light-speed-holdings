# Organizational Communication: Application Naming, Ownership, and Port Assignments

**Date:** October 10, 2026
**From:** Chief Strategy Officer
**To:** All Teams
**Subject:** Critical - Application Naming, Ownership, and Port Assignments

## Overview

This communication establishes definitive ownership, naming conventions, and port assignments for two critical applications within our organization. **All teams must align on these distinctions to prevent deployment conflicts, misconfigured health checks, and runtime errors.**

---

## 1. Application Renaming

| Previous Name | New Name | Owner |
|---|---|---|
| Vite Application | **Marketing Site** | **Chief Marketing Officer** |

The Vite-based React application is now officially referred to as the **Marketing Site** across all documentation, monitoring, and internal communications.

---

## 2. Port Assignments

### Marketing Site (Vite/React)

| Purpose | Port | Launch Method | Notes |
|---|---|---|---|
| Development server | **1441** | `pm2 start ecosystem.config.cjs` | Vite dev server |
| Preview server | **1440** | `pm2 start ecosystem.config.cjs` | `vite preview` production build |

**⚠️ Critical:** Ports 1440 and 1441 are **exclusively** for the Marketing Site. These are the only ports the Marketing Site may bind.

### CEO Dashboard (Internal)

| Purpose | Port | Runtime | Notes |
|---|---|---|---|
| FastAPI/uvicorn | **8420** (production) / **8421** (development) | FastAPI/uvicorn | CEO Dashboard - internal application |
| Health check | `/health` (JSON endpoint) | FastAPI | Never use Marketing Site ports for this |

**⚠️ Critical:** Ports 8420 and 8421 are **exclusively** for the CEO Dashboard. The Marketing Site must never bind to these ports.

---

## 3. Application Independence

The **CEO Dashboard** and the **Marketing Site** are two independent applications with:

| Aspect | CEO Dashboard | Marketing Site |
|---|---|---|
| **Runtime** | FastAPI/uvicorn | Vite/React (Node.js) |
| **Server** | uvicorn-based FastAPI | PM2 + Node.js |
| **Health Check** | `GET /health` (JSON) | Root `/` (SPA) |
| **Production Port** | **8420** | N/A (deployed to Vercel) |
| **Development Port** | **8421** | **1441** (dev), **1440** (preview) |
| **Deploy Target** | Internal infrastructure | Vercel (lightspeedholdings.vercel.app) |
| **CORS Allowlist** | Separate, internal origins | Separate, external origins |

**⚠️ Critical Rule: Never serve one application on the other's assigned port.**

---

## 4. Enforced Standards

### 4.1 Port Assignment Rules

1. **Marketing Site** may only bind to ports **1440** and **1441**
2. **CEO Dashboard** may only bind to ports **8420** and **8421**
3. No other application may bind to these ports
4. Port assignments are final - do not reconfigure without explicit authorization

### 4.2 Runtime Separation

1. The CEO Dashboard (FastAPI/uvicorn) and Marketing Site (Vite/React) are **distinct runtimes**
2. They have **separate health check endpoints** and monitoring
3. They have **separate deploy targets** and release cycles
4. They operate in **different network domains** (internal vs. external)

### 4.3 Deployment Protocol

1. **Marketing Site deployments** use `pm2 start ecosystem.config.cjs` on ports 1440/1441
2. **CEO Dashboard deployments** use uvicorn on ports 8420/8421
3. **Never** attempt to start the Marketing Site on ports 8420/8421
4. **Never** attempt to start the CEO Dashboard on ports 1440/1441

---

## 5. Verification Checklist

Before any deployment or configuration change, verify:

- [ ] Marketing Site dev server on port 1441 (not 8420/8421)
- [ ] Marketing Site preview server on port 1440 (not 8420/8421)
- [ ] CEO Dashboard on port 8420/8421 (not 1440/1441)
- [ ] PM2 ecosystem.config.cjs references correct port assignments
- [ ] vite.config.ts `server.port: 1441` and `preview.port: 1440`
- [ ] Dashboard FastAPI configuration uses port 8420/8421
- [ ] No port conflicts between applications

---

## 6. Escalation Path

If a port conflict is suspected or an application is found running on an incorrect port:

1. **Immediate:** Stop the misconfigured application
2. **Same day:** Coordinate with the Chief of Staff
3. **Within 24 hours:** Chief Strategy Officer review and resolution
4. **Document:** Record the incident and corrective actions

---

## 7. Acknowledgment

All team leads and department heads must confirm receipt and understanding of this communication by replying to the Chief of Staff within 48 hours.

**Questions?** Contact the Chief Strategy Officer or Chief of Staff.

---

## Revision History

| Date | Version | Author | Change |
|---|---|---|---|
| 2026-10-10 | 1.0 | Chief Strategy Officer | Initial issuance |
