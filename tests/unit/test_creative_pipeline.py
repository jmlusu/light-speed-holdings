"""Unit tests for the consolidated creative production engine (Phase 2/3).

Covers: brief contract, routing table + model-route integration, knowledge
warnings, tool adapters, QA gate, human approval gate, persistence, failure
and rerun behaviour. Everything runs offline with tmp directories.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from ai_company.creative import (
    ROUTES,
    AdapterRegistry,
    ApprovalDecision,
    ApprovalStatus,
    ArtifactType,
    ComfyUIAdapter,
    CreativeBrief,
    ExecutionManifest,
    OpenDesignAdapter,
    PresentationAdapter,
    QaResult,
    QaVerdict,
    RunStatus,
    build_chain,
    default_qa,
    default_registry,
    list_runs,
    load_manifest,
    route_brief,
    run_production,
    save_manifest,
    specialist_for,
)
from ai_company.model_router import ModelRouter
from ai_company.paths import get_project_root

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_brief(artifact: ArtifactType = ArtifactType.DECK, **overrides: object) -> CreativeBrief:
    """A brief that satisfies the five-question intake contract."""
    payload: dict[str, object] = {
        "title": "Agentic AI Investor Deck",
        "artifact_type": artifact.value,
        "audience": "SADC institutional investors",
        "objective": "raise a seed round",
        "core_thesis": "Governed agentic AI is the region's next growth lever.",
    }
    payload.update(overrides)
    return CreativeBrief.model_validate(payload)


def write_router_config(tmp_path: Path) -> ModelRouter:
    """Minimal offline ModelRouter: Specialist+medium -> standard tier."""
    config = {
        "providers": {
            "ollama": {
                "backend": "ollama",
                "default_model": "llama3.1-8b-32k",
                "api_base": "http://localhost:11434",
            },
            "openai": {
                "backend": "openai",
                "default_model": "gpt-4o-mini",
                "api_base": "https://api.openai.com/v1",
            },
        },
        "tiers": {
            "fast": {
                "description": "cheap",
                "providers": [{"provider": "ollama", "model": "llama3.1-8b-32k"}],
            },
            "standard": {
                "description": "balanced",
                "providers": [{"provider": "ollama", "model": "llama3.1-8b-32k"}],
            },
            "premium": {
                "description": "best",
                "providers": [{"provider": "openai", "model": "gpt-4o-mini"}],
            },
        },
        "routing": [
            {"agent_type": "Specialist", "priority": "medium", "tier": "standard"},
            {"agent_type": "Specialist", "priority": "high", "tier": "premium"},
            {"context": "approval", "tier": "premium"},
        ],
    }
    config_path = tmp_path / "models.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(yaml.dump(config), encoding="utf-8")
    return ModelRouter(
        config_path=str(config_path),
        registry_path=str(tmp_path / "agent-registry.json"),
    )


def write_project_root(path: Path, with_registry: bool = True) -> Path:
    """Fake project root, optionally with an agent registry listing specialists."""
    if with_registry:
        names = sorted({route.specialist for route in ROUTES.values()} | {"creative-director"})
        (path / "company").mkdir(parents=True, exist_ok=True)
        (path / "company" / "agent-registry.json").write_text(
            json.dumps([{"name": name, "type": "Specialist"} for name in names]),
            encoding="utf-8",
        )
    return path


def offline_registry() -> AdapterRegistry:
    """Presentation adapter wired; OpenDesign/ComfyUI present but unavailable."""
    return AdapterRegistry(
        [
            PresentationAdapter(),
            OpenDesignAdapter(probe=lambda: None),
            ComfyUIAdapter(probe=lambda: False),
        ]
    )


class ExplodingAdapter:
    """Fails on produce — used to exercise failure + rerun."""

    name = "exploding"
    wired = True

    def supports(self, artifact: ArtifactType) -> bool:
        return artifact is ArtifactType.DECK

    def availability(self) -> tuple[bool, str]:
        return True, "pretends to be available"

    def produce(self, brief: CreativeBrief, out_dir: Path) -> list[str]:
        raise RuntimeError("render backend exploded")


# ---------------------------------------------------------------------------
# CreativeBrief contract
# ---------------------------------------------------------------------------


class TestCreativeBrief:
    def test_requires_all_intake_fields(self) -> None:
        with pytest.raises(ValidationError):
            CreativeBrief(
                title="", artifact_type="deck", audience="a", objective="o", core_thesis="t"
            )
        with pytest.raises(ValidationError):
            CreativeBrief(title="Deck", artifact_type="deck", objective="o", core_thesis="t")

    def test_defaults_match_ls_creative_director_contract(self) -> None:
        brief = make_brief()
        assert brief.brand_base == "LightSpeed design system"
        assert brief.visual_language == "lightspeed-design-system"
        assert brief.qa_scope == ["visual", "brand", "ux", "content", "accessibility"]
        assert brief.source_research == []

    def test_production_payload_bridges_presentation_pipeline(self) -> None:
        brief = make_brief(narrative_arc="Hook -> proof -> evidence -> close")
        payload = brief.production_payload()
        assert payload["topic"] == "Agentic AI Investor Deck"
        assert payload["audience"] == brief.audience
        assert payload["objective"] == brief.objective
        assert "next growth lever" in payload["narrative"]
        assert "Hook -> proof" in payload["narrative"]


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


class TestRouting:
    def test_routing_table_covers_every_artifact_type(self) -> None:
        assert set(ROUTES) == set(ArtifactType)

    def test_chain_always_loads_brand_base_first_and_qa_last(self) -> None:
        for artifact in ArtifactType:
            chain = build_chain(artifact)
            assert chain.brand_base == "ls-design-system"
            assert chain.qa_gate == "ls-artifact-qa"
            assert chain.primary == ROUTES[artifact].primary
            assert chain.support == list(ROUTES[artifact].support)

    def test_every_specialist_exists_in_real_agent_registry(self) -> None:
        registry = json.loads(
            (get_project_root() / "company" / "agent-registry.json").read_text(encoding="utf-8")
        )
        names = {agent["name"] for agent in registry}
        for artifact, route in ROUTES.items():
            assert route.specialist in names, (
                f"{artifact.value} specialist '{route.specialist}' unknown"
            )

    def test_route_brief_fills_manifest_from_model_router(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        manifest = route_brief(make_brief(), router=router, project_root=root)

        assert manifest.status is RunStatus.ROUTED
        assert manifest.chain is not None
        assert manifest.agents is not None
        assert manifest.agents.director == "creative-director"
        assert manifest.agents.specialist == specialist_for(ArtifactType.DECK)
        assert manifest.agents.specialist_known is True
        assert manifest.route is not None
        assert manifest.route.tier == "standard"
        assert manifest.route.provider == "ollama"
        assert manifest.route.agent == "product-marketing-manager"
        assert not manifest.warnings

    def test_route_brief_warns_when_specialist_unknown(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root", with_registry=False)
        manifest = route_brief(make_brief(), router=router, project_root=root)
        assert manifest.agents is not None
        assert manifest.agents.specialist_known is False
        assert any("not found in agent registry" in w for w in manifest.warnings)

    def test_route_brief_survives_model_route_failure(self, tmp_path: Path) -> None:
        class ExplodingRouter(ModelRouter):
            def resolve(self, *args: object, **kwargs: object) -> object:
                raise RuntimeError("router down")

        router = ExplodingRouter(
            config_path=str(tmp_path / "missing.yaml"), registry_path=str(tmp_path / "x.json")
        )
        root = write_project_root(tmp_path / "root")
        manifest = route_brief(make_brief(), router=router, project_root=root)
        assert manifest.route is None
        assert any("model route unresolved: router down" in w for w in manifest.warnings)
        assert manifest.status is RunStatus.ROUTED


class TestKnowledgeWorkflowLink:
    def test_content_heavy_brief_without_research_warns(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        manifest = route_brief(
            make_brief(ArtifactType.WHITEPAPER), router=router, project_root=root
        )
        assert any("source_research" in w for w in manifest.warnings)

    def test_missing_research_path_warns(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        brief = make_brief(ArtifactType.WHITEPAPER, source_research=["research/does-not-exist.md"])
        manifest = route_brief(brief, router=router, project_root=root)
        assert any("source_research path not found" in w for w in manifest.warnings)

    def test_existing_research_path_is_accepted(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        (root / "research").mkdir()
        (root / "research" / "seed-evidence.md").write_text("# Evidence", encoding="utf-8")
        brief = make_brief(ArtifactType.WHITEPAPER, source_research=["research/seed-evidence.md"])
        manifest = route_brief(brief, router=router, project_root=root)
        assert not any("source_research" in w for w in manifest.warnings)

    def test_light_artifact_needs_no_research(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        manifest = route_brief(make_brief(ArtifactType.DECK), router=router, project_root=root)
        assert not any("source_research" in w for w in manifest.warnings)


# ---------------------------------------------------------------------------
# Adapters
# ---------------------------------------------------------------------------


class TestAdapters:
    def test_presentation_adapter_only_supports_decks(self) -> None:
        adapter = PresentationAdapter()
        assert adapter.supports(ArtifactType.DECK)
        for artifact in ArtifactType:
            if artifact is not ArtifactType.DECK:
                assert not adapter.supports(artifact)
        available, detail = adapter.availability()
        assert available is True
        assert "local renderer" in detail

    def test_presentation_adapter_produces_brand_token_outputs(self, tmp_path: Path) -> None:
        brief = make_brief(format_hint="keynote")
        outputs = PresentationAdapter().produce(brief, tmp_path / "run")
        assert len(outputs) == 2
        marp = next(p for p in outputs if p.endswith(".md"))
        pptxgen = next(p for p in outputs if p.endswith(".json"))
        assert "deck_keynote" in marp
        assert Path(pptxgen).read_text(encoding="utf-8").upper().count("#DC3641") > 0

    def test_default_registry_selects_presentation_for_decks(self) -> None:
        registry = default_registry()
        chosen = registry.select(ArtifactType.DECK)
        assert isinstance(chosen, PresentationAdapter)
        names = [status.name for status in registry.statuses()]
        assert names == ["presentation", "opendesign", "comfyui"]
        wired = {status.name: status.wired for status in registry.statuses()}
        assert wired["presentation"] is True
        assert wired["opendesign"] is False
        assert wired["comfyui"] is False

    def test_no_wired_adapter_for_website(self) -> None:
        assert offline_registry().select(ArtifactType.WEBSITE) is None

    def test_unavailable_backends_report_reasons(self) -> None:
        registry = offline_registry()
        statuses = {status.name: status for status in registry.statuses()}
        assert statuses["opendesign"].available is False
        assert "not an MVP dependency" in statuses["opendesign"].detail
        assert statuses["comfyui"].available is False
        assert "ComfyUI" in statuses["comfyui"].detail

    def test_available_opendesign_still_not_wired(self) -> None:
        adapter = OpenDesignAdapter(probe=lambda: "/usr/local/bin/od")
        available, detail = adapter.availability()
        assert available is True
        assert "delegated to ls-od-*" in detail
        assert adapter.wired is False
        with pytest.raises(RuntimeError, match="not wired"):
            adapter.produce(make_brief(), Path("unused"))

    def test_broken_probe_is_recorded_not_fatal(self) -> None:
        class BrokenProbe:
            name = "broken"
            wired = False

            def supports(self, artifact: ArtifactType) -> bool:
                return True

            def availability(self) -> tuple[bool, str]:
                raise RuntimeError("probe blew up")

            def produce(self, brief: CreativeBrief, out_dir: Path) -> list[str]:
                raise AssertionError("never called")

        registry = AdapterRegistry([BrokenProbe()])
        statuses = registry.statuses()
        assert statuses[0].available is False
        assert "probe failed" in statuses[0].detail
        assert registry.select(ArtifactType.DECK) is None


# ---------------------------------------------------------------------------
# QA gate
# ---------------------------------------------------------------------------


class TestDefaultQa:
    def test_pass_for_brand_clean_outputs(self, tmp_path: Path) -> None:
        marp = tmp_path / "deck.md"
        marp.write_text("# Deck\n", encoding="utf-8")
        spec = tmp_path / "deck.json"
        spec.write_text('{"red": "#DC3641"}', encoding="utf-8")
        manifest = ExecutionManifest.new(make_brief())
        manifest.outputs = [str(marp), str(spec)]
        result = default_qa(manifest, tmp_path)
        assert result.verdict is QaVerdict.PASS
        assert result.checks["outputs_exist"] == "pass"
        assert result.checks["no_legacy_red"] == "pass"
        assert result.checks["brand_tokens"] == "pass"
        assert result.passed is True

    def test_fail_on_legacy_red(self, tmp_path: Path) -> None:
        legacy = tmp_path / "old.json"
        legacy.write_text('{"red": "#E63946"}', encoding="utf-8")
        manifest = ExecutionManifest.new(make_brief())
        manifest.outputs = [str(legacy)]
        result = default_qa(manifest, tmp_path)
        assert result.verdict is QaVerdict.FAIL
        assert result.checks["no_legacy_red"] == "fail"
        assert any("legacy red" in note for note in result.notes)

    def test_fail_on_missing_outputs(self, tmp_path: Path) -> None:
        manifest = ExecutionManifest.new(make_brief())
        manifest.outputs = [str(tmp_path / "gone.md")]
        result = default_qa(manifest, tmp_path)
        assert result.checks["outputs_exist"] == "fail"
        assert result.verdict is QaVerdict.FAIL

    def test_palette_free_artifact_skips_brand_check(self, tmp_path: Path) -> None:
        notes = tmp_path / "notes.md"
        notes.write_text("# Plain notes\n", encoding="utf-8")
        manifest = ExecutionManifest.new(make_brief())
        manifest.outputs = [str(notes)]
        result = default_qa(manifest, tmp_path)
        assert result.checks["brand_tokens"] == "skipped"
        assert result.verdict is QaVerdict.PASS


# ---------------------------------------------------------------------------
# Pipeline: success, approval, failure, rerun
# ---------------------------------------------------------------------------


class TestRunProduction:
    def test_success_flow_end_to_end(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        out = tmp_path / "out"

        manifest = run_production(
            make_brief(format_hint="board_meeting"),
            out_root=out,
            project_root=root,
            router=router,
            registry=offline_registry(),
            approver=lambda m: ApprovalDecision(approved=True, by="human_ceo", note="ship it"),
        )

        assert manifest.status is RunStatus.APPROVED
        assert manifest.approval.status is ApprovalStatus.APPROVED
        assert manifest.approval.approved_by == "human_ceo"
        assert manifest.approval.qa_passed is True
        assert manifest.qa.verdict is QaVerdict.PASS
        assert len(manifest.outputs) == 2
        for item in manifest.outputs:
            assert Path(item).exists()

        persisted = load_manifest(manifest.run_id, out)
        assert persisted.status is RunStatus.APPROVED
        assert persisted.run_id == manifest.run_id
        assert (out / manifest.run_id / "manifest.json").exists()
        assert list_runs(out) == [manifest.run_id]

    def test_no_adapter_fails_with_recorded_error(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        out = tmp_path / "out"
        registry = AdapterRegistry([PresentationAdapter()])

        manifest = run_production(
            make_brief(ArtifactType.WEBSITE),
            out_root=out,
            project_root=root,
            router=router,
            registry=registry,
            approver=lambda m: ApprovalDecision(approved=True),
        )

        assert manifest.status is RunStatus.FAILED
        assert manifest.errors
        assert "no available production adapter" in manifest.errors[0]
        assert load_manifest(manifest.run_id, out).status is RunStatus.FAILED

    def test_production_exception_marks_failed_then_rerun_succeeds(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        out = tmp_path / "out"

        failed = run_production(
            make_brief(),
            out_root=out,
            project_root=root,
            router=router,
            registry=AdapterRegistry([ExplodingAdapter()]),
        )
        assert failed.status is RunStatus.FAILED
        assert any("render backend exploded" in err for err in failed.errors)

        rerun = run_production(
            make_brief(),
            out_root=out,
            project_root=root,
            router=router,
            registry=offline_registry(),
            approver=lambda m: ApprovalDecision(approved=True),
            retry_of=failed.run_id,
        )
        assert rerun.status is RunStatus.APPROVED
        assert rerun.retry_of == failed.run_id
        assert rerun.run_id != failed.run_id
        assert sorted(list_runs(out)) == sorted([failed.run_id, rerun.run_id])

    def test_qa_failure_never_offers_approval(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        out = tmp_path / "out"
        approvals: list[str] = []

        def failing_qa(manifest: ExecutionManifest, run_dir: Path) -> QaResult:
            return QaResult(
                verdict=QaVerdict.FAIL, checks={"contrast": "fail"}, notes=["contrast too low"]
            )

        manifest = run_production(
            make_brief(),
            out_root=out,
            project_root=root,
            router=router,
            registry=offline_registry(),
            qa=failing_qa,
            approver=lambda m: approvals.append(m.run_id) or ApprovalDecision(approved=True),
        )

        assert manifest.status is RunStatus.QA
        assert manifest.qa.verdict is QaVerdict.FAIL
        assert manifest.approval.status is ApprovalStatus.PENDING
        assert approvals == []
        assert any("approval gate not offered" in w for w in manifest.warnings)

    def test_qa_pass_without_approver_parks_run(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        manifest = run_production(
            make_brief(),
            out_root=tmp_path / "out",
            project_root=root,
            router=router,
            registry=offline_registry(),
        )
        assert manifest.status is RunStatus.AWAITING_APPROVAL
        assert manifest.qa.verdict is QaVerdict.PASS
        assert any("parked awaiting CEO approval" in w for w in manifest.warnings)

    def test_rejection_is_recorded(self, tmp_path: Path) -> None:
        router = write_router_config(tmp_path / "router")
        root = write_project_root(tmp_path / "root")
        manifest = run_production(
            make_brief(),
            out_root=tmp_path / "out",
            project_root=root,
            router=router,
            registry=offline_registry(),
            approver=lambda m: ApprovalDecision(
                approved=False, by="human_ceo", note="wrong audience"
            ),
        )
        assert manifest.status is RunStatus.REJECTED
        assert manifest.approval.status is ApprovalStatus.REJECTED
        assert manifest.approval.note == "wrong audience"
        assert manifest.approval.qa_passed is True


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_manifest_roundtrip(self, tmp_path: Path) -> None:
        manifest = route_brief(
            make_brief(),
            router=write_router_config(tmp_path / "router"),
            project_root=write_project_root(tmp_path / "root"),
        )
        path = save_manifest(manifest, tmp_path / "runs")
        assert path.exists()
        loaded = load_manifest(manifest.run_id, tmp_path / "runs")
        assert loaded.model_dump_json() == manifest.model_dump_json()

    def test_list_runs_ignores_dirs_without_manifest(self, tmp_path: Path) -> None:
        (tmp_path / "not-a-run").mkdir()
        assert list_runs(tmp_path) == []
        (tmp_path / "empty").mkdir()
        (tmp_path / "empty" / "other.txt").write_text("x", encoding="utf-8")
        assert list_runs(tmp_path) == []
        assert list_runs(tmp_path / "missing") == []
