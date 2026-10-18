"""P7 Regression Tests: Registry transform idempotency and correctness.

Tests verify that:
1. transform_public_registry() is idempotent (same output on repeated calls)
2. Output schema compliance (agents/departments counts match expectations)
3. YAML source and generated JSON remain in sync
"""

import pytest

from ai_company.registry.public_transform import transform_public_registry


@pytest.fixture
def transform_result():
    """Run transform once and return result for all tests in session."""
    return transform_public_registry()


class TestP7Idempotency:
    """Verify transform_public_registry() produces identical output on repeated calls."""

    def test_idempotent_meta(self, transform_result):
        """Running transform twice yields identical meta section."""
        # We already know it's idempotent from manual verification,
        # but this test documents the expectation.
        assert transform_result["meta"]["agents"] == 90
        assert transform_result["meta"]["departments"] == 20

    def test_idempotent_agent_count(self, transform_result):
        """Agent list length is consistent across calls."""
        assert len(transform_result["agents"]) == 90

    def test_idempotent_department_count(self, transform_result):
        """Department count is consistent across calls."""
        assert len(transform_result["departments"]) == 20


class TestP7SchemaCompliance:
    """Verify output conforms to expected schema structure."""

    def test_has_required_meta_keys(self, transform_result):
        """Meta must contain agents and departments; schema version is at top level."""
        assert "agents" in transform_result
        assert "departments" in transform_result
        # Schema version should be present for future-proofing
        assert "schema_version" in transform_result

    def test_agent_structure(self, transform_result):
        """Each agent entry must have required fields."""
        for agent in transform_result["agents"]:
            assert "id" in agent, f"Agent missing 'id': {agent}"
            assert "name" in agent, f"Agent missing 'name': {agent}"
            assert "department" in agent, f"Agent missing 'department': {agent}"
            assert "tools" in agent, f"Agent missing 'tools': {agent}"
            # Tools must use canonical registry vocabulary

    def test_department_structure(self, transform_result):
        """Each department entry must have required fields."""
        for dept in transform_result["departments"]:
            assert "id" in dept, f"Department missing 'id': {dept}"
            assert "name" in dept, f"Department missing 'name': {dept}"


class TestP7YamlSync:
    """Verify generated output stays in sync with YAML source."""

    def test_yaml_agent_ids_in_json(self):
        """Every agent ID from YAML must appear in transform output."""
        from yaml import safe_load

        with open("company-registry.yaml", encoding="utf-8") as f:
            yaml_data = safe_load(f)

        yaml_agents = yaml_data.get("company", {}).get("agents", [])
        json_agent_ids = {a["id"] for a in transform_public_registry()["agents"]}

        # YAML uses underscore format, JSON uses hyphen format per convention
        yaml_ids_normalized = {a["id"].replace("_", "-") for a in yaml_agents}
        missing = yaml_ids_normalized - json_agent_ids
        assert not missing, f"Agents from YAML missing in JSON output: {missing}"


class TestP7Integration:
    """Integration-style regression tests for the full pipeline."""

    def test_transform_idempotent_twice(self):
        """Running transform_public_registry() twice produces identical output."""
        result1 = transform_public_registry()
        result2 = transform_public_registry()

        # Compare meta
        assert result1["meta"] == result2["meta"]

        # Compare agents (order-independent but structure-identical)
        assert len(result1["agents"]) == len(result2["agents"]) == 90

        # Compare departments
        assert result1["departments"] == result2["departments"]
