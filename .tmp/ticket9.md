## Question

Prototype the CEO dashboard hero section on `/` combining:
- Org Health gauge (0–100, colored by band, with trend sparkline)
- Company-KPI cards (KPI-003, KPI-004 live; KPI-001/002/005 honest "n/a")
- Layout: gauge left, KPI cards right (responsive stack on mobile)

Requirements:
- Use existing Alpine `dashboard()` component in `app.js`
- Add `orgHealth` state: `{ score, band, trend[] }`
- Fetch `/api/org-health` on `loadDashboard()` (poll + WS `kpi_update` for live)
- Gauge: Chart.js doughnut or custom SVG (no new deps); sparkline via Chart.js line
- KPI cards: reuse `companyKPIs` rendering from `/kpis` page (`initCompanyKPICharts` exists)
- CSP compliant: no inline scripts beyond existing Tailwind config
- WS: listen for `kpi_update` with `org_health` payload

Insertion point in `index.html`: after top KPI cards row, before charts row.

**Blocked by: Inventory dashboard telemetry sources for the Org Health score (#23), Map the dashboard frontend for gauge and KPI cards (#25), Choose the Org Health score composition and config schema (#26)**
