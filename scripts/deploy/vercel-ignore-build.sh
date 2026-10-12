#!/usr/bin/env bash
# Vercel "Ignored Build Step" (vercel.json -> ignoreCommand).
#
# Philosophy: we merge to main often (ship fast / fail fast). Most merges
# touch docs, harness, Python, or tests — none of which change the site
# bundle or the api/ functions. Rebuilding production for those merges
# wastes build minutes and re-ships an identical site.
#
# Contract (Vercel): exit 0 -> build; exit 1 -> skip; anything else -> error
# (treated as build). Safe default is always "build".
#
# Env (set by Vercel on Git-integration builds):
#   VERCEL_GIT_PREVIOUS_SHA  last commit that actually produced a deploy
#                            (empty on first deploy; stays put across skips)
#   VERCEL_GIT_COMMIT_SHA    commit being built
#
# Trigger set = everything that can change the deployed output:
#   index.html, vercel.json, .vercelignore, package.json, package-lock.json,
#   tsconfig*.json, vite.config.*, api/ (Vercel Functions), public/,
#   brand/ (tokens imported by src), packages/design-system/ (aliased in
#   vite.config.ts), src/ (React SPA), data/<dir>/registry.ts (12 aliased
#   site registries; mirrors .vercelignore re-include rules).
#
# Explicit non-triggers: src/ai_company/ (Python), src/__tests__/ (type-
# checked by CI gate, not shipped), everything else (docs, harness, scripts,
# .github, brand static mirrors, data/ non-registry files).
set -euo pipefail

PREV="${VERCEL_GIT_PREVIOUS_SHA:-}"
HEAD="${VERCEL_GIT_COMMIT_SHA:-HEAD}"

if [ -z "$PREV" ] || ! git cat-file -e "${PREV}^{commit}" 2>/dev/null; then
  echo "vercel-ignore-build: no usable previous deploy SHA (PREV='${PREV}'); building."
  exit 0
fi

# Filter out known non-site paths first; || true so an empty diff is not an
# error under set -e. Avoid grep -q in a pipeline with set -o pipefail
# (upstream grep can die of SIGPIPE and fail the script).
changed=$(
  git diff --name-only "$PREV" "$HEAD" \
    | grep -v -e '^src/ai_company/' -e '^src/__tests__/' \
    || true
)

site_pattern='^(index\.html|vercel\.json|\.vercelignore|package\.json|package-lock\.json|tsconfig[^/]*\.json|vite\.config\.[^/]+|api/|public/|brand/|packages/design-system/|src/|data/[^/]+/registry\.ts)'

if printf '%s\n' "$changed" | grep -E -q "$site_pattern"; then
  echo "vercel-ignore-build: site-bundle files changed between ${PREV} and ${HEAD}; building."
  printf '%s\n' "$changed" | grep -E "$site_pattern" | sed 's/^/  - /' | head -n 20
  exit 0
fi

echo "vercel-ignore-build: no site-bundle changes between ${PREV} and ${HEAD}; skipping build."
if [ -n "$changed" ]; then
  echo "Changed files (all non-site):"
  printf '%s\n' "$changed" | sed 's/^/  - /' | head -n 20
fi
exit 1
