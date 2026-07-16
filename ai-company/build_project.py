import os

print("🚀 Building Light Speed Holdings AI Company...")

# 1. Create Required Directories
os.makedirs('templates', exist_ok=True)
os.makedirs('.opencode/agents', exist_ok=True)
os.makedirs('src/ai_company/models', exist_ok=True)
os.makedirs('src/ai_company', exist_ok=True)

# 2. Create company-registry.yaml
with open('company-registry.yaml', 'w', encoding='utf-8') as f:
    f.write("""company:
  name: Light Speed Holdings
  agents:
    - id: chief_of_staff
      name: Chief of Staff
      title: Chief of Staff
      description: The primary orchestrator and strategic alignment agent.
      department: Executive
      reports_to: CEO
      direct_reports: [cto]
      responsibilities:
        - Align company goals across all departments.
        - Orchestrate agent communication.
      guidelines: Maintain high-level strategic oversight.
      tools: [read, write, execute, delegate]
    - id: cto
      name: Chief Technology Officer
      title: CTO
      description: Oversees all technological infrastructure.
      department: Technology
      reports_to: Chief of Staff
      responsibilities:
        - Architect robust AI agent systems.
        - Ensure system scalability and security.
      guidelines: Prioritize clean, maintainable code.
      tools: [read, write, execute, code_interpreter]
""")
print("✅ Created company-registry.yaml")

# 3. Create templates/agent.md.j2
with open('templates/agent.md.j2', 'w', encoding='utf-8') as f:
    f.write("""---
name: {{ name }}
description: {{ description }}
tools: {{ tools | default([]) | tojson }}
---

# {{ title }}

You are the {{ title }} at Light Speed Holdings. 

## Core Responsibilities
{% for responsibility in responsibilities | default([]) %}
- {{ responsibility }}
{% endfor %}

## Reporting Structure
- **Reports To**: {{ reports_to | default('CEO') }}
- **Direct Reports**: {{ direct_reports | default([]) | join(', ') if direct_reports else 'None' }}

## Behavioral Guidelines
{{ guidelines | default('Maintain professional standards and execute tasks efficiently.') }}
""")
print("✅ Created templates/agent.md.j2")

# 4. Create src/ai_company/generator.py
with open('src/ai_company/generator.py', 'w', encoding='utf-8') as f:
    f.write("""import yaml
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
""")
print("✅ Created src/ai_company/generator.py")

# 5. Create src/ai_company/cli.py
with open('src/ai_company/cli.py', 'w', encoding='utf-8') as f:
    f.write("""import click
from ai_company.generator import AgentGenerator

@click.group()
def cli():
    \"\"\"Light Speed Holdings AI Company Builder CLI.\"\"\"
    pass

@cli.command()
def generate():
    \"\"\"Generate all OpenCode agent files from the registry.\"\"\"
    generator = AgentGenerator()
    generator.generate_all()

if __name__ == '__main__':
    cli()
""")
print("✅ Created src/ai_company/cli.py")

print("\n🎯 Setup complete!")
