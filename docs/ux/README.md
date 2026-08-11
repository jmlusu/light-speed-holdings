# UX Documentation Index

> User experience documentation for AI Company Builder.

---

## Documents

| Document | Description | Audience |
|----------|-------------|----------|
| [DASHBOARD-DESIGN.md](DASHBOARD-DESIGN.md) | Dashboard information architecture, navigation, user flows, wireframes | Product, Design, Frontend |
| [CLI-DESIGN.md](CLI-DESIGN.md) | Command naming, output formatting, error handling, color system | Product, Backend, DevRel |
| [DEVELOPER-EXPERIENCE.md](DEVELOPER-EXPERIENCE.md) | Onboarding, configuration, testing, debugging workflows | Developers |
| [NOTIFICATION-DESIGN.md](NOTIFICATION-DESIGN.md) | Notification events, channels, formatting, priority levels | Product, Backend |
| [ACCESSIBILITY.md](ACCESSIBILITY.md) | Color contrast, screen reader support, keyboard navigation | Product, Design, QA |

---

## Design System Summary

### Color Palette

| Semantic | Hex | Usage |
|----------|-----|-------|
| Brand Blue | `#0284c7` | Primary actions, links |
| Success Green | `#16a34a` | Completed, approved |
| Warning Amber | `#d97706` | Pending, attention |
| Error Red | `#dc2626` | Failed, rejected, escalated |
| Info Purple | `#9333ea` | Approvals, premium tier |

### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | System | 24px | 600 |
| H2 | System | 20px | 600 |
| H3 | System | 16px | 600 |
| Body | System | 14px | 400 |
| Code | Monospace | 13px | 400 |
| Small | System | 12px | 400 |

### Spacing

| Token | Value |
|-------|-------|
| `xs` | 4px |
| `sm` | 8px |
| `md` | 16px |
| `lg` | 24px |
| `xl` | 32px |
| `2xl` | 48px |

### Border Radius

| Element | Radius |
|---------|--------|
| Cards | 12px |
| Buttons | 8px |
| Inputs | 8px |
| Badges | 9999px (pill) |
| Modals | 16px |

---

## User Personas

### 1. CEO (Human Operator)

- **Goal**: Monitor company health at a glance
- **Time**: < 2 minutes per check
- **Focus**: KPIs, escalations, approvals
- **Channel**: Dashboard (primary), CLI (secondary)

### 2. Manager (Department Head)

- **Goal**: Review department KPIs and agent performance
- **Time**: 5-10 minutes per review
- **Focus**: Department metrics, team workload
- **Channel**: Dashboard (primary)

### 3. Operator (Technical Staff)

- **Goal**: Handle escalations, approve requests
- **Time**: Continuous monitoring
- **Focus**: Approval queue, escalation events
- **Channel**: CLI (primary), Dashboard (secondary)

### 4. Developer (Contributor)

- **Goal**: Understand system, contribute code
- **Time**: Hours per session
- **Focus**: Architecture, testing, debugging
- **Channel**: CLI (primary), Documentation (primary)

---

## Implementation Priorities

### Phase 1 (Current)

- [x] Dashboard KPI cards
- [x] Task table with filters
- [x] Approval/escalation cards
- [x] Org chart visualization
- [x] Model routing display
- [x] CLI color system
- [x] Error message format

### Phase 2 (Next)

- [ ] Notification center in dashboard
- [ ] Keyboard navigation
- [ ] Screen reader support
- [ ] Mobile responsive design
- [ ] Chart patterns for colorblind users
- [ ] CLI `--json` mode for all commands

### Phase 3 (Future)

- [ ] Department-specific views
- [ ] Memory search interface
- [ ] Workflow visualization
- [ ] Real-time collaboration
- [ ] Email/Slack notifications
- [ ] Dark mode support
