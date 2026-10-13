#!/usr/bin/env python3
"""Simple test - try to import just the generator, bypassing pipeline.py issues"""

import sys
sys.path.insert(0, '.')

# Try importing just the generator module, see if pipeline import fails
try:
    from ai_company.generator import AgentGenerator
    print("Generator imported OK")
    
    # Try creating an instance
    g = AgentGenerator()
    print("Generator instance created OK")
    
    # List methods
    methods = [m for m in dir(g) if not m.startswith("_")]
    print(f"Methods: {methods}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()