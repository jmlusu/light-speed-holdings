# Accessibility Testing Checklist (Phase 14 — Section 45)

## Keyboard Navigation
- [ ] All interactive elements reachable via Tab key
- [ ] Tab order is logical and follows visual flow
- [ ] Shift+Tab navigates backwards
- [ ] Skip links available to jump to main content
- [ ] Focus visible indicator on all focusable elements
- [ ] Escape key closes modals, dialogs, and overlays
- [ ] Arrow keys navigate within interactive groups (sliders, carousels)
- [ ] Spacebar activates buttons, checkboxes, radio buttons
- [ ] Enter key activates buttons and submit forms
- [ ] 3D interaction degrades gracefully without keyboard support

## Screen Reader Behavior (a11y)
- [ ] Semantic HTML structure (header, nav, main, section, article, footer)
- [ ] All form fields have associated labels (<label> for attribute binding)
- [ ] Landmarks identified correctly by screen readers
- [ ] 3D canvas has appropriate aria-label or role="region"
- [ ] Dynamic content announcements (polite/interruptive politeness)
- [ ] No auto-playing content without user control
- [ ] Reading order makes sense when linearized (no DOM-order surprises)

## Contrast
- [ ] Normal text: contrast ratio ≥ 4.5:1 against background
- [ ] Large text (≥ 18pt or ≥ 14pt bold): contrast ratio ≥ 3:1 against background
- [ ] UI components and graphical elements: contrast ratio ≥ 3:1
- [ ] Incidental text (logo, decorative) exempt but reviewed
- [ ] 3D overlay text has sufficient contrast
- [ ] Focus ring contrast meets 3:1 minimum

## Focus Management
- [ ] Focus is not trapped unexpectedly
- [ ] Focus returns to opening element after modal/dialog close
- [ ] Focus order matches visual order
- [ ] Page title is meaningful and descriptive
- [ ] Live region announcements for dynamic content
- [ ] Skip-to-content link at top of page

## Reduced Motion
- [ ] Media query `@media (prefers-reduced-motion: reduce)` implemented
- [ ] Non-essential animation disabled or significantly reduced
- [ ] Core functionality works without any animation
- [ ] 3D transitions respect reduced-motion preference
- [ ] Hover effects have reduced-motion fallback

## Form Accessibility
- [ ] All form fields have proper labels (not placeholder-only)
- [ ] Error identification and announcement
- [ ] Error suggestions or instructions for correction
- [ ] Fieldset/legend groups related controls
- [ ] Checkboxes and radio buttons are keyboard-focusable
- [ ] Form submission provides success confirmation
- [ ] Clear error messages with specific guidance

## Heading Hierarchy
- [ ] Page has exactly one h1 element
- [ ] Heading hierarchy is sequential (h1 → h2 → h3, no skipping)
- [ ] Heading levels describe content structure, not just styling
- [ ] 3D section headings follow same hierarchy rules
- [ ] Skip navigation links if complex navigation present

## 3D-Specific Accessibility
- [ ] Users can understand the story when 3D is disabled
- [ ] Alternative text descriptions for key 3D concepts
- [ ] Core message communicated without WebGL dependency
- [ ] Reduced-motion support for 3D animations/transitions
- [ ] Color is not the only means of conveying information in 3D
- [ ] Keyboard-accessible controls for 3D interaction (if any)
- [ ] Screen reader friendly labels for 3D controls

## Testing Methods
- [ ] Manual keyboard-only navigation test
- [ ] NVDA + Firefox screen reader testing
- [ ] VoiceOver + Safari screen reader testing
- [ ] Chrome DevTools Accessibility pane inspection
- [ ] axe-playwright or axe-core automated tests
- [ ] WAVE evaluation tool
- [ ] Focus visibility visualization in DevTools
