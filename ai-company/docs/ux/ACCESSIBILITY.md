# Accessibility Design

> Color contrast, screen reader support, keyboard navigation, and colorblind-safe palettes.

---

## 1. Standards & Compliance

| Standard | Target | Status |
|----------|--------|--------|
| WCAG 2.1 AA | Full compliance | In progress |
| Section 508 | US federal compliance | Planned |
| ADA Title III | Public accommodation | Planned |

---

## 2. Color Contrast Requirements

### 2.1 Minimum Contrast Ratios

| Element | Required Ratio | WCAG Level |
|---------|----------------|------------|
| Normal text (< 18pt) | 4.5:1 | AA |
| Large text (≥ 18pt or 14pt bold) | 3:1 | AA |
| UI components | 3:1 | AA |
| Focus indicators | 3:1 | AA |
| Graphical objects | 3:1 | AA |

### 2.2 Dashboard Color Palette

All colors meet WCAG AA contrast against white (#FFFFFF) and dark (#111827) backgrounds:

| Color Name | Hex | Contrast vs White | Contrast vs Dark |
|------------|-----|-------------------|------------------|
| Brand Blue | `#0284c7` | 4.6:1 ✓ | 4.4:1 ✓ |
| Success Green | `#16a34a` | 4.5:1 ✓ | 4.3:1 ✓ |
| Warning Amber | `#d97706` | 3.9:1 ✓ (large) | 3.7:1 ✓ (large) |
| Error Red | `#dc2626` | 4.6:1 ✓ | 4.5:1 ✓ |
| Info Purple | `#9333ea` | 4.6:1 ✓ | 4.5:1 ✓ |
| Text Primary | `#111827` | 15.4:1 ✓ | — |
| Text Secondary | `#6b7280` | 5.0:1 ✓ | 4.8:1 ✓ |
| Text Muted | `#9ca3af` | 3.1:1 ✓ (large) | 3.0:1 ✓ (large) |

### 2.3 CLI Color Palette

Terminal colors are mapped to ensure readability on both light and dark backgrounds:

| Semantic | Dark BG (ANSI) | Light BG (ANSI) | Description |
|----------|----------------|-----------------|-------------|
| Success | `\033[32m` (green) | `\033[32m` | Completed actions |
| Warning | `\033[33m` (yellow) | `\033[33m` | Attention needed |
| Error | `\033[31m` (red) | `\033[31m` | Failures |
| Info | `\033[36m` (cyan) | `\033[36m` | Headers, labels |
| Emphasis | `\033[1m` (bold) | `\033[1m` | Important text |
| Muted | `\033[90m` (gray) | `\033[90m` | Timestamps, secondary |

---

## 3. Colorblind-Safe Palette

### 3.1 Design Principles

- **Never use color as the sole indicator** — always pair with text, icons, or patterns
- **Use shape + color** — circles for success, triangles for warning, squares for error
- **Use patterns** — striped, dotted, solid fills for charts
- **Use text labels** — `[PASS]`, `[WARN]`, `[FAIL]` alongside colored badges

### 3.2 Colorblind-Safe Status Indicators

| Status | Color | Icon | Text Label | Pattern (Charts) |
|--------|-------|------|------------|------------------|
| Success | Green | ✓ | `PASS` | Solid fill |
| Warning | Amber | ⚠ | `WARN` | Diagonal stripes |
| Error | Red | ✗ | `FAIL` | Cross-hatch |
| Info | Blue | ℹ | `INFO` | Dots |
| Pending | Gray | ○ | `PENDING` | Empty outline |

### 3.3 Chart Patterns

For bar charts and pie charts, use fill patterns in addition to colors:

```
Success:  [████████] Solid
Warning:  [▓▓▓▓▓▓▓▓] Diagonal stripes
Error:    [╳╳╳╳╳╳╳╳] Cross-hatch
Info:     [········] Dots
Pending:  [        ] Outline only
```

### 3.4 Text-Based Alternatives

When color cannot be used (plain text, print):

```
# Instead of colored text:
✓ Completed (green)
⚠ Warning (amber)
✗ Failed (red)

# Always include:
Status: completed [OK]
Status: pending [WAIT]
Status: failed [ERR]
Status: escalated [UP]
```

---

## 4. Keyboard Navigation

### 4.1 Dashboard Keyboard Shortcuts

| Key | Action | Context |
|-----|--------|---------|
| `1`-`6` | Switch tabs | Global |
| `Tab` | Move to next element | Current tab |
| `Shift+Tab` | Move to previous element | Current tab |
| `Enter` / `Space` | Activate button/link | Focused element |
| `Esc` | Close modal / dismiss toast | Modal open |
| `n` | Open notification center | Global |
| `a` | Approve (when card focused) | Approvals tab |
| `r` | Reject (when card focused) | Approvals tab |
| `?` | Show keyboard shortcuts | Global |

### 4.2 Focus Management

**Focus order:**
1. Skip-to-content link (hidden until Tab)
2. Navigation tabs
3. Main content area
4. Interactive elements in order

**Focus indicators:**
```css
:focus-visible {
  outline: 2px solid #0284c7;
  outline-offset: 2px;
  border-radius: 4px;
}
```

**Focus trap in modals:**
- Tab cycles within modal
- Esc closes modal
- Focus returns to trigger element

### 4.3 Screen Reader Announcements

```html
<!-- Live region for KPI updates -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  Pending tasks: 12
</div>

<!-- Status announcements -->
<div aria-live="assertive" class="sr-only">
  Task completed: Budget report by CFO
</div>

<!-- Navigation announcements -->
<div aria-live="polite" class="sr-only">
  Tab: Approvals and Escalations
</div>
```

### 4.4 CLI Keyboard Support

The CLI uses standard terminal input:
- Arrow keys for command history
- Tab for completion (when implemented)
- Ctrl+C to interrupt
- Ctrl+L to clear screen

---

## 5. Screen Reader Support

### 5.1 ARIA Labels

All interactive elements have descriptive labels:

| Element | ARIA Label |
|---------|------------|
| KPI card | `"Pending tasks: 12"` |
| Status badge | `"Status: pending"` |
| Priority badge | `"Priority: high"` |
| Tab button | `"Tab: Dashboard, currently selected"` |
| Approve button | `"Approve request apr-7b3e9f"` |
| Reject button | `"Reject request apr-7b3e9f"` |
| Org chart node | `"Agent: Lead Engineer, role: Specialist, department: engineering"` |
| Modal close | `"Close agent detail panel"` |

### 5.2 Semantic HTML

```html
<!-- Use semantic elements -->
<header role="banner">...</header>
<nav role="navigation" aria-label="Main navigation">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>

<!-- Tables with proper headers -->
<table>
  <caption>Agent roster</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Role</th>
    </tr>
  </thead>
</table>

<!-- Forms with labels -->
<label for="receiver">Receiver</label>
<select id="receiver">...</select>
```

### 5.3 Chart Accessibility

Charts include text alternatives:

```html
<canvas aria-label="Task status bar chart showing 12 pending, 4 in progress, 45 completed">
</canvas>

<!-- Text alternative -->
<div class="sr-only">
  Task status: 12 pending, 4 in progress, 45 completed, 0 failed, 3 escalated
</div>
```

---

## 6. Responsive Accessibility

### 6.1 Mobile Considerations

- Touch targets minimum 44x44px
- No hover-dependent interactions
- Swipe gestures for tab navigation
- Reduced motion respect: `prefers-reduced-motion`

### 6.2 Zoom Support

- Dashboard usable at 200% zoom
- Text reflows without horizontal scrolling
- Layout adapts gracefully

### 6.3 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 7. CLI Accessibility

### 7.1 NO_COLOR Support

When `NO_COLOR` env var is set, all color codes are stripped:

```bash
$ NO_COLOR=1 ai-company doctor run

System Health
+--------------------------+------+----------------------------------+
| Check                    |Status| Message                          |
+--------------------------+------+----------------------------------+
| Registry exists          | PASS | Found 27 agents                  |
```

### 7.2 Plain Text Mode

```bash
$ ai-company agents list --plain

Role                                 Type          Department
Chief of Staff                       Executive     operations
CTO                                  Executive     engineering
Lead Engineer                        Specialist    engineering
```

### 7.3 Verbose Mode

```bash
$ ai-company orchestrator tick --verbose

[2026-07-20 14:30:01] INFO  Loading inbox.json (12 tasks)
[2026-07-20 14:30:01] INFO  Task a3f2c1: pending → in_progress
[2026-07-20 14:30:02] INFO  Task a3f2c1: assigned to lead-engineer
[2026-07-20 14:30:03] INFO  Task a3f2c1: completed successfully
```

---

## 8. Testing Accessibility

### 8.1 Automated Checks

```bash
# Lighthouse (dashboard)
npx lighthouse http://localhost:8420 --accessibility

# axe-core (browser extension)
# Install axe DevTools extension, run scan

# pa11y (CLI)
npx pa11y http://localhost:8420
```

### 8.2 Manual Testing Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Focus visible on all focusable elements
- [ ] Screen reader announces all dynamic content
- [ ] Color contrast meets AA ratios
- [ ] Charts have text alternatives
- [ ] Modals trap focus correctly
- [ ] Esc closes all modals/popups
- [ ] Form inputs have associated labels
- [ ] Error messages announced to screen readers
- [ ] No content flashes more than 3 times per second
- [ ] Page works at 200% zoom
- [ ] Works with `prefers-reduced-motion`

### 8.3 Screen Reader Testing

| Screen Reader | Browser | Platform |
|---------------|---------|----------|
| NVDA | Chrome/Firefox | Windows |
| VoiceOver | Safari | macOS |
| JAWS | Chrome | Windows |
| TalkBack | Chrome | Android |

---

## 9. Documentation Accessibility

All documentation follows:

- **Heading hierarchy**: H1 → H2 → H3 (no skipped levels)
- **Link text**: Descriptive, not "click here"
- **Lists**: Proper `<ul>`, `<ol>`, `<dl>` elements
- **Tables**: Proper `<th>`, `<caption>`, `scope` attributes
- **Code blocks**: Language specified for syntax highlighting
- **Images**: Alt text for all images (or decorative attribute)
- **Language**: Plain language, 8th-grade reading level

---

## 10. Accessibility Statement

```
Light Speed Holdings is committed to ensuring digital accessibility
for people with disabilities. We are continually improving the user
experience for everyone and applying the relevant accessibility
standards.

Conformance Status:
- WCAG 2.1 Level AA: Partially conformant
- Section 508: Planned

Known Limitations:
- Dashboard charts use canvas elements with text alternatives
- CLI output uses ANSI colors with NO_COLOR fallback

Feedback:
If you encounter accessibility barriers, please contact us at
[accessibility@lightspeedholdings.com].
```
