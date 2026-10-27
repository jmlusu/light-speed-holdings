"""Layout probe for the executive briefing HTML.

Prints, per A4 page, the natural content height against the 1123px A4 box so
overflow is measured rather than eyeballed.

Usage:
    python artifacts/campaigns/2026-10-26-pipeline-test/open-design/probe_layout.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
HTML = HERE / "executive-briefing.html"

JS = """
() => {
  const out = [];
  document.querySelectorAll('.page').forEach((page, i) => {
    const box = page.getBoundingClientRect();
    let content = 0;
    for (const child of page.children) {
      content += child.getBoundingClientRect().height;
    }
    const rows = [];
    const push = (sel) => {
      page.querySelectorAll(sel).forEach((el) => {
        const r = el.getBoundingClientRect();
        rows.push({
          sel,
          text: (el.textContent || '').trim().slice(0, 46),
          top: +(r.top - box.top).toFixed(1),
          h: +r.height.toFixed(1),
          bottom: +(r.bottom - box.top).toFixed(1),
        });
      });
    };
    ['header', '.section-head', 'p', '.pillars', '.evidence', '.callout-navy',
     '.reg-columns', '.steps', '.callout-red', 'footer'].forEach(push);
    const body = document.body.getBoundingClientRect();
    out.push({
      page: i + 1,
      boxW: +box.width.toFixed(1),
      boxH: +box.height.toFixed(1),
      scrollH: page.scrollHeight,
      contentSum: +content.toFixed(1),
      bodyScrollH: body.height,
      rows,
    });
  });
  return out;
}
"""


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(HTML.as_uri(), wait_until="load")
        page.wait_for_function("document.fonts.status === 'loaded'")
        data = page.evaluate(JS)
        npm = page.evaluate("() => document.body.scrollHeight")
        browser.close()

    print(f"body natural height: {npm}px  (A4 box = 1123px)")
    for d in data:
        overflow = d["scrollH"] - d["boxH"]
        flag = "OVERFLOW" if d["contentSum"] > d["boxH"] else "ok"
        print(
            f"\nPAGE {d['page']}  box {d['boxW']}x{d['boxH']}  "
            f"content {d['contentSum']}  scroll {d['scrollH']}  -> {flag} ({overflow:+.0f}px)"
        )
        for r in d["rows"]:
            print(
                f"   {r['sel']:16s} top={r['top']:7.1f} h={r['h']:7.1f} "
                f"bottom={r['bottom']:7.1f}  {r['text']}"
            )


if __name__ == "__main__":
    main()
