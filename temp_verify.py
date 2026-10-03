import sys
sys.path.insert(0, '.')
from ai_company.generator import AgentGenerator
gen = AgentGenerator()
errors = gen.validate_generated()
print(f'Validation errors: {len(errors)}')
for e in errors[:10]:
    print(e)