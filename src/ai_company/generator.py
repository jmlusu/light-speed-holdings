import yaml
from jinja2 import Environment, DictLoader
from pathlib import Path

AGENT_TEMPLATE_STR = """---
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

## Standard Operating Procedures (SOP)

### Checking Your Inbox
Before taking action, always check your inbox for pending tasks:

    python -m ai_company.cli inbox --agent {{ id }}

### Delegating a Task
If a task requires subordinates, delegate it immediately:

    python -m ai_company.cli delegate --sender {{ id }} --receiver "[SUBORDINATE_ID]" --instruction "[YOUR_INSTRUCTION]"

### Completing a Task
When you finish a task, record your findings and mark it complete:

    python -m ai_company.cli complete --task-id "[TASK_ID]" --result "[YOUR_RESULT_SUMMARY]"

"""

class AgentGenerator:
    def __init__(self, registry_path="company-registry.yaml", output_dir=".opencode/agents"):
        self.registry_path = Path(registry_path)
        self.output_dir = Path(output_dir)
        self.env = Environment(loader=DictLoader({"agent.md": AGENT_TEMPLATE_STR}))
        self.template = self.env.get_template("agent.md")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_registry(self):
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found at: {self.registry_path.absolute()}")
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def generate_all(self):
        data = self.load_registry()
        agents = data.get('company', {}).get('agents', [])
        print(f"Generating {len(agents)} agents for {data['company']['name']}...")
        for agent in agents:
            self._generate_agent(agent)
        print("Generation complete! Agents now include SOP instructions.")

    def _generate_agent(self, agent_data):
        rendered = self.template.render(**agent_data)
        output_file = self.output_dir / f"{agent_data['id']}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"  Generated: {output_file}")
