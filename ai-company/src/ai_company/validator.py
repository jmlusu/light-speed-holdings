import yaml
from pathlib import Path

class CompanyValidator:
    def __init__(self, registry_path="company-registry.yaml"):
        self.registry_path = Path(registry_path)
        self.errors = []
        self.warnings = []

    def load_registry(self):
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def validate(self):
        data = self.load_registry()
        agents = data.get('company', {}).get('agents', [])
        ceo = data.get('company', {}).get('ceo', 'human_operator')

        agent_ids = {a['id'] for a in agents}
        agent_map = {a['id']: a for a in agents}

        print(f"Validating {len(agents)} agents...")

        for agent in agents:
            aid = agent['id']

            # Check required fields
            for field in ['id', 'name', 'title', 'department', 'reports_to']:
                if field not in agent or not agent[field]:
                    self.errors.append(f"[{aid}] Missing required field: {field}")

            # Check reports_to exists
            reports_to = agent.get('reports_to', '')
            if reports_to != ceo and reports_to not in agent_ids:
                self.errors.append(f"[{aid}] reports_to '{reports_to}' does not exist in registry")

            # Check direct_reports exist
            for report_id in agent.get('direct_reports', []):
                if report_id not in agent_ids:
                    self.errors.append(f"[{aid}] direct_report '{report_id}' does not exist in registry")

            # Check for self-reporting
            if reports_to == aid:
                self.errors.append(f"[{aid}] Agent cannot report to itself")

        # Check for circular dependencies
        self._check_circular_deps(agent_map, ceo)

        # Print results
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} Warning(s):")
            for w in self.warnings:
                print(f"   {w}")

        if self.errors:
            print(f"\n❌ {len(self.errors)} Error(s):")
            for e in self.errors:
                print(f"   {e}")
            return False
        else:
            print("\n✅ Company structure is valid! No errors found.")
            return True

    def _check_circular_deps(self, agent_map, ceo):
        for start_id in agent_map:
            visited = set()
            current = start_id
            while current and current != ceo:
                if current in visited:
                    self.errors.append(f"Circular dependency detected involving: {start_id}")
                    break
                visited.add(current)
                current = agent_map.get(current, {}).get('reports_to', '')
