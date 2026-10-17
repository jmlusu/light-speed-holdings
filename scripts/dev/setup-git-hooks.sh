#!/usr/bin/env bash
# Register the custom "ours_lockfile" merge driver so lockfiles always keep the
# local copy during merges. This is the local, per-developer half of the
# .gitattributes rules (cats .gitattributes cannot install the driver itself).
#
# Notes:
#   - Applies to the repo the script is run from (git config is local unless
#     --global is added).
#   - On macOS/Linux/WSL run: bash scripts/setup-git-hooks.sh
#   - The driver keeps the LOCAL version of bun.lock / uv.lock when AI Studio
#     syncs get merged back through OpenCode (ADR-024).
set -e

echo "Setting up custom Git merge drivers for lockfiles..."
git config merge.ours_lockfile.name "Keep local lockfile during merges"
git config merge.ours_lockfile.driver "git merge-file --ours %A %O %B"
echo "Git merge drivers successfully configured."
echo
echo "Verify with:"
echo "  git config --get merge.ours_lockfile.driver"
echo "  git check-attr merge -- bun.lock uv.lock"
