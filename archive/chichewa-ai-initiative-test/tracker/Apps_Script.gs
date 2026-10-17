/**
 * CHICHEWA AI INITIATIVE — NEGOTIATION TRACKER AUTOMATION
 * Google Apps Script for daily standup email, overdue alerts, and Notion integration
 *
 * SETUP INSTRUCTIONS:
 * 1. Open Google Sheet → Extensions → Apps Script
 * 2. Paste this code into Code.gs
 * 3. Save → Run setupTriggers() → Authorize
 * 4. Notion API key and email are pre-configured below
 */

// ============================================================
// CONFIGURATION
// ============================================================

function getConfig() {
  return {
    // Notion configuration
    NOTION_API_KEY: 'YOUR_NOTION_API_KEY',  // REPLACE WITH YOUR NOTION INTEGRATION TOKEN
    NOTION_DATABASE_ID: 'YOUR_DATABASE_ID',  // UPDATE THIS: Open Notion DB → Share → Copy link → extract 32-char ID

    // Email for reports
    REPORT_EMAIL: 'jmlusu@gmail.com',

    // Sheet names (must match your tab names)
    SHEETS: {
      OVERVIEW: 'Stakeholder Overview',
      OI: 'OI JDA',
      ZBS: 'ZBS License',
      MINAG: 'MinAg MoU',
      WB: 'WB Trust Fund',
      GATES: 'Gate Tracker',
      RISKS: 'Risk & Issues'
    },

    // Column positions (0-indexed)
    COL: {
      STATUS: 6,       // Column G (Status R/Y/G)
      DUE_DATE: 5,     // Column F (Due Date)
      OWNER: 4,        // Column E (Owner)
      DELIVERABLE: 2,  // Column C (Deliverable)
      PRIORITY: 8,     // Column I (Priority - some sheets)
      NOTES: 7         // Column H (Notes)
    },

    // Timezone
    TIMEZONE: 'Africa/Blantyre',  // CAT (UTC+2)

    // Critical dates
    GATE_1_DATE: '2026-09-30',
    GATE_2_DATE: '2026-10-30',
    GATE_3_DATE: '2026-11-29'
  };
}

// ============================================================
// DAILY STANDUP — Email report (runs 9 AM CAT daily)
// ============================================================

function dailyStandup() {
  const config = getConfig();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const today = new Date();
  const todayStr = Utilities.formatDate(today, config.TIMEZONE, 'yyyy-MM-dd');

  let report = '📊 DAILY STANDUP — ' + todayStr + '\n';
  report += 'Chichewa AI Initiative — Negotiation Tracker\n';
  report += '================================================\n\n';

  // Gate countdown
  const gate1 = new Date(config.GATE_1_DATE);
  const daysToGate1 = Math.ceil((gate1 - today) / (1000 * 60 * 60 * 24));

  let gateStatus = '';
  if (daysToGate1 > 0) {
    gateStatus = '⏰ Gate 1 (Day 30): ' + daysToGate1 + ' days remaining — ' + config.GATE_1_DATE;
  } else if (daysToGate1 === 0) {
    gateStatus = '🚨 GATE 1 TODAY — GO/NO-GO DECISION REQUIRED';
  } else {
    gateStatus = '✅ Gate 1 passed (' + Math.abs(daysToGate1) + ' days ago)';
  }
  report += gateStatus + '\n\n';

  // Iterate through partner sheets
  const sheets = [config.SHEETS.OI, config.SHEETS.ZBS, config.SHEETS.MINAG, config.SHEETS.WB];
  let hasItems = false;

  for (const sheetName of sheets) {
    try {
      const sheet = ss.getSheetByName(sheetName);
      if (!sheet) continue;

      const data = sheet.getDataRange().getValues();
      let overdue = [];
      let dueToday = [];
      let dueThisWeek = [];

      for (let i = 1; i < data.length; i++) {
        const dueDateStr = data[i][config.COL.DUE_DATE];
        const status = data[i][config.COL.STATUS];
        const owner = data[i][config.COL.OWNER];
        const deliverable = data[i][config.COL.DELIVERABLE];
        const priority = data[i][config.COL.PRIORITY] || 'Medium';

        if (!dueDateStr || dueDateStr === '') continue;
        if (status === 'Done' || status === 'Completed') continue;

        const dueDate = new Date(dueDateStr);
        const diffDays = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));

        if (diffDays < 0) {
          overdue.push({ sheet: sheetName, deliverable, owner, daysOverdue: Math.abs(diffDays), priority });
        } else if (diffDays === 0) {
          dueToday.push({ sheet: sheetName, deliverable, owner, priority });
        } else if (diffDays <= 7) {
          dueThisWeek.push({ sheet: sheetName, deliverable, owner, daysOut: diffDays, priority });
        }
      }

      if (overdue.length > 0) {
        hasItems = true;
        report += '🚨 OVERDUE — ' + sheetName + '\n';
        for (const item of overdue) {
          const pEmoji = item.priority === 'Critical' ? '🔴 ' : item.priority === 'High' ? '🟠 ' : '🔵 ';
          report += pEmoji + item.deliverable + ' (+' + item.daysOverdue + 'd) — ' + item.owner + '\n';
        }
        report += '\n';
      }

      if (dueToday.length > 0) {
        hasItems = true;
        report += '📅 DUE TODAY — ' + sheetName + '\n';
        for (const item of dueToday) {
          const pEmoji = item.priority === 'Critical' ? '🔴 ' : item.priority === 'High' ? '🟠 ' : '🔵 ';
          report += pEmoji + item.deliverable + ' — ' + item.owner + '\n';
        }
        report += '\n';
      }

      if (dueThisWeek.length > 0) {
        hasItems = true;
        report += '📋 DUE THIS WEEK — ' + sheetName + ' (' + dueThisWeek.length + ' items)\n';
        for (const item of dueThisWeek) {
          report += '  • ' + item.deliverable + ' (' + item.daysOut + 'd) — ' + item.owner + '\n';
        }
        report += '\n';
      }

    } catch (e) {
      Logger.log('Error processing sheet ' + sheetName + ': ' + e.toString());
    }
  }

  if (!hasItems) {
    report += '✅ No overdue or due-today items. All on track.\n\n';
  }

  // Gate readiness
  const gateCheck = checkGateReadiness(config, ss);
  report += '--- GATE 1 READINESS ---\n';
  report += gateCheck.readyCount + '/' + gateCheck.totalCount + ' criteria complete\n';
  for (const detail of gateCheck.details) {
    report += '  ' + detail.replace(/[:✅❌]/g, '').trim() + '\n';
  }

  report += '\n---\n';
  report += 'Auto-generated by Negotiation Tracker • ' + todayStr + ' CAT\n';
  report += 'View tracker: [Google Sheet Link]\n';

  // Send email
  MailApp.sendEmail({
    to: config.REPORT_EMAIL,
    subject: '[Chichewa AI] Daily Standup — ' + todayStr,
    body: report
  });

  // Log last run
  const tracker = ss.getSheetByName(config.SHEETS.GATES);
  if (tracker) {
    const lastRow = tracker.getLastRow();
    tracker.getRange(lastRow + 1, 1).setValue('Last Standup');
    tracker.getRange(lastRow + 1, 2).setValue(todayStr);
  }

  Logger.log('Daily standup email sent to ' + config.REPORT_EMAIL);
}

// ============================================================
// OVERDUE ALERT — Email every 4 hours if critical items overdue
// ============================================================

function overdueAlert() {
  const config = getConfig();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const today = new Date();

  const sheets = [config.SHEETS.OI, config.SHEETS.ZBS, config.SHEETS.MINAG, config.SHEETS.WB];
  let overdueItems = [];

  for (const sheetName of sheets) {
    const sheet = ss.getSheetByName(sheetName);
    if (!sheet) continue;

    const data = sheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      const dueDateStr = data[i][config.COL.DUE_DATE];
      const status = data[i][config.COL.STATUS];
      const owner = data[i][config.COL.OWNER];
      const deliverable = data[i][config.COL.DELIVERABLE];
      const priority = data[i][config.COL.PRIORITY] || 'Medium';

      if (!dueDateStr || dueDateStr === '') continue;
      if (status === 'Done' || status === 'Completed') continue;

      const dueDate = new Date(dueDateStr);
      const diffDays = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));

      if (diffDays < 0) {
        overdueItems.push({ sheet: sheetName, deliverable, owner, daysOverdue: Math.abs(diffDays), priority });
      }
    }
  }

  if (overdueItems.length === 0) return;

  // Only alert on Critical/High priority overdue
  overdueItems = overdueItems.filter(item => item.priority === 'Critical' || item.priority === 'High');
  if (overdueItems.length === 0) return;

  // Sort by severity
  overdueItems.sort((a, b) => {
    const priorityOrder = { 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return b.daysOverdue - a.daysOverdue;
  });

  let text = '🚨 OVERDUE DELIVERABLES — ACTION REQUIRED\n\n';

  for (const item of overdueItems) {
    const pEmoji = item.priority === 'Critical' ? '🔴 ' : '🟠 ';
    text += pEmoji + '*' + item.sheet + '*: ' + item.deliverable +
            ' (+' + item.daysOverdue + 'd overdue) — Owner: ' + item.owner + '\n';
  }

  text += '\n⚠️ Please update status or blockers in the tracker immediately.';

  // Send email alert
  MailApp.sendEmail({
    to: config.REPORT_EMAIL,
    subject: '🚨 [Chichewa AI] Overdue Alert — ' + overdueItems.length + ' critical items',
    body: text
  });

  Logger.log('Overdue alert sent for ' + overdueItems.length + ' items');
}

// ============================================================
// GATE READINESS CHECK
// ============================================================

function checkGateReadiness(config, ss) {
  const today = new Date();

  const gate1Criteria = [
    { sheet: config.SHEETS.OI, match: 'JDA signed (GATE 1)' },
    { sheet: config.SHEETS.ZBS, match: 'Data License Agreement signed (GATE 1)' },
    { sheet: config.SHEETS.MINAG, match: 'MoU signed (GATE 1)' }
  ];

  let readyCount = 0;
  let totalCount = gate1Criteria.length;
  let details = [];

  for (const criterion of gate1Criteria) {
    const sheet = ss.getSheetByName(criterion.sheet);
    if (!sheet) continue;

    const data = sheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      const deliverable = data[i][config.COL.DELIVERABLE] || '';
      const status = data[i][config.COL.STATUS] || '';

      if (deliverable.includes(criterion.match)) {
        if (status === 'Done' || status === 'Completed') {
          readyCount++;
          details.push('✅ ' + deliverable);
        } else {
          details.push('❌ ' + deliverable + ' — Status: ' + status);
        }
      }
    }
  }

  return { readyCount, totalCount, details };
}

// ============================================================
// NOTION INTEGRATION — Sync status to Notion database
// ============================================================

function syncToNotion() {
  const config = getConfig();
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  if (config.NOTION_DATABASE_ID === 'YOUR_DATABASE_ID') {
    Logger.log('Notion sync skipped: DATABASE_ID not configured');
    return;
  }

  const sheets = [config.SHEETS.OI, config.SHEETS.ZBS, config.SHEETS.MINAG, config.SHEETS.WB];
  let synced = 0;

  for (const sheetName of sheets) {
    const sheet = ss.getSheetByName(sheetName);
    if (!sheet) continue;

    const data = sheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      const deliverable = data[i][config.COL.DELIVERABLE];
      const owner = data[i][config.COL.OWNER];
      const dueDate = data[i][config.COL.DUE_DATE];
      const status = data[i][config.COL.STATUS];
      const priority = data[i][config.COL.PRIORITY] || 'Medium';
      const notes = data[i][config.COL.NOTES] || '';

      if (!deliverable || deliverable === '') continue;

      // Map status to Notion status
      let notionStatus = 'To-do';
      if (status === 'Done' || status === 'Completed') notionStatus = 'Done';
      else if (status === 'In Progress') notionStatus = 'In progress';
      else if (status === 'Blocked') notionStatus = 'Blocked';

      const payload = {
        parent: { database_id: config.NOTION_DATABASE_ID },
        properties: {
          'Name': { title: [{ text: { content: deliverable } }] },
          'Status': { status: { name: notionStatus } },
          'Assignee': { people: [] },
          'Due Date': dueDate ? { date: { start: dueDate } } : {},
          'Priority': { select: { name: priority } },
          'Source': { select: { name: sheetName } },
          'Notes': { rich_text: [{ text: { content: notes } }] }
        }
      };

      try {
        UrlFetchApp.fetch('https://api.notion.com/v1/pages', {
          method: 'post',
          contentType: 'application/json',
          headers: {
            'Authorization': 'Bearer ' + config.NOTION_API_KEY,
            'Notion-Version': '2022-06-28'
          },
          payload: JSON.stringify(payload)
        });
        synced++;
      } catch (e) {
        Logger.log('Notion sync failed for ' + deliverable + ': ' + e.toString());
      }
    }
  }

  Logger.log('Notion sync complete: ' + synced + ' items');
}

// ============================================================
// WEEKLY SUMMARY REPORT — Email Monday 10 AM CAT
// ============================================================

function weeklySummaryReport() {
  const config = getConfig();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const today = new Date();
  const todayStr = Utilities.formatDate(today, config.TIMEZONE, 'yyyy-MM-dd');

  let summary = 'CHICHEWA AI INITIATIVE — WEEKLY NEGOTIATION SUMMARY\n';
  summary += 'Week of ' + todayStr + '\n\n';

  // Gate status
  const gateCheck = checkGateReadiness(config, ss);
  summary += 'GATE 1 STATUS: ' + gateCheck.readyCount + '/' + gateCheck.totalCount + ' criteria met\n';
  for (const detail of gateCheck.details) {
    summary += '  ' + detail.replace(/[✅❌]/g, '').trim() + '\n';
  }

  // Partner status
  const sheets = [config.SHEETS.OI, config.SHEETS.ZBS, config.SHEETS.MINAG, config.SHEETS.WB];

  for (const sheetName of sheets) {
    const sheet = ss.getSheetByName(sheetName);
    if (!sheet) continue;

    summary += '\n--- ' + sheetName.toUpperCase() + ' ---\n';

    const data = sheet.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      const deliverable = data[i][config.COL.DELIVERABLE];
      const owner = data[i][config.COL.OWNER];
      const status = data[i][config.COL.STATUS];
      const dueDate = data[i][config.COL.DUE_DATE];
      const notes = data[i][config.COL.NOTES] || '';

      if (!deliverable || deliverable === '') continue;

      summary += '• [' + status + '] ' + deliverable + ' — ' + owner;
      if (dueDate) summary += ' (Due: ' + dueDate + ')';
      if (notes) summary += ' — ' + notes.substring(0, 80);
      summary += '\n';
    }
  }

  // Risk summary
  summary += '\n--- RISKS & BLOCKERS ---\n';
  const riskSheet = ss.getSheetByName(config.SHEETS.RISKS);
  if (riskSheet) {
    const riskData = riskSheet.getDataRange().getValues();
    for (let i = 1; i < riskData.length; i++) {
      const risk = riskData[i][1];
      const severity = riskData[i][3];
      const status = riskData[i][6];

      if (status === 'Closed' || status === 'Resolved') continue;

      summary += '• [' + severity + '] ' + risk + ' — ' + status + '\n';
    }
  }

  // Send email
  MailApp.sendEmail({
    to: config.REPORT_EMAIL,
    subject: '[Chichewa AI] Weekly Negotiation Summary — ' + todayStr,
    body: summary
  });

  Logger.log('Weekly summary sent to ' + config.REPORT_EMAIL);
}

// ============================================================
// TRIGGER SETUP — Run once to install triggers
// ============================================================

function setupTriggers() {
  // Clear existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    ScriptApp.deleteTrigger(trigger);
  }

  // Daily standup at 9 AM CAT (7 AM UTC)
  ScriptApp.newTrigger('dailyStandup')
    .timeBased()
    .everyDays(1)
    .atHour(7)
    .create();

  // Overdue alert every 4 hours (only for Critical/High)
  ScriptApp.newTrigger('overdueAlert')
    .timeBased()
    .everyHours(4)
    .create();

  // Weekly summary report (Monday 10 AM CAT = 8 AM UTC)
  ScriptApp.newTrigger('weeklySummaryReport')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(8)
    .create();

  // Notion sync every 6 hours
  ScriptApp.newTrigger('syncToNotion')
    .timeBased()
    .everyHours(6)
    .create();

  Logger.log('All triggers installed successfully');
  MailApp.sendEmail({
    to: getConfig().REPORT_EMAIL,
    subject: '[Chichewa AI] Triggers Installed',
    body: 'All automated triggers have been set up:\n\n' +
      '• Daily Standup: 9 AM CAT (email)\n' +
      '• Overdue Alert: Every 4 hours (email, Critical/High only)\n' +
      '• Weekly Report: Monday 10 AM CAT (email)\n' +
      '• Notion Sync: Every 6 hours\n\n' +
      'Run "Check Gate Readiness" from the menu anytime.'
  });
}

// ============================================================
// MENU: Add custom menu to spreadsheet
// ============================================================

function onOpen() {
  const ui = SpreadsheetApp.getUi();

  ui.createMenu('🤖 Negotiation Tracker')
    .addItem('📊 Generate Daily Standup (Email)', 'dailyStandup')
    .addItem('🚨 Run Overdue Alert (Email)', 'overdueAlert')
    .addItem('📈 Generate Weekly Report (Email)', 'weeklySummaryReport')
    .addItem('🔄 Sync to Notion', 'syncToNotion')
    .addSeparator()
    .addItem('⚙️ Setup/Reset Triggers', 'setupTriggers')
    .addItem('📋 Check Gate Readiness', function() {
      const config = getConfig();
      const ss = SpreadsheetApp.getActiveSpreadsheet();
      const result = checkGateReadiness(config, ss);
      SpreadsheetApp.getUi().alert(
        'Gate 1 Readiness: ' + result.readyCount + '/' + result.totalCount + '\n\n' +
        result.details.join('\n')
      );
    })
    .addToUi();
}
