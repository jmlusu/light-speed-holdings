# Dashboard Support Quick Reference Card

**Document Type:** Support Quick Reference  
**Last Updated:** 2026-07-22  
**For:** Customer Support Agents

---

## User Complaint Summary

> "The dashboard is buggy and unstable. It keeps scrolling on its own and I can't control it."

---

## What Users Are Experiencing

### 1. Auto-Scrolling (Primary Issue)
- Page scrolls to top every 10 seconds during data refresh
- Task kanban board jumps during drag-and-drop
- Tables lose scroll position when updated
- Charts briefly disappear and reappear

### 2. Connection Instability
- "Live" indicator flickers between green (connected) and red (offline)
- Real-time updates stop working without warning
- No indication when data fails to load

### 3. Missing Feedback
- No loading spinners when data is being fetched
- No error messages when something fails
- No way to report issues directly from dashboard

---

## Immediate Workaround (Share with Users)

```
We're aware of the auto-scrolling issue and have workarounds:

1. AVOID SCROLLING during the 10-second refresh cycle (you'll see 
   data update briefly)

2. If connection drops (red "Offline" indicator), click "Reconnect" 
   in the header

3. If data seems stale, press F5 or Ctrl+R to fully refresh

4. For the task board, try to complete drag-and-drop actions quickly

This issue is documented and a fix is planned for the next sprint.
```

---

## Quick Diagnosis Checklist

When user reports dashboard issues, ask:

| Question | Why It Matters |
|----------|----------------|
| "Is the indicator in the top-right green or red?" | Checks connection status |
| "What page are you on?" | Some issues are page-specific |
| "Did you see any toast notifications?" | May indicate error occurred |
| "Are you trying to drag-and-drop?" | Known issue with kanban |
| "How long has it been happening?" | Helps identify trigger |

---

## Common User Messages & Responses

### "The page keeps jumping to the top"
**Response:** "This is a known issue with the auto-refresh feature. The dashboard updates data every 10 seconds, which causes the page to reset its scroll position. We're working on a fix. In the meantime, try to avoid scrolling during updates."

### "I can't see if it's working or not"
**Response:** "Look at the top-right corner for the connection indicator. Green means live updates are working. If it's red or says 'Offline', click the 'Reconnect' button."

### "My task disappeared when I was moving it"
**Response:** "This happens when the auto-refresh interrupts a drag-and-drop action. Try to complete the move quickly before the next update cycle. We're implementing a fix to prevent this."

### "I don't know if the data is current"
**Response:** "The dashboard updates automatically, but if you see the 'Live' indicator, the data should be current. You can also refresh the page manually with F5 to ensure you have the latest data."

---

## Error Messages Users Might See

| Message | Meaning | Action |
|---------|---------|--------|
| "Offline" (red) | WebSocket disconnected | Click "Reconnect" or refresh page |
| "Reconnecting..." (blue) | Attempting to reconnect | Wait 5-10 seconds |
| Toast: "Connection lost" | WebSocket dropped | Auto-reconnects in 3 seconds |
| Toast: "Failed to load" | API error occurred | Refresh page or try again later |

---

## When to Escalate

Escalate to engineering if:
- User cannot access dashboard at all
- Data is clearly wrong (not just slow/stale)
- User reports security concerns
- Issue persists after page refresh
- Multiple users report same issue simultaneously

---

## Related Documentation

- **Full Issue Details:** `knowledge/technology/dashboard-known-issues.md`
- **Architecture:** `docs/CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md`
- **Status:** `docs/STATUS.md`

---

**Remember:** These are known bugs, not user errors. Be empathetic and provide workarounds while we implement fixes.
