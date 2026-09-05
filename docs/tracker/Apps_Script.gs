/**
 * CHICHEWA AI INITIATIVE — NEGOTIATION TRACKER AUTOMATION
 * Google Apps Script for daily standup sync, overdue alerts, and Notion integration
 *
 * SETUP INSTRUCTIONS:
 * 1. Open Google Sheet → Extensions → Apps Script
 * 2. Paste this code into Code.gs
 * 3. Save → Set trigger (below) → Authorize
 * 4. Configure webhook URL in setConfig() below
 */

// ============================================================
// CONFIGURATION — UPDATE THESE VALUES
// ============================================================

function getConfig() {
  return {
    // Slack webhook URL for alerts
    SLACK_WEBHOOK_URL: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',

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

    // Today's standup time (UTC)
    STANDUP_HOUR: 7,   // 7 AM UTC = 9 AM CAT (Malawi)

    // Critical dates
    GATE_1_DATE: '2026-09-30',
    GATE_2_DATE: '2026-10-30',
    GATE_3_DATE: '2026-11-29',

    // Team member Slack IDs (for @mentions)
    TEAM_SLACK_IDS: {
      'CEO': '<@U00000000>',
      'CTO': '<@U00000001>',
      'COO': '<@U00000002',
      'CLO': '<@U00000003>',
      'CSO': '<@U00000004>',
      'BD Lead': '<@U00000005>',
      'PM': '<@U00000006>',
      'ML Eng': '<@U00000007>',
      'CTO/ML': '<@U00000001>',
      'Malawi Liaison': '<@U00000008>',
      'CFO': '<@U00000009>'
    }
  };
}

// ============================================================
// DAILY STANDUP — Auto-generate and post to Slack
// ============================================================

function dailyStandup() {
  const config = getConfig();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const today = new Date();
  const todayStr = Utilities.formatDate(today, 'UTC', 'yyyy-MM-dd');

  let blocks = [];

  // Header
  blocks.push({
    type: 'header',
    text: {
      type: 'plain_text',
      text: '📊 Daily Standup — ' + todayStr,
      emoji: true
    }
  });

  blocks.push({
    type: 'section',
    text: {
      type: 'mrkdwn',
      text: '*Chichewa AI Initiative — Negotiation Tracker*'
    }
  });

  blocks.push({ type: 'divider' });

  // Gate countdown
  const gate1 = new Date(config.GATE_1_DATE);
  const daysToGate1 = Math.ceil((gate1 - today) / (1000 * 60 * 60 * 24));

  let gateStatus = '';
  if (daysToGate1 > 0) {
    gateStatus = ':alarm_clock: *Gate 1 (Day 30):* ' + daysToGate1 + ' days remaining — ' + config.GATE_1_DATE;
  } else if (daysToGate1 === 0) {
    gateStatus = ':rotating_light: *GATE 1 TODAY* — GO/NO-GO DECISION REQUIRED';
  } else {
    gateStatus = ':white_check_mark: Gate 1 passed (' + Math.abs(daysToGate1) + ' days ago)';
  }

  blocks.push({
    type: 'section',
    text: {
      type: 'mrkdwn',
      text: gateStatus
    }
  });

  // Iterate through partner sheets and find overdue/today items
  const sheets = [config.SHEETS.OI, config.SHEETS.ZBS, config.SHEETS.MINAG, config.SHEETS.WB];

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

        const dueDate = new Date(dueDateStr);
        const diffDays = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));

        if (status === 'Done' || status === 'Completed') continue;

        const slackId = config.TEAM_SLACK_IDS[owner] || owner;

        if (diffDays < 0) {
          overdue.push({
            sheet: sheetName,
            deliverable: deliverable,
            owner: slackId,
            daysOverdue: Math.abs(diffDays),
            priority: priority
          });
        } else if (diffDays === 0) {
          dueToday.push({
            sheet: sheetName,
            deliverable: deliverable,
            owner: slackId,
            priority: priority
          });
        } else if (diffDays <= 7) {
          dueThisWeek.push({
            sheet: sheetName,
            deliverable: deliverable,
            owner: slackId,
            daysOut: diffDays,
            priority: priority
          });
        }
      }

      // Add overdue items
      if (overdue.length > 0) {
        let overdueText = ':rotating_light: *OVERDUE — ' + sheetName + '*\n';
        for (const item of overdue) {
          const priorityEmoji = item.priority === 'Critical' ? ':red_circle:' :
                               item.priority === 'High' ? ':large_orange_circle:' : ':large_blue_circle:';
          overdueText += priorityEmoji + ' ' + item.deliverable + ' (+' + item.daysOverdue + 'd) — ' + item.owner + '\n';
        }
        blocks.push({
          type: 'section',
          text: { type: 'mrkdwn', text: overdueText }
        });
      }

      // Add due today items
      if (dueToday.length > 0) {
        let todayText = ':calendar: *DUE TODAY — ' + sheetName + '*\n';
        for (const item of dueToday) {
          const priorityEmoji = item.priority === 'Critical' ? ':red_circle:' :
                               item.priority === 'High' ? ':large_orange_circle:' : ':large_blue_circle:';
          todayText += priorityEmoji + ' ' + item.deliverable + ' — ' + item.owner + '\n';
        }
        blocks.push({
          type: 'section',
          text: { type: 'mrkdwn', text: todayText }
        });
      }

      // Add due this week items (summary only)
      if (dueThisWeek.length > 0) {
        let weekText = ':page_facing_up: *DUE THIS WEEK — ' + sheetName + ' (' + dueThisWeek.length + ' items)*\n';
        for (const item of dueThisWeek) {
          weekText += '• ' + item.deliverable + ' (' + item.daysOut + 'd) — ' + item.owner + '\n';
        }
        blocks.push({
          type: 'section',
          text: { type: 'mrkdwn', text: weekText }
        });
      }

    } catch (e) {
      Logger.log('Error processing sheet ' + sheetName + ': ' + e.toString());
    }
  }

  // Gate readiness summary
  blocks.push({ type: 'divider' });

  const gateCheck = checkGateReadiness(config, ss);
  blocks.push({
    type: 'section',
    text: {
      type: 'mrkdwn',
      text: ':white_check_mark: *GATE 1 READINESS:* ' + gateCheck.readyCount + '/' + gateCheck.totalCount + ' deliverables complete'
    }
  });

  // Footer
  blocks.push({
    type: 'context',
    elements: [{
      type: 'mrkdwn',
      text: 'Auto-generated by Negotiation Tracker • Updated daily at 9 AM CAT'
    }]
  });

  // Post to Slack
  const payload = { blocks: blocks };
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };

  try {
    UrlFetchApp.fetch(config.SLACK_WEBHOOK_URL, options);
    Logger.log('Standup posted successfully');
  } catch (e) {
    Logger.log('Slack post failed: ' + e.toString());
  }

  // Also update the tracker sheet with last sync time
  const tracker = ss.getSheetByName('Gate Tracker');
  if (tracker) {
    // Find the "Last Standup" cell or add one
    const lastRow = tracker.getLastRow();
    tracker.getRange(lastRow + 1, 1).setValue('Last Standup');
    tracker.getRange(lastRow + 1, 2).setValue(todayStr);
  }
}

// ============================================================
// OVERDUE ALERT — Triggered every 4 hours
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
        overdueItems.push({
          sheet: sheetName,
          deliverable: deliverable,
          owner: owner,
          daysOverdue: Math.abs(diffDays),
          priority: priority
        });
      }
    }
  }

  if (overdueItems.length === 0) return;

  // Sort by severity (Critical first, then by days overdue descending)
  overdueItems.sort((a, b) => {
    const priorityOrder = { 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return b.daysOverdue - a.daysOverdue;
  });

  let text = ':rotating_light: *OVERDUE DELIVERABLES — ACTION REQUIRED*\n\n';

  for (const item of overdueItems) {
    const priorityEmoji = item.priority === 'Critical' ? ':red_circle:' :
                         item.priority === 'High' ? ':large_orange_circle:' : ':large_blue_circle:';
    const slackId = config.TEAM_SLACK_IDS[item.owner] || item.owner;
    text += priorityEmoji + ' *' + item.sheet + '*: ' + item.deliverable +
            ' (+' + item.daysOverdue + 'd overdue) — Owner: ' + slackId + '\n';
  }

  text += '\n:x: Escalation: Please update status or blockers in the tracker immediately.';

  const payload = {
    blocks: [{
      type: 'section',
      text: { type: 'mrkdwn', text: text }
    }]
  };

  try {
    UrlFetchApp.fetch(config.SLACK_WEBHOOK_URL, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload)
    });
  } catch (e) {
    Logger.log('Overdue alert failed: ' + e.toString());
  }
}

// ============================================================
// GATE READINESS CHECK
// ============================================================

function checkGateReadiness(config, ss) {
  const today = new Date();

  // Gate 1 criteria: OI JDA signed + ZBS NDA signed + MinAg MoU signed
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
          details.push(':white_check_mark: ' + deliverable);
        } else {
          details.push(':x: ' + deliverable + ' — Status: ' + status);
        }
      }
    }
  }

  return { readyCount: readyCount, totalCount: totalCount, details: details };
}

// ============================================================
// NOTION INTEGRATION — Sync status back to Notion project
// ============================================================

/**
 * Sync tracker status to Notion database
 * Requires: Notion API key and Database ID
 */
function syncToNotion() {
  const config = getConfig();
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Notion configuration (UPDATE THESE)
  const NOTION_API_KEY = 'secret_YOUR_NOTION_API_KEY';
  const NOTION_DATABASE_ID = 'YOUR_DATABASE_ID';

  const sheets = [config.SHEETS.OI, config.SHEETS.ZBS, config.SHEETS.MINAG, config.SHEETS.WB];

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

      // Create Notion page
      const payload = {
        parent: { database_id: NOTION_DATABASE_ID },
        properties: {
          'Name': {
            title: [{ text: { content: deliverable } }]
          },
          'Status': {
            status: { name: notionStatus }
          },
          'Assignee': {
            people: [] // Map owner to Notion user ID
          },
          'Due Date': dueDate ? {
            date: { start: dueDate }
          } : {},
          'Priority': {
            select: { name: priority }
          },
          'Source': {
            select: { name: sheetName }
          },
          'Notes': {
            rich_text: [{ text: { content: notes } }]
          }
        }
      };

      try {
        UrlFetchApp.fetch('https://api.notion.com/v1/pages', {
          method: 'post',
          contentType: 'application/json',
          headers: {
            'Authorization': 'Bearer ' + NOTION_API_KEY,
            'Notion-Version': '2022-06-28'
          },
          payload: JSON.stringify(payload)
        });
      } catch (e) {
        Logger.log('Notion sync failed for ' + deliverable + ': ' + e.toString());
      }
    }
  }

  Logger.log('Notion sync complete');
}

// ============================================================
// SUMMARY REPORT — Weekly email to CEO
// ============================================================

function weeklySummaryReport() {
  const config = getConfig();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const today = new Date();

  let summary = 'CHICHEWA AI INITIATIVE — WEEKLY NEGOTIATION SUMMARY\n';
  summary += 'Week of ' + Utilities.formatDate(today, 'UTC', 'yyyy-MM-dd') + '\n\n';

  // Gate status
  const gateCheck = checkGateReadiness(config, ss);
  summary += 'GATE 1 STATUS: ' + gateCheck.readyCount + '/' + gateCheck.totalCount + ' criteria met\n';
  for (const detail of gateCheck.details) {
    summary += '  ' + detail.replace(/:white_check_mark:|:x:/g, '').trim() + '\n';
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
      const risk = riskData[i][1]; // Risk/Issue column
      const severity = riskData[i][3]; // Severity column
      const status = riskData[i][6]; // Status column

      if (status === 'Closed' || status === 'Resolved') continue;

      summary += '• [' + severity + '] ' + risk + ' — ' + status + '\n';
    }
  }

  // Send email
  MailApp.sendEmail({
    to: 'ceo@lightspeed.ai',
    subject: '[Chichewa AI] Weekly Negotiation Summary — ' + Utilities.formatDate(today, 'UTC', 'yyyy-MM-dd'),
    body: summary
  });

  Logger.log('Weekly summary sent');
}

// ============================================================
// TRIGGER SETUP — Run this once to install triggers
// ============================================================

function setupTriggers() {
  // Clear existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    ScriptApp.deleteTrigger(trigger);
  }

  // Daily standup at 7 AM UTC (9 AM CAT)
  ScriptApp.newTrigger('dailyStandup')
    .timeBased()
    .everyDays(1)
    .atHour(config.STANDUP_HOUR)
    .create();

  // Overdue alert every 4 hours
  ScriptApp.newTrigger('overdueAlert')
    .timeBased()
    .everyHours(4)
    .create();

  // Weekly summary report (Monday 8 AM UTC = 10 AM CAT)
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
}

// ============================================================
// UTILITY: Format date for display
// ============================================================

function formatDate(dateStr) {
  if (!dateStr || dateStr === '') return 'No date';
  const date = new Date(dateStr);
  return Utilities.formatDate(date, 'UTC', 'yyyy-MM-dd');
}

// ============================================================
// UTILITY: Get status color for conditional formatting
// ============================================================

function getStatusColor(status) {
  switch (status) {
    case 'Done': return '#00ff00';      // Green
    case 'In Progress': return '#ffff00'; // Yellow
    case 'Not Started': return '#ff6666'; // Red
    case 'Blocked': return '#ff0000';     // Dark Red
    case 'At Risk': return '#ff9900';     // Orange
    default: return '#ffffff';            // White
  }
}

// ============================================================
// MENU: Add custom menu to spreadsheet
// ============================================================

function onOpen() {
  const ui = SpreadsheetApp.getUi();

  ui.createMenu('🤖 Negotiation Tracker')
    .addItem('📊 Generate Daily Standup', 'dailyStandup')
    .addItem('🚨 Run Overdue Alert', 'overdueAlert')
    .addItem('📈 Generate Weekly Report', 'weeklySummaryReport')
    .addItem('🔄 Sync to Notion', 'syncToNotion')
    .addSeparator()
    .addItem('⚙️ Setup Triggers', 'setupTriggers')
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
