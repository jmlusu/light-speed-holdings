import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class AgentGenerator:
    def __init__(self, registry_path="company-registry.yaml", output_dir=".opencode/agents"):
        self.registry_path = Path(registry_path)
        self.output_dir = Path(output_dir)
        self.env = Environment(loader=FileSystemLoader("templates"))
        self.template = self.env.get_template("agent.md.j2")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_registry(self):
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found at: {self.registry_path.absolute()}")
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def generate_all(self):
        data = self.load_registry()
        agents = data.get('company', {}).get('agents', [])
        print(f"🚀 Generating {len(agents)} agents for {data['company']['name']}...")
        for agent in agents:
            self._generate_agent(agent)
        print("✅ Generation complete! Check the .opencode/agents directory.")

    def _generate_agent(self, agent_data):
        rendered = self.template.render(**agent_data)
        output_file = self.output_dir / f"{agent_data['id']}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"  📝 Generated: {output_file}")
