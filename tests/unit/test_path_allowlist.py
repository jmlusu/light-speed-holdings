"""Outside-workspace allowlist + attribution logging (GO-5)."""

from __future__ import annotations

from ai_company.security.path_allowlist import AllowlistConfig, PathAllowlist, load_allowlist_config


class TestAllowlist:
    def test_primary_workspace_allowed(self):
        v = PathAllowlist(session_id="ses_1")
        d = v.validate(r"C:\Users\jmlus\light-speed-holdings\AGENTS.md", tool="read")
        assert d.allowed is True and d.category == "primary"

    def test_athena_sibling_per_session(self):
        v = PathAllowlist(session_id="ses_1")
        d = v.validate(r"C:\Users\jmlus\athena\app.py", tool="edit")
        assert d.allowed is True and d.category == "sibling"

    def test_social_media_sibling_per_session(self):
        v = PathAllowlist(session_id="ses_1")
        d = v.validate(r"C:\Users\jmlus\social-media-automation-os\Dockerfile", tool="read")
        assert d.allowed is True

    def test_temp_opencode_sandbox_write(self):
        v = PathAllowlist(session_id="ses_1")
        d = v.validate(
            r"C:\Users\jmlus\AppData\Local\Temp\opencode\ses_1\scratch.txt", tool="write"
        )
        assert d.allowed is True and d.category == "sandbox"

    def test_temp_opencode_read_requires_session_prefix(self):
        v = PathAllowlist(session_id="ses_1")
        d = v.validate(r"C:\Users\jmlus\AppData\Local\Temp\opencode\root.txt", tool="read")
        assert d.allowed is False

    def test_openmausbot_denied(self):
        v = PathAllowlist(session_id="ses_1")
        d = v.validate(r"C:\Users\jmlus\.openmausbot\workspace\file.txt", tool="read")
        assert d.allowed is False and "openmausbot" in d.reason

    def test_drive_root_denied(self):
        v = PathAllowlist(session_id="ses_1")
        assert v.validate("C:/", tool="bash").allowed is False

    def test_db_and_auth_paths_denied(self):
        v = PathAllowlist(session_id="ses_1")
        for p in (
            r"C:\Users\jmlus\.local\share\opencode\opencode.db",
            r"C:\Users\jmlus\.local\share\opencode\opencode.db-wal",
            r"C:\Users\jmlus\.local\share\opencode\tool-output\x.txt",
            r"C:\Users\jmlus\light-speed-holdings\auth.json",
            r"C:\Users\jmlus\light-speed-holdings\.env",
        ):
            assert v.validate(p, tool="read").allowed is False, p

    def test_unknown_outside_default_deny(self):
        v = PathAllowlist(session_id="ses_1")
        d = v.validate(r"C:\Users\jmlus\some-random-repo\file.txt", tool="read")
        assert d.allowed is False and d.category == "outside"

    def test_attribution_log_records_path_tool_session_never_content(self):
        v = PathAllowlist(
            session_id="ses_9", project_id="proj_1", directory=r"C:\Users\jmlus\athena"
        )
        v.validate(r"C:\Users\jmlus\athena\app.py", tool="edit")
        (rec,) = v.attribution_log
        assert rec["session_id"] == "ses_9"
        assert rec["project_id"] == "proj_1"
        assert rec["tool"] == "edit"
        assert rec["allowed"] is True
        assert "content" not in rec

    def test_config_from_dict_and_yaml(self, tmp_path):
        cfg = AllowlistConfig.from_dict({"allow": {"primary_repo": "light-speed-holdings"}})
        assert cfg.primary_repo == "light-speed-holdings"
        # Missing file -> defaults, never crash.
        assert (
            load_allowlist_config(tmp_path / "missing.yaml").primary_repo == "light-speed-holdings"
        )
