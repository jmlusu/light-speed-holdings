# Fire-and-forget wrapper for `graphify update` used by the post-commit hook.
# The synchronous version takes ~27 min; if the hook process is killed before
# pre-commit's stash-restore runs, every unstaged edit in the worktree is
# silently reverted (data loss). Spawning detached lets the hook exit in <1s
# so the restore always completes; the graph still rebuilds in the background.
$root = Split-Path -Parent $PSScriptRoot
if (Get-Process -Name graphify -ErrorAction SilentlyContinue) {
    Write-Host "[graphify-rebuild] update already running; skipping"
    exit 0
}
Start-Process -FilePath "uv" -ArgumentList "run", "graphify", "update", "." `
    -WorkingDirectory $root -WindowStyle Hidden
Write-Host "[graphify-rebuild] spawned background graphify update"
exit 0
