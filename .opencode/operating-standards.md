# Operating Standards

These standards apply to every agent in the organization. Agent cards reference
this document instead of duplicating the content inline.

## Operating Principles

- Evidence over opinion
- Customer first
- Security by design
- Automate repetitive work
- Escalate uncertainty

## Luxury Documentation Formatting Principles (inherited from LUXURY-EDITORIAL-STANDARD.md)

- **Token compliance:** All documentation must use only canonical brand tokens
  (`--ls-red: #DC3641`, `grey-light: #F2F2F2`, and the 7 other approved values).
  No inline hex colours, fonts, or spacing tokens outside the allowlisted palette.
- **Accent restraint:** The primary accent (`--ls-red`) must appear in no more than
  3 places per document page. This is enforced by the compliance linter.
- **Line-length constraint:** Prose lines must not exceed 75 characters. Body text
  should be constrained to 65ch max via the theme-layer `max-width` setting.
- **Spatial rhythm:** Documents should respect macro whitespace (64px–96px between
  sections, via `var(--ls-space-8/9)`) and micro line-height 1.65 set on the `html`
  element.
- **Callout format:** Any callout element must use a 2px left border in
  `--ls-red`, indented padding, muted text (`var(--ls-grey-dark)`), no icons,
  and no coloured background fill.
- **No decorative chrome:** Heavy box-shadow, thick borders ( >1px), saturated
  background fills, and multicolored badges are prohibited.
- **Code block format:** Code blocks must use `var(--ls-bg-dark)` background,
  `var(--ls-white)` text, 24px minimum padding, and zero decorative chrome.

*For full details, see `docs/standards/LUXURY-EDITORIAL-STANDARD.md`.*
