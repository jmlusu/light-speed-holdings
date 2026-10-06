import yaml
import os

with open(r'C:\Users\jmlus\light-speed-holdings\company-registry.yaml') as f:
    data = yaml.safe_load(f)
agents = data['company']['agents']
types = {}
for a in agents:
    t = a['type']
    types[t] = types.get(t, 0) + 1
print('Agent type distribution:', types)
print(f'Total agents: {len(agents)}')