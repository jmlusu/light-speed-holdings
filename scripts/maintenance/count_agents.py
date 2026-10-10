import yaml

data = yaml.safe_load(open("company-registry.yaml"))
agents = data.get("company", {}).get("agents", [])
print(f"Agents: {len(agents)}")
depts = set(a.get("department") for a in agents if a.get("department"))
print(f"Departments: {len(depts)}")
print(f"Departments list: {sorted(depts)}")
