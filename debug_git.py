import subprocess
import os

# Check git log for memory/ and inbox changes
result = subprocess.run(
    ['git', 'log', '--oneline', '--since=2026-09-01', '--', 'memory/', '.opencode/inbox.json', 'company-registry.yaml'],
    capture_output=True, text=True, cwd=r'.'
)
print('Git log for key files:')
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr)

# Also check when vector index grew
result2 = subprocess.run(
    ['git', 'log', '--oneline', '--since=2026-09-01', '--', 'memory/vector_index/'],
    capture_output=True, text=True, cwd=r'.'
)
print('Git log for vector_index:')
print(result2.stdout)
if result2.stderr:
    print('STDERR:', result2.stderr)

# Check diff of vector index
result3 = subprocess.run(
    ['git', 'diff', '--stat', 'memory/vector_index.json'],
    capture_output=True, text=True, cwd=r'.'
)
print('Git diff stat for vector_index.json:')
print(result3.stdout)
if result3.stderr:
    print('STDERR:', result3.stderr)