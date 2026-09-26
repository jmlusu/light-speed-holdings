# Diagram: Website Architecture & Venture-Studio Execution Flow

## Mermaid Architecture Diagram

```mermaid
%% {init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#070A40', 'primaryContentColor': '#FFFFFF', 'secondaryColor': '#E63946', 'tertiaryColor': '#00BFFF', 'fontFamily': 'Arial, Helvetica, sans-serif'}}}%%

flowchart TB
    %% Brand/Palette node
    style BrandPalette fill:#070A40,stroke:#E63946,stroke-width:2px
    class BrandPalette

    %% UI Layer
    subgraph UI["UI Layer\n(Vite React SPA)"]
        direction LR
        Homepage["/`/` — Homepage\nHeroMist + Ripple + HeroSection\nStrategy Chasm + UseCaseCatalog\nCtaBand + StatCounter"]
        AboutPage["/`/about` — About Section\nInstitutional Charter + Thesis Banner"]
        TechPage["/`/technology` — Technology Page\nThreeCanvas + Full Navigation"]
        Solutions["`/solutions/*` — Solutions Ecosystem\n4 sub-pages with PillarNavigationCard"]
        Industries["`/industries/*` — Industries\n5 sector-specific pages"]
        ProofPages["`/work, /evidence, /insights` — Proof & Evidence"]
        Conversation["`/contact, /ask` — Conversation"]
        LegalPages["`/legal/*, /resources, /events, /news` — Supporting"]
        AllPages["All pages share: FloatingNav, SiteFooter"]
    end

    %% Brand Token Layer
    subgraph Tokens["Brand Token Layer\n(ADR-020 Locked)"]
        direction LR
        Navy["Navy #070A40"]
        Red["Red #E63946"]
        Cyan["Cyan #00BFFF"]
        style Navy fill:#070A40,color:#FFFFFF
        style Red fill:#E63946,color:#FFFFFF
        style Cyan fill:#00BFFF,color:#FFFFFF
    end

    %% Effect Layer
    subgraph Effects["Effect Layer"]
        direction LR
        Ripple["`ripple-on` — CSS ripple effect\nOn all nav links & CTA buttons"]
        HeroMist["`HeroMist` — Ambient mist\n6 blurred radial gradients\nGated on prefers-reduced-motion"]
        SmoothScroll["`smoothScrollToElement`\nCubic-bezier(0.25,1,0.5,1) over 650ms\nFalls back to scrollIntoView"]
        ThreeCanvas["`ThreeCanvas` — WebGL/three.js\nAbstract data flow visualization"]
    end

    %% Navigation Layer
    subgraph Nav["Navigation Layer"]
        direction LR
        TopNav["Desktop: hidden lg:flex\nTop horizontal bar"]
        MobileNav["Mobile: hamburger → fullscreen overlay"]
        PillarNav["PillarNavigationCard\n4 connected tactile pillars\nStrategy → Build → Govern → Scale"]
    end

    %% Data/Layer
    subgraph Data["Data & Catalog Layer"]
        direction LR
        SiteContent["`src/data/siteContent.ts` — Home page data"]
        CatalogData["`src/data/useCaseCatalogData.ts`\nOffers (7), Industries (5), Scenarios (8), Proof (12), Method"]
        RegistryData["`company-registry.yaml` — Agent configs\n152 verified configs, KPI metrics"]
        ThreeCanvasData["`src/ThreeCanvas.tsx` — 3D scene data"]
    end

    %% Execution Flow
    subgraph Flow["Venture-Studio Execution Flow"]
        direction LR
        Part1["Part 1: Homepage Brand Effects\n✅ Shipped\nCSS ripple, HeroMist, smooth scroll,\nADR-020 palette enforcement"]
        Part2["Part 2: Sector Positioning\n`02-sector-positioning.md`\nMarket positioning, category creation"]
        Part3["Part 3: Operating Model\n`03-operating-model.md`\nFive-tier approval, audit trails, compliance"]
        Part4["Part 4: Technical Architecture\n`04-technical-architecture.md`\nSystem diagrams, data pipelines, integration patterns"]
        Part5["Part 5: KPI Scorecard\n`05-kpi-scorecard.md`\nQuantified metrics, instrumentation roadmap"]
        ECL["ECL (Execution Change Log)\n`harness/changes/parking/...`\nphase: validate, validation_status: pass"]
    end

    %% Connections
    BrandPalette --> Tokens
    Tokens --> Ripple
    Tokens --> HeroMist
    Tokens --> SmoothScroll
    Tokens --> ThreeCanvas
    Tokens --> AllPages

    UI --> TopNav
    UI --> MobileNav
    UI --> PillarNav
    UI --> Homepage
    UI --> AboutPage
    UI --> TechPage
    UI --> Solutions
    UI --> Industries
    UI --> ProofPages
    UI --> Conversation
    UI --> LegalPages

    Nav --> UI
    Data --> SiteContent
    Data --> CatalogData
    Data --> RegistryData
    Data --> ThreeCanvasData

    Flow --> Part1
    Flow --> Part2
    Flow --> Part3
    Flow --> Part4
    Flow --> Part5
    Flow --> ECL

    style UI fill:#F0F9FF,stroke:#070A40,stroke-width:1px
    style Tokens fill:#F0F9FF,stroke:#E63946,stroke-width:1px
    style Effects fill:#F0F9FF,stroke:#00BFFF,stroke-width:1px
    style Nav fill:#F0F9FF,stroke:#070A40,stroke-width:1px
    style Data fill:#F0F9FF,stroke:#070A40,stroke-width:1px
    style Flow fill:#F0F9FF,stroke:#E63946,stroke-width:1px
```

## Mermaid Venture-Studio Workflow Diagram

```mermaid
flowchart TD
    style BrandPalette fill:#070A40,stroke:#E63946,stroke-width:2px
    class BrandPalette

    Start["🟢 Start: Idea & Scoping\n\n- Market need identification\n- CEO approval (Jack Mlusu)\n- Define Part boundary (1–5)"]

    Part1Trigger["📦 Part 1: Homepage Brand Effects\n\n- CSS ripple effects\n- HeroMist ambient mist\n- Smooth scroll cubic-bezier\n- ADR-020 palette enforcement\n\n✅ Status: SHIPPED\n\nBranch: archive/2026-09-24-ai-venture-studio-web-experience-brand-psychology/"]

    Part2Trigger["📦 Part 2: Sector Positioning\n\n- 02-sector-positioning.md\n- Market category creation\n- Competitive landscape\n- Value proposition\n\nBranch: docs/venture-studio/02-sector-positioning.md"]

    Part3Trigger["📦 Part 3: Operating Model\n\n- 03-operating-model.md\n- Five-tier approval matrix\n- Audit trail design\n- Regional compliance (Malawi, SADC)\n\nBranch: docs/venture-studio/03-operating-model.md"]

    Part4Trigger["📦 Part 4: Technical Architecture\n\n- 04-technical-architecture.md\n- System diagrams\n- Data pipeline patterns\n- Integration blueprints\n\nBranch: docs/venture-studio/04-technical-architecture.md"]

    Part5Trigger["📦 Part 5: KPI Scorecard\n\n- 05-kpi-scorecard.md\n- Quantified metrics\n- Instrumentation roadmap\n- Governance KPIs\n\nBranch: docs/venture-studio/05-kpi-scorecard.md"]

    Archive["📁 Archive ECLs\n\n- parking/ → completed/ on slot release\n- INDEX.json reindex\n- lint-ecl.ps1 validation"]

    Closeout["✅ Closeout\n\n- `harness-change.ps1 close completed`\n- Git commit with all 64 files\n- Post-commit: graphify update, lint, test"]

    %% Flow connections
    Start --> Part1Trigger
    Start --> Part2Trigger
    Start --> Part3Trigger
    Start --> Part4Trigger
    Start --> Part5Trigger

    Part1Trigger --> Archive
    Part2Trigger --> Archive
    Part3Trigger --> Archive
    Part4Trigger --> Archive
    Part5Trigger --> Archive

    Archive --> Closeout

    %% Status styling
    style Start fill:#BBF7D0,stroke:#059669,stroke-width:2px
    style Part1Trigger fill:#BBF7D0,stroke:#059669,stroke-width:2px
    style Part2Trigger fill:#BBF7D0,stroke:#059669,stroke-width:2px
    style Part3Trigger fill:#BBF7D0,stroke:#059669,stroke-width:2px
    style Part4Trigger fill:#BBF7D0,stroke:#059669,stroke-width:2px
    style Part5Trigger fill:#BBF7D0,stroke:#059669,stroke-width:2px
    style Archive fill:#FEF3C7,stroke:#D97706,stroke-width:2px
    style Closeout fill:#FBBF24,stroke:#EA580C,stroke-width:2px
```

## Diagram Key

| Symbol | Meaning |
|--------|---------|
| `🟢` | Process step / decision point |
| `📦` | Deliverable package |
| `📁` | Archive/state management |
| `✅` | Completed/shipped |
| `Branch:` | Git branch or file path reference |

## Color Mapping (ADR-020)

- **Navy `#070A40`**: Primary accent, primary text, section borders
- **Red `#E63946`**: Secondary accent, error states, CTA primary, honesty "Proven in-house" badges
- **Cyan `#00BFFF`**: Highlight accent, fieldable badges, pip active states, link highlights
- **White `#FFFFFF`**: Backgrounds, card surfaces (light theme)
- **Grey-dark `#334155`**: Default body text
- **Grey-light-text `#98a2a6`**: Secondary/placeholder text

---
*Diagrams generated from codebase analysis and ECL structure. Architecture diagram captures the Vite React SPA structure, brand token enforcement, effect layer, and navigation. Workflow diagram captures the Part 1–5 venture-studio execution flow from idea through closeout.*
