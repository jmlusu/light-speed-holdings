from ai_company.generator import AgentGenerator

g = AgentGenerator()
files = g.generate_all(clean=True, use_full_registry=False)
print(f"Generated {len(files)} agent files")
