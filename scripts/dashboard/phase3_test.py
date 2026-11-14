#!/usr/bin/env python
"""Phase 3 test: Vector search and memory pruning."""

import sys

# Add the project to path
sys.path.insert(0, r"C:\Users\jmlus\light-speed-holdings\src")

from ai_company.memory.consolidation import ConsolidationConfig, ConsolidationScheduler
from ai_company.memory.engine import MemoryStore

# Test 1: Memory store has prune and consolidate methods
print("=== Test 1: MemoryStore methods ===")
store = MemoryStore()
print("  has prune:", hasattr(store, "prune"))
print("  has consolidate_all:", hasattr(store, "consolidate_all"))
print("  has enable_vector_search:", hasattr(store, "enable_vector_search"))

# Test 2: Consolidation scheduler
print()
print("=== Test 2: ConsolidationScheduler ===")
config = ConsolidationConfig(tick_interval=50, entry_threshold=500)
scheduler = ConsolidationScheduler(store=store, config=config)
print("  scheduler.on_tick() callable:", callable(scheduler.on_tick))

# Test 5: Enable vector search
print()
print("=== Test 4: Enable vector search ===")
store.enable_vector_search()
print("  Vector search enabled:", store.has_vector_search)

# Test 5: Index entries
print()
print("=== Test 5: Index entries ===")
store.store("episodic", "Test memory content about debugging a Python issue")
store.store("semantic", "Python debugging best practices")
index_count = store._vector_store.index_all()
print("  Entries indexed:", index_count)
print("  Vector search available:", store.has_vector_search)

# Test 6: Recall with vector search
print()
print("=== Test 6: Recall with vector search ===")
results = store.recall("episodic", query="debug", use_semantic=True, limit=5)
print("  Vector recall results:", len(results))

print()
print("=== Phase 3 verification complete ===")
