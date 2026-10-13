#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from ai_company.generator import AgentGenerator

g = AgentGenerator()
print('Generator imported successfully')
print(f'Methods: {[m for m in dir(g) if not m.startswith("_")]}')