import yaml
data = yaml.safe_load(open('company-registry.yaml'))
agents = data.get('company', {}).get('agents', [])
print(f'Total agents in YAML: {len(agents)}')
for a in agents:
    aid = a.get('id', '')
    aname = a.get('name', '')
    atype = a.get('type', '')
    arreports = a.get('reports_to', 'MISSING')
    if 'board' in aname.lower() or 'chair' in aname.lower() or 'board' in str(atype).lower():
        print(f'  {aid}: {aname}, type: {atype}, reports_to: {arreports}')
# Also print all agent IDs to find board-chair
print('\nAll agent IDs:')
for a in agents:
    print(f'  {a.get("id")}')