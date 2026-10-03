import yaml
from ai_company.registry.loader import load_yaml_cached
from pathlib import Path

# Load the registry data the same way the generator does
registry_path = Path('company-registry.yaml')
data = load_yaml_cached(registry_path)

# Get the agents like the generator does
agents = data.get("company", {}).get("agents", [])

# Find board_chair
for agent in agents:
    if agent.get("id") == "board_chair":
        print("board_chair agent dict:")
        for k, v in agent.items():
            print(f"  {k!r}: {v!r}")
        # Now simulate what template.render() would receive
        print(f"\nreports_to in agent dict: {agent.get('reports_to', 'NOT PRESENT')!r}")
        print(f"bool(reports_to): {bool(agent.get('reports_to'))!r}")
        break