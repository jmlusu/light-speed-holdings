import yaml
from collections import Counter

with open('company-registry.yaml') as f:
    data = yaml.safe_load(f)

agents = data.get('company', {}).get('agents', [])
print(f'Total agents: {len(agents)}')

# Check for duplicates after kebab-case conversion
ids = [a['id'] for a in agents]
kebab_ids = [i.replace('_', '-') for i in ids]

# Find duplicates
dup = Counter(kebab_ids)
duplicates = {k: v for k, v in dup.items() if v > 1}
print(f'Duplicates after kebab-case conversion: {duplicates}')

# Board agents
board_agents = [a for a in agents if a.get('type') == 'board']
print(f'Board agents: {[a["id"] for a in board_agents]}')

# Check for any snake_case vs kebab-case in registry
for a in agents:
    if '-' in a['id']:
        print(f'Kebab-case ID in registry: {a["id"]}')

# Print all IDs with their types
for a in agents:
    print(f"  {a['id']}: type={a.get('type', 'N/A')}, reports_to={a.get('reports_to', 'N/A')}")