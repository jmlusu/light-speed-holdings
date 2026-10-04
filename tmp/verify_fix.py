import os
from ai_company.generator import AgentGenerator

gen = AgentGenerator()
gen.generate_all(use_full_registry=False)

agents_dir = '.opencode/agents'
md_files = [f for f in os.listdir(agents_dir) if f.endswith('.md')]
print(f'Total MD files: {len(md_files)}')

# Check board-chair specifically
board_chair_file = os.path.join(agents_dir, 'board-chair.md')
if os.path.exists(board_chair_file):
    with open(board_chair_file, encoding='utf-8') as f:
        content = f.read()
    print('board-chair.md exists!')
    # Check for reports_to
    if 'reports_to' in content.lower():
        print('  - reports_to field is present')
    else:
        print('  - WARNING: reports_to field missing')
    
    # Show the frontmatter reports_to
    import yaml
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
        rpt = frontmatter.get('reports_to', 'MISSING')
        print(f'  - Frontmatter reports_to: {rpt}')
else:
    print('board-chair.md NOT found')
    print('Available files with board:')
    for f in md_files:
        if 'board' in f:
            print(f'  {f}')