"""Tests for the shared LLM JSON parsing utilities.

Covers trailing-comma repair (``_strip_trailing_commas``), invalid-escape
repair (``_fix_invalid_escapes``), and the transactional parse entry point
(``parse_llm_json``), including regression tests for the Pharos scan loop
failures where a trailing comma or a raw ``\\d`` regex escape made a
planning-only response parse as ``None`` and silently end the agent loop
after one iteration.
"""

from ai_company.llm.json_parser import (
    _fix_invalid_escapes,
    _strip_trailing_commas,
    parse_llm_json,
)

# The exact failing response from
# results/routine-pharos_sadc_research_scan-2026-09-17/loop_result.json:
# a trailing comma after the last plan item made every strict parse
# strategy fail, so the agent loop treated the planning text as a final
# answer and ran zero tools.
PHAROS_TRAILING_COMMA_RESPONSE = """To perform the SADC Research Scan, I'll start by accessing the stakeholder map to identify relevant sources. Then, I'll use webfetch to retrieve the latest developments from each stakeholder and verify their sources.

```json
{
  "thought": "First, I'll read the stakeholder map to identify relevant sources for the SADC Research Scan.",
  "plan": [
    {"tool": "read", "args": {"args": ["stakeholder-map.md"]}},
    {"tool": "webfetch", "args": {"url": "https://example.com/stakeholder-URL"}},
    {"tool": "read", "args": {"args": ["result-of-webfetch"]}},
    {"tool": "edit", "args": {"file": "docs/Pharos/sadc-research-scan.md", "content": "Initial scan content"}},
    {"tool": "task", "args": {"receiver": "content_writer", "instruction": "Compile scan note with markdown format"}},
  ],
  "result": "Stakeholder map read completed. Next, initiating webfetch for the first URL.",
  "done": false
}
```"""


class TestStripTrailingCommas:
    def test_single_object_trailing_comma(self):
        assert _strip_trailing_commas('{"a": 1,}') == '{"a": 1}'

    def test_array_trailing_comma(self):
        assert _strip_trailing_commas("[1, 2,]") == "[1, 2]"

    def test_commas_inside_strings_are_preserved(self):
        assert (
            _strip_trailing_commas('{"msg": "hi, there,", "n": 2,}')
            == '{"msg": "hi, there,", "n": 2}'
        )

    def test_escaped_quotes_inside_strings(self):
        assert _strip_trailing_commas('{"msg": "say \\"hi,\\"",}') == '{"msg": "say \\"hi,\\""}'

    def test_nested_trailing_commas(self):
        assert (
            _strip_trailing_commas('{"a": [1, 2,], "b": {"c": 3,},}')
            == '{"a": [1, 2], "b": {"c": 3}}'
        )

    def test_non_trailing_commas_untouched(self):
        assert _strip_trailing_commas('{"a": 1, "b": 2}') == '{"a": 1, "b": 2}'


class TestFixInvalidEscapes:
    def test_raw_regex_backslash_doubled(self):
        # "^\d+.*" -> "\\d" must become a valid escape "\\d" (regex preserved)
        assert _fix_invalid_escapes(r'{"p": "^\d+.*"}') == r'{"p": "^\\d+.*"}'

    def test_valid_escapes_untouched(self):
        assert _fix_invalid_escapes(r'{"p": "line\nbreak \"q\""}') == r'{"p": "line\nbreak \"q\""}'

    def test_escaped_backslash_untouched(self):
        # "\\" is a valid escape (literal backslash); must not be doubled
        assert _fix_invalid_escapes(r'{"p": "a\\b"}') == r'{"p": "a\\b"}'

    def test_unicode_escape_untouched(self):
        assert _fix_invalid_escapes(r'{"p": "\u00e9"}') == r'{"p": "\u00e9"}'

    def test_backslash_outside_string_untouched(self):
        assert _fix_invalid_escapes(r'{"a": 1} \d') == r'{"a": 1} \d'


class TestParseTrailingCommaTolerance:
    def test_parse_valid_json_still_works(self):
        assert parse_llm_json('{"plan": [], "result": "ok"}') == {
            "plan": [],
            "result": "ok",
        }

    def test_parse_direct_trailing_comma(self):
        result = parse_llm_json('{"plan": [{"tool": "read"}], "done": false,}')
        assert result is not None
        assert result["done"] is False
        assert result["plan"][0]["tool"] == "read"

    def test_parse_in_code_block_with_trailing_comma(self):
        raw = 'Here is the plan:\n```json\n{"plan": [{"tool": "read", "args": {"path": "x.py"}},], "done": false}\n```'
        result = parse_llm_json(raw)
        assert result is not None
        assert result["done"] is False
        assert len(result["plan"]) == 1

    def test_parse_invalid_returns_none(self):
        assert parse_llm_json("I'm not sure what to do here.") is None
        assert parse_llm_json("```some code```") is None

    def test_pharos_scan_regression(self):
        """The planning response that silently ended the loop must now parse.

        Assertions mirror what the agent loop needs to proceed: a non-null
        dict, ``done`` false, a five-item plan, and the intended first tool.
        """
        result = parse_llm_json(PHAROS_TRAILING_COMMA_RESPONSE)
        assert result is not None
        assert result["done"] is False
        assert len(result["plan"]) == 5
        assert result["plan"][0]["tool"] == "read"
        assert result["result"].startswith("Stakeholder map read completed.")

    def test_pharos_scan_invalid_escape_regression(self):
        """Raw regex escapes (``\\d``) must no longer fail the whole parse.

        The Pharos scan loop emitted ``"pattern": "^\\d+.*"`` — a backslash
        followed by ``d`` is an invalid JSON escape, so strict parsing
        returned ``None`` and the loop silently ended after one iteration.
        """
        raw = (
            "Before starting, I'll review the scan history.\n"
            "```json\n{\n"
            '  "plan": [\n'
            '    {"tool": "webfetch", "args": {"url": "https://example.com"}},\n'
            '    {"tool": "grep", "args": {"pattern": "^\\\\d+.*", "path": "stakeholder-map.md"}}\n'
            "  ],\n"
            '  "result": "Starting scan.",\n'
            '  "done": false\n'
            "}\n```"
        )
        result = parse_llm_json(raw)
        assert result is not None
        assert result["done"] is False
        assert len(result["plan"]) == 2
        assert result["plan"][1]["args"]["pattern"] == r"^\d+.*"
