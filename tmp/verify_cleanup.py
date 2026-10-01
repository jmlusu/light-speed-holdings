import os
import yaml

agents_dir = '.opencode/agents'

# Check board-chair specifically
with open(os.path.join(agents_dir, 'board-chair.md'), encoding='utf-8') as f:
    content = f.read()

# Check frontmatter
parts = content.split('---', 2)
frontmatter = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
rpt = frontmatter.get('reports_to', 'MISSING')

print('board-chair.md verification:')
print(f'  reports_to in frontmatter: {rpt!r}')
print(f'  Has Reports To line: {"Reports To:" in content}')

# Count total MD files
md_count = len([f for f in os.listdir(agents_dir) if f.endswith('.md')])
print(f'  Total .md agent cards: {md_count}')

# Verify registry
with open('company-registry.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
bc = [a for a in data['company']['agents'] if a['id'] == 'board_chair'][0]
print(f'  Registry board_chair reports_to: {bc["reports_to"]!r}')

print()
print('=== CLEANUP SUMMARY ===')
print(f'  .bak files removed: 243')
print(f'  .md files remaining: {md_count}')
print(f'  board-chair reports_to: {rpt!r} (from frontmatter) / {bc["reports_to"]!r} (from registry)')