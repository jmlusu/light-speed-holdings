# 3D Iconography Design System Standard

**Document Version:** 1.1.0
**Specification:** Transparent Blue Glass & Polished Metallic Gold 3D Visual Language
**Scope:** Regipedia & LightSpeed Web Applications

---

## 1. Design Direction & Material Specifications

The 3D Iconography System establishes a cohesive visual standard combining **Transparent Blue Glass**, **Polished Metallic Gold**, and **Cyan/Deep Navy Refraction Accents**.

### Core Material Palette

| Attribute | Specification | Color Tokens / Stops | Visual Effect |
|---|---|---|---|
| **Primary Material** | Transparent Blue Glass | `#070A40`, `#0A1960`, `#1E3A8A` (Opacity: 0.75 - 0.88) | Refractive, glassmorphic depth with subtle inner shadows |
| **Secondary Material** | Polished Metallic Gold | `#FFD700`, `#F59E0B`, `#B45309`, `#FEF08A` | Specular highlights, polished metallic beveled borders & accents |
| **Accent Material** | Cyan Glass Edge & Glow | `#00BFFF`, `#38BDF8`, `#00E5FF` | Rim highlights, neon edge refractions, and active status halos |
| **Surface Finish** | High-Gloss Reflective | Specular lighting filters & multi-stop linear/radial gradients | Polished studio finish with multi-angle specular highlights |
| **Shadows** | Soft Radial Drop Shadow | `rgba(7, 10, 64, 0.35)` with `blur: 12px` | Realistic 3D elevation and soft ground plane anchoring |
| **Perspective** | Three-Quarter Orthographic | 15° to 25° isometric/three-quarter tilt | Consistent spatial orientation across all icon categories |

---

## 2. Size & Responsive Scale Hierarchy

The `<Icon3D />` component supports four standardized size tokens to maintain information density across viewports:

| Size Token | Dimensions (px) | Grid Container | Use Context |
|---|---|---|---|
| `sm` | 24 × 24 px | 32 × 32 px | Inline table rows, navigation items, compact badge chips |
| `md` | 48 × 48 px | 60 × 60 px | Standard feature cards, service category blocks, form headers |
| `lg` | 64 × 64 px | 80 × 80 px | Primary section headings, prominent dashboard KPIs, modal headers |
| `hero` | 96 × 96 px | 120 × 120 px | Hero section focal points, onboarding empty states, whitepaper covers |

---

## 3. Semantic Taxonomy & Registry Mapping

The system relies on a semantic identifier mapping so components reference icons by concept rather than file paths:

- `dashboard` / `analytics`: 3D Glass Bar Chart with Gold Trend Arrow
- `finance` / `revenue`: 3D Transparent Blue Glass Vault & Gold Coin Stack
- `security` / `compliance`: 3D Blue Glass Shield with Gold Crest & Cyan Keyhole
- `documents` / `reports`: 3D Stacked Glass Pages with Gold Bookmark & Cyan Stamp
- `users` / `organizations`: 3D Glass Avatar Sphere with Gold Crown Rim
- `registration` / `verification`: 3D Blue Glass ID Badge with Gold Lock Ring
- `settings` / `administration`: 3D Glass Gear Engine with Gold Metallic Core
- `notifications` / `activity`: 3D Glass Bell with Gold Clapper & Cyan Signal Halo
- `search` / `filtering`: 3D Glass Lens with Gold Metallic Handle
- `support` / `help`: 3D Glass Lifebuoy with Gold Metallic Accents
- `approvals` / `workflow`: 3D Bounded Glass Gate with Gold Seal
- `categories` / `sectors`: 3D Glass Structural Cube with Gold Face
- `location` / `geography`: 3D Glass Pin / Globe with Gold Continent Lines
- `calendar` / `history`: 3D Glass Calendar Block with Gold Ring Binders
- `intelligence`: 3D Glass Brain with Gold Neural Core
- `orchestration`: 3D Glass Routing Lattice with Gold Node Rays
- `governance`: 3D Glass Sovereign Shield with Gold Crown Gate

---

## 4. Accessibility & Performance Guidelines

1. **Accessibility (`aria-hidden` vs `aria-label`)**:
   - Decorative icons in cards automatically set `aria-hidden="true"`.
   - Standalone icons set explicit `aria-label` accessibility text.
2. **Layout Stability**:
   - Explicit width and height attributes prevent layout shift during page hydration.
3. **Vector Rendering Performance**:
   - Icons are rendered as lightweight, pure SVG 3D vector paths with hardware-accelerated CSS filters, avoiding heavy WebGL dependencies or large image downloads.
