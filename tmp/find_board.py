from ai_company.registry import load_registry
reg = load_registry()
# Find and update the board-chair entry
# Check all entries for board-related ones
for i, exec in enumerate(reg.executives):
    if 'board' in exec.name.lower() or exec.id == 'board_chair':
        print(f'Found executive: {exec.id}: {exec.name}, reports_to: {exec.reports_to}')
for i, spec in enumerate(reg.specialists):
    if 'board' in spec.name.lower() or 'chair' in spec.name.lower():
        print(f'Found specialist: {spec.id}: {spec.name}, reports_to: {spec.reports_to}, dept: {spec.department}')