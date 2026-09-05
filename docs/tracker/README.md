# CHICHEWA AI INITIATIVE — NEGOTIATION TRACKER
## Setup Guide: Google Sheets + Apps Script Automation

---

## OVERVIEW

This tracker provides a single source of truth for all stakeholder negotiations, deliverables, and gate decisions. It includes 7 sheets plus Apps Script automation for daily standup sync, overdue alerts, weekly reports, and Notion integration.

---

## 1. SETUP — GOOGLE SHEETS

### Step 1: Create the Spreadsheet
1. Open [Google Sheets](https://sheets.new)
2. Name: **Chichewa AI Initiative — Negotiation Tracker**
3. Create 7 tabs (rename Sheet1, Sheet2, etc.):
   - `Stakeholder Overview`
   - `OI JDA`
   - `ZBS License`
   - `MinAg MoU`
   - `WB Trust Fund`
   - `Gate Tracker`
   - `Risk & Issues`

### Step 2: Import CSV Data
For each tab, import the corresponding CSV file:

| Tab Name | CSV File | How |
|----------|----------|-----|
| Stakeholder Overview | `Sheet1_Stakeholder_Overview.csv` | File → Import → Upload → Replace current sheet |
| OI JDA | `Sheet2_OI_JDA.csv` | Same |
| ZBS License | `Sheet3_ZBS_License.csv` | Same |
| MinAg MoU | `Sheet4_MinAg_MoU.csv` | Same |
| WB Trust Fund | `Sheet5_WB_Trust_Fund.csv` | Same |
| Gate Tracker | `Sheet6_Gate_Tracker.csv` | Same |
| Risk & Issues | `Sheet7_Risk_Issues.csv` | Same |

### Step 3: Share & Set Permissions
1. Click **Share** (top-right)
2. Add team members: CEO, CTO, COO, CLO, CSO, CFO, BD Lead, PM, ML Engineers, Malawi Liaison
3. Set permission: **Editor** (for all)
4. Consider adding: World Bank TTL, OI CTO as **Viewer** (optional)

### Step 4: Freeze Header Rows
For each data tab:
1. Select row 1
2. **View → Freeze → 1 row**

### Step 5: Apply Conditional Formatting (Status Column)

**Sheet 2-5 (Status column G):**
- Select G2:G100
- Format → Conditional formatting
- Add 4 rules:

| Rule | Format |
|------|--------|
| `G2` equals "Done" | Green fill |
| `G2` equals "In Progress" | Light yellow fill |
| `G2` equals "Not Started" | Light red fill |
| `G2` equals "Blocked" | Red fill + bold |

**Sheet 1 (Status Column G):**
- Select G2:G100
- `G2` equals "Green" → Green
- `G2` equals "Yellow" → Yellow
- `G2` equals "Red" → Red

### Step 6: Add Filter Views
For each data tab:
1. Header → filter icon
2. Create filter view per team lead:
   - "My Items" (filter by owner)
   - "Critical Only" (filter by priority)
   - "Due This Week"
   - "Overdue"

---

## 2. SETUP — APPS SCRIPT AUTOMATION

### Step 1: Open Apps Script Editor
1. In the spreadsheet: **Extensions → Apps Script**
2. Delete the default `function myFunction() {}`
3. Paste the contents of `Apps_Script.gs` into `Code.gs`
4. Save (Ctrl+S)

### Step 2: Configure Values
Edit the `getConfig()` function at the top of `Apps_Script.gs`:

**a) Slack Webhook URL:**
```javascript
const config = getConfig();
// Replace with your Slack Incoming Webhook:
// https://api.slack.com/messaging/webhooks → Create App → Add Incoming Webhooks
```

**b) Team Slack IDs:**
Replace `<@U00000000>` placeholders with real Slack user IDs:
```
How to find: Slack → Click user → Profile → More → Copy Member ID
```

**c) Notion API Key & Database ID** (for `syncToNotion`):
```
API Key: https://www.notion.so/my-integrations → Create integration → Copy token
Database ID: In Notion, open the database → Share → Copy link → extract 32-char ID
```

### Step 3: Set Up Triggers
1. In Apps Script editor: select `setupTriggers` from the dropdown
2. Click **Run** (▶)
3. **Authorize**: Choose your Google account → Allow (warns about permissions — it needs access to the spreadsheet, Gmail for weekly report, and external URLs for Slack/Notion)

This installs:
| Trigger | Schedule | Function |
|---------|----------|----------|
| Daily Standup | 9:00 AM CAT (7 AM UTC) | `dailyStandup` |
| Overdue Alert | Every 4 hours | `overdueAlert` |
| Weekly Report | Monday 10 AM CAT (8 AM UTC) | `weeklySummaryReport` |
| Notion Sync | Every 6 hours | `syncToNotion` |

### Step 4: Test
1. **Extensions → Apps Script → Select `dailyStandup` → Run**
2. Check Slack #chichewa-ai channel for the standup message
3. **Extensions → Apps Script → Select `overdueAlert` → Run** (test)
4. If Slack not showing: check **Apps Script → Executions** for errors

---

## 3. WORKFLOW — DAILY USAGE

### Daily Standup Cadence (9:00 AM CAT / 3:00 AM ET)

1. **Before standup** (automated): Script posts summary to Slack #chichewa-ai
2. **During standup** (15 min, daily): Review Slack summary
   - Any :red_circle: or :rotating_light: items → owners explain blockers
   - Update Status column in tracker DURING standup (keep it live)
   - Gate countdown → confirm we're on track
3. **After standup**: Owners update Notes with progress/blockers

### Weekly Review (Monday, 30 min)

1. Automated weekly summary email arrives from script (to CEO)
2. Review Gate 1 readiness %, partner status, risks
3. Update Blockers column for any :x: items
4. Check next week's deadlines → proactive outreach

### Gate Reviews (Day 30 / 60 / 90)

1. **3 days before**: Script flag "Gate approaching"
2. **Gate day**:
   - Run `Check Gate Readiness` from menu
   - CEO/Board decision (Approve/Pivot/Pause)
   - Record decision in `Gate Tracker` tab
   - Unlock next phase deliverables

---

## 4. ROLE GUIDE — WHO OWNS WHAT

| Item | Owner | Update Cadence |
|------|-------|----------------|
| Stakeholder Overview status | CoS | Daily |
| OI JDA deliverables | BD Lead + CLO | Daily (during negotiation) |
| ZBS License deliverables | CLO + ML Eng | Daily (during evaluation) |
| MinAg MoU deliverables | CoS + Malawi Liaison | Daily (during govt engagement) |
| WB Trust Fund deliverables | CSO | Weekly |
| Gate Tracker decisions | CEO/CoS | At gates |
| Risk & Issues log | CoS + all | Ongoing |

---

## 5. STATUS VOCABULARY (USE THESE EXACTLY)

| Status | Meaning | Action |
|--------|---------|--------|
| **Not Started** | No work begun | Schedule/assign |
| **In Progress** | Active work | Keep moving |
| **At Risk** | May miss deadline | Escalate blockers |
| **Blocked** | Waiting on external | List blocker + owner |
| **Done** | Complete + verified | Celebrate |
| **Deferred** | Moved to later phase | Update target date |

**Sheet 1 (Stakeholder) status:**
| Status | Meaning |
|--------|---------|
| **Green** | On track, no blockers |
| **Yellow** | At risk, needs attention |
| **Red** | Blocked, needs escalation |

---

## 6. TROUBLESHOOTING

### Slack messages not appearing
1. Check Webhook URL is correct (full starts with `https://hooks.slack.com/services/...`)
2. Check **Apps Script → Executions → View failures**
3. Test webhook manually with cURL:
   ```bash
   curl -X POST -H 'Content-type: application/json' \
   --data '{"text":"test"}' YOUR_WEBHOOK_URL
   ```

### Notion sync failing
1. Verify API key has access to the database
2. Check the database has properties named: Name, Status, Assignee, Due Date, Priority, Source, Notes
3. Adjust property mappings in `syncToNotion()` function

### Triggers canceled
- Google may disable triggers if script hits daily quota errors
- Re-run `setupTriggers()` from Apps Script
- Check quotas: **Apps Script → Project Settings → Quotas**

### Date parsing issues
- Ensure CSV dates imported as strings `YYYY-MM-DD` (Google Sheets should auto-detect)
- If not: select date column → Format → Date

---

## 7. EXTENSIONS (OPTIONAL)

### Add Google Calendar sync
In `dailyStandup()`, add:
```javascript
CalendarApp.createEvent('Chichewa AI Standup', start, end); // Create if not exists
```

### Add email digest to Malawi Liaison
Modify `weeklySummaryReport()` to include:
```javascript
MailApp.sendEmail({
  to: 'malawi@lightspeed.ai',
  subject: 'Weekly tracker update',
  body: summary,
  cc: 'bd@lightspeed.ai'
});
```

### Add auto-reminders before calls
```javascript
function callReminders() {
  // Check Stakeholder Overview for calls due in next 48h
  // Post to Slack with :telephone_receiver: icon
  // Implement in code below if needed
}
```

---

## FILE INDEX

```
docs/tracker/
├── Sheet1_Stakeholder_Overview.csv   → Tab: "Stakeholder Overview"
├── Sheet2_OI_JDA.csv                  → Tab: "OI JDA"
├── Sheet3_ZBS_License.csv             → Tab: "ZBS License"
├── Sheet4_MinAg_MoU.csv               → Tab: "MinAg MoU"
├── Sheet5_WB_Trust_Fund.csv           → Tab: "WB Trust Fund"
├── Sheet6_Gate_Tracker.csv            → Tab: "Gate Tracker"
├── Sheet7_Risk_Issues.csv             → Tab: "Risk & Issues"
├── Apps_Script.gs                     → Google Apps Script code
└── README.md                          → This file
```

---

## QUICK START (5 MINUTES)

1. Create Google Sheet → 7 tabs with names above
2. Import 7 CSVs (File → Import → Upload)
3. Share with team (Editor access)
4. Extensions → Apps Script → paste `Apps_Script.gs` → save
5. Configure Slack webhook + team IDs in `getConfig()`
6. Run `setupTriggers()` → authorize
7. Add conditional formatting + freeze headers
8. Done ✓

---

**Maintained by:** Chief of Staff
**Last Updated:** September 2026
