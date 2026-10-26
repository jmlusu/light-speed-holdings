# Target Application Context & Guardrails

### 1. Workspace Boundaries
- The active, deployable Vite application root is: `./marketing_site/`.
- All source code, components, styles, and assets must live strictly inside `./marketing_site/src/`.
- Never modify or create files outside the `marketing_site/` directory.

### 2. Design System & Styling
- Tailwind CSS is configured via `@tailwindcss/vite` in `./marketing_site/src/index.css`.
- Brand design tokens reside in `./marketing_site/brand/tokens/brand-tokens.css`.
- Data registries live in `./marketing_site/data/` and must maintain existing TypeScript export contracts.
