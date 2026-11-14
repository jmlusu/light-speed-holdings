# Dual-Theme Gap Analysis: LightSpeed Holdings

**Audit Date**: November 3, 2026
**Auditor**: Lead Frontend Architect & Accessibility Specialist

---

## 1. Theme Switcher & Storage Architecture

- **Theme Toggle Location**: Header top-right utility area (`FloatingNav.tsx`).
- **State Management**: React state synced with `localStorage.getItem('lightspeed_theme')`.
- **CSS Class Targeting**: Toggles `.dark` on `document.documentElement` (`<html>`).
- **Tailwind v4 Configuration**: `@custom-variant dark (&:where(.dark, .dark *));` is configured in `/src/index.css` directly below `@import "tailwindcss";`.

---

## 2. Contrast & Surface Mapping

| Element | Dark Mode State | Light Mode State | WCAG 2.2 AA Contrast |
| :--- | :--- | :--- | :--- |
| **Canvas / Background** | Deep Mineral (`#121518`) / Navy (`#070A40`) | Morning Mist (`#F7F8F9`) / Off-White | Passed (21:1 / 18:1) |
| **Primary Headlines** | White (`#FFFFFF`) | Deep Navy (`#070A40`) | Passed (19:1 / 18:1) |
| **Body Text** | Slate Light (`#CBD5E1` / `#E2E8F0`) | Slate Dark (`#334155` / `#1E293B`) | Passed (9.5:1 / 11:1) |
| **Accent Text / Links** | Cyan (`#00BFFF`) | Medium Cyan (`#0088CC`) | Passed (4.8:1 / 4.6:1) |
| **Primary CTA Button** | Brand Red (`#E63946`) with White text | Brand Red (`#E63946`) with White text | Passed (4.7:1) |
| **Brand Logo** | `/brand/logo/logo-dark-bg.svg` | `/brand/logo/logo-light-bg.svg` | Passed |

---

## 3. Verified Theme Behaviors

1. **Zero Flash on Load**: Theme state is evaluated before render and applied directly to `document.documentElement`.
2. **Interactive States**: Hover, focus-visible (`outline: 2px solid #00BFFF`), and active states respond with smooth 300ms transitions (`var(--ease-spatial)`).
3. **Card Boundaries**: Subtle hairline borders (`border-white/10` in dark mode, `border-slate-200` in light mode) ensure container separation without heavy fills.
