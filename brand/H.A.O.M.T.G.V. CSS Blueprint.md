# H.A.O.M.T.G.V. CSS Blueprint

Technical blueprint for building the Lightspeed Holdings H.A.O.M.T.G.V. operating-philosophy hero in React and Tailwind CSS. Blueprint only; no component code until approved.

**Canvas:** 16:9 (about 1672×941), designed at 1440px and up. Stacks on mobile (see section 5).

## 1. Z-Index & Layering

| z | Layer | Spec |
| --- | --- | --- |
| `z-0` | Base | Solid `#050B1A` (deep navy). Fallback while the photo loads. |
| `z-0` | Photo | Dusk terrace/lake/mountains, `object-cover`, full opacity. Sunset glow is baked in at lower-left. **Needs an exported raster asset; CSS can't recreate it.** |
| `z-10` | Scrims | (a) Right-to-left darkening: `linear-gradient(to left, rgba(5,11,26,.88) 0%, rgba(5,11,26,.55) 45%, transparent 75%)`. (b) Top fade for the header: `linear-gradient(to bottom, rgba(5,11,26,.7), transparent 25%)`. (c) Left scrim for text legibility: `linear-gradient(to right, rgba(5,11,26,.65), transparent 55%)`. |
| `z-10` | Glow orbs | Cyan radial behind the stack: `radial-gradient(ellipse 380px 520px at 50% 50%, rgba(34,211,238,.25), transparent 70%)`. Red radial under the base: `radial-gradient(ellipse 320px 90px at 50% 92%, rgba(255,45,85,.45), transparent 70%)`. |
| `z-20` | Content grid | `relative`, 3 columns. Header and tagline are `absolute`. |
| `z-20` | Connector lines | Absolute, between the stack and the right-hand badges. |
| `z-30` | Slab stack | Always above the connectors. The hovered slab goes to `z-40`. |
| `z-40` | Beam and base ring | Vertical light beam through the stack center, glowing ring at the base. |

## 2. Advanced CSS Effects

### Glows (box-shadow / drop-shadow)

- **Cyan slab:** `0 0 24px rgba(34,211,238,.45), 0 0 60px rgba(37,99,235,.35), inset 0 0 20px rgba(125,211,252,.3)`
- **Red G slab:** `0 0 24px rgba(255,45,85,.55), 0 0 70px rgba(239,43,74,.4), inset 0 0 20px rgba(255,120,140,.3)`
- **Slab hover:** raise the first two layers to 0.7 opacity and add `0 0 90px` bloom.
- **Letter badges (circles):** `0 0 14px rgba(34,211,238,.5), inset 0 0 10px rgba(34,211,238,.25)`
- **Icons:** `drop-shadow(0 0 6px rgba(34,211,238,.8))`
- **Human figure on top:** `drop-shadow(0 0 16px #22D3EE)` plus a concentric ring glow beneath it.
- **Base ring:** `0 0 40px rgba(34,211,238,.6), 0 0 80px rgba(255,45,85,.35)`
- **Logo:** subtle `drop-shadow(0 0 10px rgba(34,211,238,.35))`

### Glass (backdrop-filter)

- **Slabs:** `backdrop-blur-md` (12px), `bg` at 35–55% opacity, 1px border `rgba(125,211,252,.6)`.
- **Right panel rows:** optional `backdrop-blur-sm` (4px) over `bg-[#050B1A]/30`. The scrim carries most of the contrast, so this is only for legibility.
- **Feature icons row (left):** no blur, text only.

### Gradients (depth)

- **Slab top face:** `linear-gradient(135deg, rgba(103,232,249,.65), rgba(37,99,235,.4))`
- **Slab side/thickness:** `linear-gradient(to bottom, rgba(37,99,235,.7), rgba(8,30,90,.9))`
- **Red slab:** `linear-gradient(135deg, rgba(255,120,140,.6), rgba(190,18,60,.45))`
- **Slab shine:** diagonal white sheen overlay, `linear-gradient(115deg, transparent 35%, rgba(255,255,255,.18) 50%, transparent 65%)`
- **Headline cyan line:** solid `#22D3EE`, or a subtle `bg-clip-text` gradient from `#22D3EE` to `#38BDF8`.
- **Beam:** `linear-gradient(to bottom, #22D3EE, rgba(34,211,238,.1))`, 2px wide, with `blur-[1px]`.

### 3D slab construction

- Parent `perspective: 1200px`. Each slab is `rotateX(62deg)` with a thickness pseudo-element (`::after`, 14px, side gradient).
- Vertical pitch is about 105px, with slabs overlapping by negative margin.
- Slab width is about 300px, with a skewed or clip-path diamond outline.
- Letter (H, A, O…) sits on the left corner of each face, `text-4xl font-bold`, with a text glow.
- Icon sits at the slab center.

### Palette tokens (tailwind.config extend)

- `ink #050B1A`
- `cyan-glow #22D3EE`
- `blue-core #2563EB`
- `red-gov #FF2D55`
- `text-dim #CBD5E1`

## 3. Layout & Positioning

- **Root:** `relative w-full aspect-video overflow-hidden` (or `min-h-screen`).
- **Main grid:** `grid grid-cols-[1.1fr_0.8fr_1.1fr] items-center px-16 py-12 gap-x-8`.
- **Header logo:** `absolute top-12 left-[8%]`, mark 56px plus a two-line wordmark (`tracking-[0.15em]`).
- **Tagline:** `absolute top-12 right-16`, `tracking-[0.2em] text-xl`. "ASPIRE." white, "ACT." cyan, "ACHIEVE." red.
- **Left column:**
  - Eyebrow: `text-sm tracking-[0.3em] text-slate-300 mb-4`
  - H1: `text-7xl font-extrabold tracking-tight`
  - Subhead: `text-4xl font-bold`, with "Human at the Core." in cyan
  - Body: `text-lg max-w-md mt-6 leading-relaxed`, with "human authority runs through every layer" in bold
  - Feature row: `flex gap-8 mt-10`, 1px `white/20` vertical dividers, icon 40px plus a `text-sm` label
- **Center column:** `relative h-[720px]`, slabs `absolute left-1/2 -translate-x-1/2`, each at `top: i * 105px`.
- **Right column:** `flex flex-col justify-between h-[720px]`, 7 rows that align 1:1 with the slabs.
- **Row anatomy:** `grid grid-cols-[48px_40px_1fr] gap-x-4 items-start`, badge circle 48px with a 2px border, icon 28px, then title (`text-lg font-semibold text-cyan-400`) and description (`text-sm leading-snug text-slate-200 max-w-[320px]`).
- **Connectors:** `absolute h-px` cyan at 60% opacity, with a 6px end dot, from the slab edge to the badge. Row G uses red.
- **Spacing scale:** 4 / 8 / 16 / 24 / 32 / 64px. Content gutter is 64px, row pitch about 105px.
- **Type:** Inter or Sora for body, Space Grotesk or Sora for H1. Uppercase tracked styles for the eyebrow and tagline.

## 4. Animation & Interaction

**Shared state:** `activeIndex` in React (`useState`). Hovering a right-hand row or a slab highlights both together.

### Hover (row)

- `translateX(6px)` over 200ms ease-out
- Title brightens to white
- Badge glow ×1.5, border goes from `cyan-400/70` to `cyan-300`
- Connector line goes to 100% opacity and gets a glow

### Hover (slab)

- `translateY(-10px) scale(1.03)` over 300ms
- Glow opacity from 0.45 to 0.7, with a bloom ring
- Other slabs dim to 70%

### Ambient

- Whole stack floats `translateY(0 → -6px → 0)`, 6s ease-in-out, infinite
- Beam pulses opacity 0.6 → 1, 3s
- Base ring: slow glow pulse, 4s
- Red G slab: faint "breathing" glow, 3.5s

### Entrance (on mount)

- Slabs drop in from top with an 80ms stagger (H first, V last)
- Right-hand rows fade and slide from the right with a matching stagger
- Connector lines draw via `scaleX(0 → 1)` after their slab lands

### Accessibility

Wrap ambient animations in `motion-safe:`. Rows get `tabIndex=0` with the same focus and hover state. All text keeps at least a 4.5:1 contrast ratio over the scrims.

## 5. Responsive & Build Notes

- **Below 1024px:** collapse to one column in the order headline, stack (scaled to 0.7), then the 7-item list. Connectors hide.
- **Icons:** `lucide-react` (User, Network/Share2, Workflow, Database, Wrench, ShieldCheck, TrendingUp, Brain, Target).
- **Logo:** needs an SVG export.

## Open Items Before Coding

1. Do you have a clean background photo file, or should a CSS gradient stand-in be used (night-sky gradient with a sunset glow)?
2. Should this be a full-viewport hero or a fixed 16:9 canvas that scales?
