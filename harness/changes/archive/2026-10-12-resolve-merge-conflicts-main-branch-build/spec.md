# Specification

**Change**: Resolve merge conflicts for main branch build

**Summary**: Resolve 8 merge conflicts across source files with canonical LightSpeed implementations.

**ECL Gates**:
- HITL Expiry Sweep: pass
- Approval Gate: pass
- Dashboard RBAC: pass
- Brand Curation: pass

**Technical Details**:
- check_port.py: LightSpeed ports 1441/1440 (per AGENTS.md §12)
- AGENT-REGISTRY-TABLE.md: generation date 2026-10-11
- App.tsx: route components Architecture, Build, OfferB, OfferC, OfferE
- FloatingNav.tsx: HAOMTGV Governance Framework overlay
- utils.ts: cn() function with clsx/tailwind-merge
- UseCaseDetailPage.tsx: @lightspeed/data/* canonical imports
- start_vite.bat: npx vite launch
- conftest.py: data root isolation fixture
