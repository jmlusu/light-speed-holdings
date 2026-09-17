# Client-Facing Web Application Sitemap

**Project:** LightSpeed Holdings Limited
**Framework:** React (Vite) + React Router v6
**Last Updated:** 2026-09-17

---

## Root

| Path | Description |
|------|-------------|
| `/` | Home page — primary entry point |

---

## Navigation Header (FloatingNav)

| Path | Label |
|------|-------|
| `/` | Home |
| `/offerings` | Offerings |
| `/solutions` | Solutions |
| `/industries` | Industries |
| `/ai-company-builder` | AI Company Builder |
| `/evidence` | Evidence |
| `/about` | About |
| `/insights` | Insights |
| `/contact` | Contact |

---

## Main Application Routes (App.tsx Router)

| Path | Component | Description |
|------|-----------|-------------|
| `/` | `HomePage` | Hero / value proposition entry point |
| `/about` | `AboutPage` | Company overview and mission |
| `/solutions` | `SolutionsPage` | High-level solutions overview |
| `/solutions/agentic-ai` | `SolutionDetailPage` | Agentic AI solution |
| `/solutions/digital-transformation` | `SolutionDetailPage` | Digital Transformation solution |
| `/solutions/data-intelligence` | `SolutionDetailPage` | Data & Intelligence solution |
| `/solutions/automation` | `SolutionDetailPage` | Intelligent Automation solution |
| `/solutions/strategy-advisory` | `SolutionDetailPage` | Strategy & Advisory solution |
| `/industries` | `IndustriesPage` | Industries vertical overview |
| `/industries/government` | `IndustryDetailPage` | Government industry |
| `/industries/development` | `IndustryDetailPage` | Development & Donor industry |
| `/industries/financial-services` | `IndustryDetailPage` | Financial Services industry |
| `/industries/healthcare` | `IndustryDetailPage` | Healthcare industry |
| `/industries/agriculture` | `IndustryDetailPage` | Agriculture industry |
| `/technology` | `TechnologyPage` | Technology overview page |
| `/work` | `WorkPage` | Work & Proof portfolio |
| `/insights` | `InsightsPage` | Evidence, research & agentic AI canon |
| `/offerings` | `OfferingsPage` | Client service catalog |
| `/evidence` | `EvidencePage` | Evidence & method |
| `/ai-company-builder` | `AiCompanyBuilderPage` | AI company registry & generator |
| `/contact` | `ContactPage` | Get in touch / booking form |
| `/legal/privacy` | `PrivacyPage` | Privacy policy |
| `/legal/terms` | `TermsPage` | Terms of service |

---

## Footer Column Links

### SOLUTIONS

| Path | Link Text |
|------|-----------|
| `/solutions/agentic-ai` | Agentic AI |
| `/solutions/digital-transformation` | Digital Transformation |
| `/solutions/data-intelligence` | Data & Intelligence |
| `/solutions/automation` | Intelligent Automation |
| `/solutions/strategy-advisory` | Strategy & Advisory |
| `/technology#governance` | AI Governance & Policy |

### INDUSTRIES

| Path | Link Text |
|------|-----------|
| `/industries/government` | Government |
| `/industries/development` | Development & Donor |
| `/industries/financial-services` | Financial Services |
| `/industries/healthcare` | Healthcare |
| `/industries/agriculture` | Agriculture |

### AI COMPANY BUILDER

| Path | Link Text |
|------|-----------|
| `/ai-company-builder` | Overview |
| `/technology` | Technology |
| `/contact` | Start a Conversation |

### TECHNOLOGY

| Path | Link Text |
|------|-----------|
| `/technology#architecture` | Architecture |
| `/technology#proof` | Technical Proof |
| `/technology#governance` | Security & Governance |

### COMPANY

| Path | Link Text |
|------|-----------|
| `/about` | About |
| `/work` | Work |
| `/insights` | Insights |
| `/contact` | Contact |

### LEGAL

| Path | Link Text |
|------|-----------|
| `/legal/privacy` | Privacy Policy |
| `/legal/terms` | Terms of Service |

---

## Route Title Mapping (SiteLayout ROUTE_TITLES)

| Path | Page Title |
|------|------------|
| `/` | `LIGHTSPEED HOLDINGS — Build the Intelligent Enterprise` |
| `/about` | `About \| LIGHTSPEED HOLDINGS` |
| `/solutions` | `Solutions \| LIGHTSPEED HOLDINGS` |
| `/solutions/agentic-ai` | `Agentic AI \| LIGHTSPEED HOLDINGS` |
| `/solutions/digital-transformation` | `Digital Transformation \| LIGHTSPEED HOLDINGS` |
| `/solutions/data-intelligence` | `Data & Intelligence \| LIGHTSPEED HOLDINGS` |
| `/solutions/automation` | `Intelligent Automation \| LIGHTSPEED HOLDINGS` |
| `/solutions/strategy-advisory` | `Strategy & Advisory \| LIGHTSPEED HOLDINGS` |
| `/industries` | `Industries \| LIGHTSPEED HOLDINGS` |
| `/industries/government` | `Government \| LIGHTSPEED HOLDINGS` |
| `/industries/development` | `Development & Donor \| LIGHTSPEED HOLDINGS` |
| `/industries/financial-services` | `Financial Services \| LIGHTSPEED HOLDINGS` |
| `/industries/healthcare` | `Healthcare \| LIGHTSPEED HOLDINGS` |
| `/industries/agriculture` | `Agriculture \| LIGHTSPEED HOLDINGS` |
| `/ai-company-builder` | `AI Company Builder \| LIGHTSPEED HOLDINGS` |
| `/technology` | `Technology \| LIGHTSPEED HOLDINGS` |
| `/work` | `Work & Proof \| LIGHTSPEED HOLDINGS` |
| `/insights` | `Evidence, Research & the Agentic AI Canon \| LIGHTSPEED HOLDINGS` |
| `/offerings` | `Client Service Catalog \| LIGHTSPEED HOLDINGS` |
| `/evidence` | `Evidence & Method \| LIGHTSPEED HOLDINGS` |
| `/contact` | `Start a Conversation \| LIGHTSPEED HOLDINGS` |
| `/legal/privacy` | `Privacy Policy \| LIGHTSPEED HOLDINGS` |
| `/legal/terms` | `Terms of Service \| LIGHTSPEED HOLDINGS` |

---

## Wildcard / Fallback

| Pattern | Behavior |
|---------|----------|
| `*` | Redirects to `/` (root) with `replace` |

---

## Sitemap Summary

- **21 top-level route paths** (excluding wildcard)
- **43 distinct URL paths** including slug variants and anchor links
- **9 main navigation items** in the floating header
- **5 footer column groups** with 21 total footer links
- All routes are rendered inside the shared `SiteLayout` component
- Page titles are auto-injected via the `ROUTE_TITLES` mapping in `SiteLayout`
- A catch-all `*` route ensures no dead ends — always redirects to homepage
