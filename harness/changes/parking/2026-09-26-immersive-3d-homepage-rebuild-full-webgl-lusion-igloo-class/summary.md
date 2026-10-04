---
title: "Immersive 3D homepage rebuild - full WebGL (lusion/igloo class)"
slug: "immersive-3d-homepage-rebuild-full-webgl-lusion-igloo-class"
status: "parked"
location: "parking"
phase: "plan"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules: ["src/three", "src/components/ImmersiveStage.tsx", "src/pages/HomePage.tsx", "src/components/home", "src/data/homeImmersiveCopy.ts"]
files: []
tags: ["webgl", "three-js", "homepage", "immersive", "adr-036"]
validation_status: "unknown"
created_at: "2026-09-26"
updated_at: "2026-09-26"
session_id: "3a3864ad-c396-4355-9724-ac04ffa87799"
owner_agent: "jmlus"
claimed_at: "2026-09-26"
---

# Summary

## Outcome

Pending (implementation in progress).

## Decisions

- CEO scope (2026-09-26): homepage rebuild in place; full WebGL like lusion/igloo.
- ADR-036 written: `three` authorized (homepage-only, lazy, gated, ≤250 KB gz chunk); no GSAP/Lenis/R3F; React stays 18; #303 superseded only for `/`.
- Two-layer Lusion architecture: DOM canonical, fixed WebGL stage behind content.
- Parallel ownership: Agent A `src/three/**` + `ImmersiveStage` + `vite.config.ts`; Agent B `HomePage` + `HeroSection` + `src/components/home/**` + `index.css`; Agent C `src/data/homeImmersiveCopy.ts`; orchestrator owns `package.json`/`bun.lock`.

## Validation

- Pending.

## Next Step

- Dispatch A/B/C in parallel; then integrate, run verification plan (lint/test/build/ECL lint/visual), update STATUS, close change.
