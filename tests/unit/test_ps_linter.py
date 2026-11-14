"""PowerShell anti-pattern pre-flight (P1-T3 / T-05)."""

from __future__ import annotations

from ai_company.executor.ps_linter import antipattern_ids, check_powershell_command


class TestPsLinter:
    def test_clean_command_passes(self) -> None:
        assert check_powershell_command("git status") == (True, "safe")

    def test_negative_first_rejected(self) -> None:
        ok, msg = check_powershell_command("Get-ChildItem | Select-Object -First -30")
        assert not ok
        assert "select_negative" in msg

    def test_negative_last_rejected(self) -> None:
        ok, _ = check_powershell_command("logs | Select-Object -Last -5")
        assert not ok

    def test_double_ampersand_rejected(self) -> None:
        ok, msg = check_powershell_command("cd foo && git status")
        assert not ok
        assert "double_ampersand" in msg

    def test_heredoc_rejected(self) -> None:
        ok, _ = check_powershell_command("python << 'PYEOF'")
        assert not ok

    def test_python3_rejected(self) -> None:
        ok, _ = check_powershell_command("python3 script.py")
        assert not ok

    def test_jq_subshell_rejected(self) -> None:
        ok, msg = check_powershell_command('gh pr view --jq "state=$(.state)"')
        assert not ok
        assert "jq_dollar_subshell" in msg

    def test_single_quoted_jq_passes(self) -> None:
        ok, _ = check_powershell_command("gh pr view --jq '.state'")
        assert ok

    def test_ids(self) -> None:
        ids = antipattern_ids("cd a && python3 x.py")
        assert "double_ampersand" in ids
        assert "python3_windows" in ids
