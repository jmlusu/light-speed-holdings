# CHICHEWA AI INITIATIVE — NEGOTIATION TRACKER
## Setup Guide: Google Sheets + Apps Script Automation (Email + Notion)

---

## OVERVIEW

This tracker provides a single source of truth for all stakeholder negotiations, deliverables, and gate decisions. It includes 7 sheets plus Apps Script automation for **daily email standups**, **overdue email alerts**, **weekly email reports**, and **Notion two-way sync**.

**No Slack required** — all notifications go to email (`jmlusu@gmail.com`).

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

**Only ONE value to update:**
```javascript
NOTION_DATABASE_ID: 'YOUR_DATABASE_ID',  // UPDATE THIS
```

**How to get Notion Database ID:**
1. Open your Notion database (the one you want to sync to)
2. Click **Share** → **Copy link**
3. The URL looks like: `https://www.notion.so/workspace/32charID?v=...`
4. Copy the 32-character ID (the part after the last `/` and before `?v=`)
5. Paste it in place of `'YOUR_DATABASE_ID'`

**Already configured:**
- ✅ Notion API Key: `YOUR_NOTION_API_KEY` (update in Apps_Script.gs)
- ✅ Report Email: `jmlusu@gmail.com`
- ✅ Timezone: Africa/Blantyre (CAT)

### Step 3: Set Up Triggers
1. In Apps Script editor: select `setupTriggers` from the dropdown
2. Click **Run** (▶)
3. **Authorize**: Choose your Google account → Allow
   - Needs: Spreadsheet access, Gmail (send email), External URLs (Notion API)

This installs:
| Trigger | Schedule | Function |
|---------|----------|----------|
| Daily Standup Email | 9:00 AM CAT daily | `dailyStandup` |
| Overdue Alert Email | Every 4 hours (Critical/High only) | `overdueAlert` |
| Weekly Report Email | Monday 10:00 AM CAT | `weeklySummaryReport` |
| Notion Sync | Every 6 hours | `syncToNotion` |

### Step 4: Test
1. **Extensions → Apps Script → Select `dailyStandup` → Run**
2. Check email `jmlusu@gmail.com` for the standup message
3. **Extensions → Apps Script → Select `syncToNotion` → Run** (test)
4. Check Notion database for new pages
5. If issues: check **Apps Script → Executions** for errors

---

## 3. WORKFLOW — DAILY USAGE

### Daily Standup Cadence (9:00 AM CAT)

1. **Before standup** (automated): Email arrives at `jmlusu@gmail.com` with summary
2. **During standup** (15 min, daily): Review email on phone/laptop
   - Any 🔴 or 🟠 items → owners explain blockers
   - Update Status column in tracker DURING standup (keep it live)
   - Gate countdown → confirm we're on track
3. **After standup**: Owners update Notes with progress/blockers

### Overdue Alerts
- **Critical/High priority only** — emails every 4 hours if overdue
- Won't spam for Medium/Low priority items

### Weekly Review (Monday, 10:00 AM CAT)

1. Automated weekly summary email arrives
2. Review Gate 1 readiness %, partner status, risks
3. Update Blockers column for any ❌ items
4. Check next week's deadlines → proactive outreach

### Gate Reviews (Day 30 / 60 / 90)

1. **3 days before**: Email flags "Gate approaching"
2. **Gate day**:
   - Run `Check Gate Readiness` from menu (🤖 Negotiation Tracker)
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

## 6. NOTION DATABASE SETUP

For Notion sync to work, your target database must have these properties:

| Property Name | Type | Required |
|---------------|------|----------|
| **Name** | Title | Yes |
| **Status** | Status (with options: To-do, In progress, Blocked, Done) | Yes |
| **Assignee** | People | No |
| **Due Date** | Date | No |
| **Priority** | Select (Critical, High, Medium, Low) | Yes |
| **Source** | Select (OI JDA, ZBS License, MinAg MoU, WB Trust Fund) | Yes |
| **Notes** | Rich text | No |

If your database has different property names, update the `syncToNotion()` function mappings.

---

## 7. TROUBLESHOOTING

### Emails not arriving
1. Check spam/junk folder
2. Check **Apps Script → Executions → View failures**
3. Verify `REPORT_EMAIL` in `getConfig()` is correct
4. Test: Run `dailyStandup()` manually and watch Executions log

### Notion sync failing
1. Verify API key has access to the database (Notion Settings → Integrations → your integration → Add to database)
2. Check the database has properties named exactly: Name, Status, Assignee, Due Date, Priority, Source, Notes
3. Adjust property mappings in `syncToNotion()` if names differ

### Triggers canceled
- Google may disable triggers if script hits daily quota errors
- Re-run `setupTriggers()` from Apps Script
- Check quotas: **Apps Script → Project Settings → Quotas**

### Date parsing issues
- Ensure CSV dates imported as strings `YYYY-MM-DD` (Google Sheets should auto-detect)
- If not: select date column → Format → Date

---

## 8. FILE INDEX

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
5. Update `NOTION_DATABASE_ID` in `getConfig()`
6. Run `setupTriggers()` → authorize
7. Add conditional formatting + freeze headers
8. Test: run `dailyStandup()` → check email → check Notion
9. Done ✓

---

**Maintained by:** Chief of Staff
**Last Updated:** September 2026
