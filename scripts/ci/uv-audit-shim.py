"""CI wrapper for uv-audit that works around a package-schemes name-matching bug.

package-schemes Pyproject.get_package_meta() matches dependency strings with a raw
``dep.startswith(name)`` prefix test, so a transitive query for ``httpx`` resolves to
the direct dependency string ``httpx2>=2.12`` (parsed name ``httpx2``). The lock side
matches exactly (name ``httpx``), and PackageMeta.merge() then asserts
``pyproject name == lock name`` ("httpx2" == "httpx") and crashes with AssertionError.

This repository depends on httpx2 directly (issue #156) while httpx remains a
transitive dependency (huggingface-hub, safety), which triggers the bug. All
package-schemes releases 0.1.0-0.1.2 contain identical matching code and uv-audit
requires >=0.1.2, so no version pin avoids it.

Shim: when the two metas disagree on the name, trust the lock metadata (exact match
on the queried name; the pyproject side is the fuzzy one), equivalent to what
merge(None, lock) already returns. Vulnerability scanning and exit-code semantics
are unchanged.

Revert this wrapper once package-schemes compares parsed package names instead of
raw string prefixes (upstream: package-schemes Pyproject.get_package_meta).
"""

from package_schemes.interfaces.packages import PackageMeta

_orig_merge = PackageMeta.merge.__func__


def _merge(cls, meta_1, meta_2):
    if meta_1 is not None and meta_2 is not None and meta_1.name != meta_2.name:
        return _orig_merge(cls, None, meta_2)
    return _orig_merge(cls, meta_1, meta_2)


PackageMeta.merge = classmethod(_merge)

from uv_audit.cli import cli  # noqa: E402

if __name__ == "__main__":
    cli()
