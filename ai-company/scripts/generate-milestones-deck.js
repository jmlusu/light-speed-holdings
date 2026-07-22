#!/usr/bin/env node
/**
 * Generate AI Company Builder Milestones Deck
 * Uses pptxgenjs to create a professional PowerPoint presentation
 */

const pptxgen = require("pptxgenjs");

// Color palette - Professional theme
const COLORS = {
  darkBlue: "1a1a2e",
  teal: "16213e",
  accent: "0f3460",
  highlight: "e94560",
  white: "ffffff",
  lightGray: "f8f9fa",
  mediumGray: "6c757d",
  darkGray: "343a40",
  success: "28a745",
  warning: "ffc107",
  info: "17a2b8"
};

// Create presentation
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'AI Company Builder';
pres.title = 'AI Company Builder - Major Milestones';

// Helper function to create consistent slide backgrounds
function setSlideBackground(slide, color = COLORS.white) {
  slide.background = { color: color };
}

// Helper function to add consistent header
function addSlideHeader(slide, title, subtitle = null) {
  // Header bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.8,
    fill: { color: COLORS.darkBlue }
  });
  
  // Title
  slide.addText(title, {
    x: 0.5, y: 0.15, w: 9, h: 0.5,
    fontSize: 24, fontFace: "Arial",
    color: COLORS.white, bold: true, margin: 0
  });
  
  // Subtitle if provided
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.5, y: 0.5, w: 9, h: 0.25,
      fontSize: 12, fontFace: "Arial",
      color: COLORS.white, italic: true, margin: 0
    });
  }
}

// Helper function for metric cards
function addMetricCard(slide, x, y, value, label, color = COLORS.accent) {
  // Card background
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 2.2, h: 1.2,
    fill: { color: COLORS.white },
    shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 }
  });
  
  // Color accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 0.08, h: 1.2,
    fill: { color: color }
  });
  
  // Value
  slide.addText(value, {
    x: x + 0.2, y: y + 0.1, w: 1.8, h: 0.6,
    fontSize: 24, fontFace: "Arial",
    color: color, bold: true, margin: 0
  });
  
  // Label
  slide.addText(label, {
    x: x + 0.2, y: y + 0.7, w: 1.8, h: 0.4,
    fontSize: 10, fontFace: "Arial",
    color: COLORS.mediumGray, margin: 0
  });
}

// Slide 1: Title Slide
let titleSlide = pres.addSlide();
setSlideBackground(titleSlide, COLORS.darkBlue);

// Decorative shape
titleSlide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 4.5, w: 10, h: 1.125,
  fill: { color: COLORS.teal, transparency: 70 }
});

// Title
titleSlide.addText("AI Company Builder", {
  x: 0.5, y: 1.5, w: 9, h: 1.0,
  fontSize: 44, fontFace: "Arial",
  color: COLORS.white, bold: true, margin: 0
});

// Subtitle
titleSlide.addText("Major Milestones", {
  x: 0.5, y: 2.5, w: 9, h: 0.6,
  fontSize: 28, fontFace: "Arial",
  color: COLORS.white, margin: 0
});

// Version info
titleSlide.addText("v0.3.0 | 1205 Tests | 26 CLI Commands | 53 Agent Roles", {
  x: 0.5, y: 3.2, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.white, italic: true, margin: 0
});

// Date
titleSlide.addText("July 2026", {
  x: 0.5, y: 4.8, w: 9, h: 0.3,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.white, margin: 0
});

// Slide 2: Executive Summary
let summarySlide = pres.addSlide();
setSlideBackground(summarySlide, COLORS.white);
addSlideHeader(summarySlide, "Executive Summary", "Key Project Statistics");

// Metric cards
addMetricCard(summarySlide, 0.5, 1.2, "1205", "Tests Passing", COLORS.success);
addMetricCard(summarySlide, 2.9, 1.2, "26", "CLI Commands", COLORS.info);
addMetricCard(summarySlide, 5.3, 1.2, "53", "Agent Roles", COLORS.highlight);
addMetricCard(summarySlide, 7.7, 1.2, "0", "Lint Errors", COLORS.success);

// Key achievements
summarySlide.addText([
  { text: "Project Overview", options: { bold: true, fontSize: 16, breakLine: true } },
  { text: "Python CLI tool for creating and orchestrating AI agent hierarchies", options: { breakLine: true } },
  { text: "Complete with 8 major milestones achieved in 3 sprints", options: { breakLine: true } },
  { text: "Production-ready with comprehensive testing and documentation", options: { breakLine: true } }
], {
  x: 0.5, y: 2.8, w: 9, h: 2.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 3: Project Timeline
let timelineSlide = pres.addSlide();
setSlideBackground(timelineSlide, COLORS.white);
addSlideHeader(timelineSlide, "Project Timeline", "8 Major Milestones Across 3 Sprints");

// Timeline line
timelineSlide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 2.5, w: 9, h: 0.02,
  fill: { color: COLORS.accent }
});

// Timeline milestones
const milestones = [
  { x: 0.5, label: "Foundation", date: "Pre-Sprint 1" },
  { x: 1.7, label: "Sprint 1", date: "Jul 20" },
  { x: 2.9, label: "Sprint 2", date: "Jul 21" },
  { x: 4.1, label: "Org Expansion", date: "Jul 21" },
  { x: 5.3, label: "Sprint 3", date: "Jul 22" },
  { x: 6.5, label: "Dashboard", date: "Jul 22" },
  { x: 7.7, label: "CLI & DX", date: "Jul 22" },
  { x: 8.9, label: "Documentation", date: "Jul 22" }
];

milestones.forEach((milestone, index) => {
  // Milestone dot
  timelineSlide.addShape(pres.shapes.OVAL, {
    x: milestone.x, y: 2.4, w: 0.2, h: 0.2,
    fill: { color: index % 2 === 0 ? COLORS.accent : COLORS.highlight }
  });
  
  // Label
  timelineSlide.addText(milestone.label, {
    x: milestone.x - 0.5, y: 2.7, w: 1.2, h: 0.3,
    fontSize: 8, fontFace: "Arial",
    color: COLORS.darkGray, align: "center", margin: 0
  });
  
  // Date
  timelineSlide.addText(milestone.date, {
    x: milestone.x - 0.5, y: 3.0, w: 1.2, h: 0.2,
    fontSize: 7, fontFace: "Arial",
    color: COLORS.mediumGray, align: "center", margin: 0
  });
});

// Slide 4: Milestone 1 - Foundation
let milestone1Slide = pres.addSlide();
setSlideBackground(milestone1Slide, COLORS.white);
addSlideHeader(milestone1Slide, "Milestone 1: Foundation", "Pre-Sprint 1 - Core Architecture");

// Two-column layout
// Left column: Architecture
milestone1Slide.addText([
  { text: "Core Architecture", options: { bold: true, fontSize: 16, breakLine: true } },
  { text: "Core Python package structure with Typer CLI", options: { bullet: true, breakLine: true } },
  { text: "17+ Pydantic domain models", options: { bullet: true, breakLine: true } },
  { text: "Company, Executive, Department, Agent, Workflow, Task, etc.", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.2, w: 4.3, h: 2.0,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Right column: Registry System
milestone1Slide.addText([
  { text: "Registry System", options: { bold: true, fontSize: 16, breakLine: true } },
  { text: "4-module registry system", options: { bullet: true, breakLine: true } },
  { text: "Loader, Parser, Resolver, Validator", options: { bullet: true, breakLine: true } },
  { text: "Loading 19 YAML configurations", options: { bullet: true, breakLine: true } }
], {
  x: 5.2, y: 1.2, w: 4.3, h: 2.0,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Bottom: Templates
milestone1Slide.addText([
  { text: "Template System", options: { bold: true, fontSize: 16, breakLine: true } },
  { text: "12 Jinja2 templates for agent generation", options: { bullet: true, breakLine: true } },
  { text: "Generator with template selection by agent type", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 3.5, w: 9, h: 1.5,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 5: Milestone 2 - Sprint 1
let milestone2Slide = pres.addSlide();
setSlideBackground(milestone2Slide, COLORS.white);
addSlideHeader(milestone2Slide, "Milestone 2: Sprint 1", "Code Hardening & Audit Trail - Completed July 20");

// Key achievements
milestone2Slide.addText([
  { text: "Sprint 1 Achievements", options: { bold: true, fontSize: 16, breakLine: true } },
  { text: "Audit trail system (AuditEvent, AuditWriter, AuditReader)", options: { bullet: true, breakLine: true } },
  { text: "Executor integration with audit logging", options: { bullet: true, breakLine: true } },
  { text: "Code hardening across all modules", options: { bullet: true, breakLine: true } },
  { text: "All Track B and Track C items completed", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.2, w: 9, h: 3.0,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Status indicator
milestone2Slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.5, w: 2.0, h: 0.5,
  fill: { color: COLORS.success }
});

milestone2Slide.addText("COMPLETED", {
  x: 0.5, y: 4.5, w: 2.0, h: 0.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.white, bold: true, align: "center", valign: "middle", margin: 0
});

// Slide 6: Milestone 3 - Sprint 2
let milestone3Slide = pres.addSlide();
setSlideBackground(milestone3Slide, COLORS.white);
addSlideHeader(milestone3Slide, "Milestone 3: Sprint 2", "Core Engines & Integration - Completed July 21");

// Key metrics
milestone3Slide.addText("13 items completed | 41 hours estimated effort", {
  x: 0.5, y: 1.2, w: 9, h: 0.3,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.accent, bold: true, margin: 0
});

// Core engines in two columns
milestone3Slide.addText([
  { text: "Core Engines", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Executor pipeline: Inbox polling → AgentLoop (ReAct) → LLM → Tools → Audit", options: { bullet: true, breakLine: true } },
  { text: "DecisionEngine: Approval matrix, risk assessment, decision tree navigation", options: { bullet: true, breakLine: true } },
  { text: "WorkflowEngine: 9 workflow definitions, step tracking, SLA monitoring", options: { bullet: true, breakLine: true } },
  { text: "MemoryEngine: 6 memory types with persistence and executor integration", options: { bullet: true, breakLine: true } },
  { text: "GraphEngine: 4 graph types with BFS pathfinding", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.6, w: 4.3, h: 3.0,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

milestone3Slide.addText([
  { text: "Additional Features", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Circuit Breaker, Cost Tracker, Dead-Letter Queue", options: { bullet: true, breakLine: true } },
  { text: "Postmortem system for incident tracking", options: { bullet: true, breakLine: true } },
  { text: "BootstrapEngine: Full company generation from registry", options: { bullet: true, breakLine: true } },
  { text: "1093 tests passing, 0 ruff/mypy errors", options: { bullet: true, breakLine: true } }
], {
  x: 5.2, y: 1.6, w: 4.3, h: 3.0,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 7: Milestone 4 - Organization Expansion
let milestone4Slide = pres.addSlide();
setSlideBackground(milestone4Slide, COLORS.white);
addSlideHeader(milestone4Slide, "Milestone 4: Organization Expansion", "July 21 - 53 New Roles Added");

// Key metrics
milestone4Slide.addText("53 new roles added across all departments", {
  x: 0.5, y: 1.2, w: 9, h: 0.3,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.accent, bold: true, margin: 0
});

// Expansion details
milestone4Slide.addText([
  { text: "4-Phase Expansion Plan", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Immediate → Weeks 1-8 → Weeks 9-16 → Weeks 17-24", options: { bullet: true, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "Structural Improvements", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "CTO span reduced for better management", options: { bullet: true, breakLine: true } },
  { text: "Product department created", options: { bullet: true, breakLine: true } },
  { text: "Strategy department created", options: { bullet: true, breakLine: true } },
  { text: "AI Safety hierarchy established", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.6, w: 9, h: 3.5,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 8: Milestone 5 - Sprint 3
let milestone5Slide = pres.addSlide();
setSlideBackground(milestone5Slide, COLORS.white);
addSlideHeader(milestone5Slide, "Milestone 5: Sprint 3", "Gap Closure & Testing - Completed July 22");

// Key metrics
milestone5Slide.addText("8 items completed | 22 hours estimated effort", {
  x: 0.5, y: 1.2, w: 9, h: 0.3,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.accent, bold: true, margin: 0
});

// Key achievements in two columns
milestone5Slide.addText([
  { text: "Testing Improvements", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Org chart test rewrite (832 lines → 56 tests, all passing)", options: { bullet: true, breakLine: true } },
  { text: "DataTransformer frozen model bug fix", options: { bullet: true, breakLine: true } },
  { text: "E2E pipeline test", options: { bullet: true, breakLine: true } },
  { text: "WebSocket integration tests (30 tests)", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.6, w: 4.3, h: 2.5,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

milestone5Slide.addText([
  { text: "CLI Enhancements", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Governance CLI (7 commands, 9 tests)", options: { bullet: true, breakLine: true } },
  { text: "Memory CLI enhancement (stats/search/recall)", options: { bullet: true, breakLine: true } },
  { text: "Dashboard API tests (9 tests)", options: { bullet: true, breakLine: true } },
  { text: "v0.3.0 release tagged", options: { bullet: true, breakLine: true } }
], {
  x: 5.2, y: 1.6, w: 4.3, h: 2.5,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Final test count
milestone5Slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.3, w: 9, h: 0.5,
  fill: { color: COLORS.success }
});

milestone5Slide.addText("1205 Tests Passing | 0 Failures | 0 Ruff Errors | 0 Mypy Errors", {
  x: 0.5, y: 4.3, w: 9, h: 0.5,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.white, bold: true, align: "center", valign: "middle", margin: 0
});

// Slide 9: Milestone 6 - Dashboard & Monitoring
let milestone6Slide = pres.addSlide();
setSlideBackground(milestone6Slide, COLORS.white);
addSlideHeader(milestone6Slide, "Milestone 6: Dashboard & Monitoring", "Real-time Visibility & Analytics");

// Dashboard features in two columns
milestone6Slide.addText([
  { text: "FastAPI Dashboard", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "FastAPI dashboard with CORS and API key auth", options: { bullet: true, breakLine: true } },
  { text: "WebSocket broadcast for real-time updates", options: { bullet: true, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "7-Department KPI System", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Engineering, HR, Finance, Legal, Marketing, Sales, Customer Success", options: { bullet: true, breakLine: true } },
  { text: "28 KPI definitions with collectors", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.2, w: 4.3, h: 3.5,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

milestone6Slide.addText([
  { text: "Analytics System", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "History tracking, trend analysis, alert rules", options: { bullet: true, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "CEO Dashboard", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Company health overview", options: { bullet: true, breakLine: true } },
  { text: "Agent performance metrics", options: { bullet: true, breakLine: true } },
  { text: "Cost tracking and optimization", options: { bullet: true, breakLine: true } },
  { text: "Task pipeline visualization", options: { bullet: true, breakLine: true } }
], {
  x: 5.2, y: 1.2, w: 4.3, h: 3.5,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 10: Milestone 7 - CLI & DX
let milestone7Slide = pres.addSlide();
setSlideBackground(milestone7Slide, COLORS.white);
addSlideHeader(milestone7Slide, "Milestone 7: CLI & Developer Experience", "26 Commands for Complete Control");

// CLI commands in a grid layout
const cliCommands = [
  "company", "decision", "graph", "workflows", "memory", "agents",
  "board", "departments", "executives", "specialists", "orchestrator", "models",
  "dashboard", "executor", "doctor", "marketing", "sales", "customer-success",
  "legal", "hr", "generate", "status", "sop", "raci", "governance", ""
];

// Create command grid
cliCommands.forEach((cmd, index) => {
  if (cmd) {
    const row = Math.floor(index / 6);
    const col = index % 6;
    const x = 0.5 + col * 1.5;
    const y = 1.5 + row * 0.6;
    
    milestone7Slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: 1.3, h: 0.4,
      fill: { color: COLORS.lightGray }
    });
    
    milestone7Slide.addText(cmd, {
      x: x, y: y, w: 1.3, h: 0.4,
      fontSize: 8, fontFace: "Arial",
      color: COLORS.darkGray, align: "center", valign: "middle", margin: 0
    });
  }
});

// Developer experience
milestone7Slide.addText([
  { text: "Developer Experience", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "System diagnostics (doctor command)", options: { bullet: true, breakLine: true } },
  { text: "Pre-commit hooks (ruff, mypy, bandit)", options: { bullet: true, breakLine: true } },
  { text: "Comprehensive help system for all commands", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 4.0, w: 9, h: 1.5,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 11: Milestone 8 - Documentation & Governance
let milestone8Slide = pres.addSlide();
setSlideBackground(milestone8Slide, COLORS.white);
addSlideHeader(milestone8Slide, "Milestone 8: Documentation & Governance", "30+ Documentation Files");

// Documentation categories in two columns
milestone8Slide.addText([
  { text: "Technical Documentation", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Architecture docs, developer guide", options: { bullet: true, breakLine: true } },
  { text: "ECL (change lifecycle)", options: { bullet: true, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "Standard Operating Procedures", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "Incident response, deployment", options: { bullet: true, breakLine: true } },
  { text: "HR onboarding, budget approval", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.2, w: 4.3, h: 3.0,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

milestone8Slide.addText([
  { text: "Governance Framework", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "RACI matrices: Hiring, escalation, deployment workflows", options: { bullet: true, breakLine: true } },
  { text: "Risk register (14 items with mitigations)", options: { bullet: true, breakLine: true } },
  { text: "Board governance charter", options: { bullet: true, breakLine: true } },
  { text: "Model routing policy", options: { bullet: true, breakLine: true } }
], {
  x: 5.2, y: 1.2, w: 4.3, h: 3.0,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 12: Quality Metrics
let qualitySlide = pres.addSlide();
setSlideBackground(qualitySlide, COLORS.white);
addSlideHeader(qualitySlide, "Quality Metrics", "Production-Ready Standards");

// Quality metrics table
const qualityData = [
  [
    { text: "Metric", options: { bold: true, fill: { color: COLORS.darkBlue }, color: COLORS.white } },
    { text: "Value", options: { bold: true, fill: { color: COLORS.darkBlue }, color: COLORS.white } },
    { text: "Status", options: { bold: true, fill: { color: COLORS.darkBlue }, color: COLORS.white } }
  ],
  [
    { text: "Tests Passing", options: { fill: { color: COLORS.lightGray } } },
    { text: "1205", options: { fill: { color: COLORS.lightGray } } },
    { text: "✓ PASS", options: { fill: { color: COLORS.lightGray }, color: COLORS.success } }
  ],
  [
    { text: "Ruff Lint Errors", options: { fill: { color: COLORS.white } } },
    { text: "0", options: { fill: { color: COLORS.white } } },
    { text: "✓ CLEAN", options: { fill: { color: COLORS.white }, color: COLORS.success } }
  ],
  [
    { text: "Mypy Type Errors", options: { fill: { color: COLORS.lightGray } } },
    { text: "0", options: { fill: { color: COLORS.lightGray } } },
    { text: "✓ CLEAN", options: { fill: { color: COLORS.lightGray }, color: COLORS.success } }
  ],
  [
    { text: "CLI Commands", options: { fill: { color: COLORS.white } } },
    { text: "26", options: { fill: { color: COLORS.white } } },
    { text: "✓ COMPLETE", options: { fill: { color: COLORS.white }, color: COLORS.success } }
  ],
  [
    { text: "Agent Roles", options: { fill: { color: COLORS.lightGray } } },
    { text: "53", options: { fill: { color: COLORS.lightGray } } },
    { text: "✓ DEPLOYED", options: { fill: { color: COLORS.lightGray }, color: COLORS.success } }
  ]
];

qualitySlide.addTable(qualityData, {
  x: 0.5, y: 1.2, w: 9, h: 3.0,
  border: { pt: 1, color: COLORS.mediumGray },
  colW: [3, 2, 4]
});

// Slide 13: Architecture Overview
let archSlide = pres.addSlide();
setSlideBackground(archSlide, COLORS.white);
addSlideHeader(archSlide, "Architecture Overview", "Module Hierarchy & Data Flow");

// Architecture diagram (text-based)
archSlide.addText([
  { text: "Module Hierarchy", options: { bold: true, fontSize: 14, breakLine: true } },
  { text: "ai-company/", options: { breakLine: true } },
  { text: "├── src/ai_company/          # Core package", options: { breakLine: true } },
  { text: "│   ├── cli/                 # Typer CLI (26 commands)", options: { breakLine: true } },
  { text: "│   ├── models/              # Pydantic models (17+)", options: { breakLine: true } },
  { text: "│   ├── registry/            # 4-module registry system", options: { breakLine: true } },
  { text: "│   ├── generator/           # Jinja2 template engine", options: { breakLine: true } },
  { text: "│   ├── orchestrator/        # Task orchestration", options: { breakLine: true } },
  { text: "│   ├── engines/             # Core engines (5)", options: { breakLine: true } },
  { text: "│   ├── dashboard/           # FastAPI dashboard", options: { breakLine: true } },
  { text: "│   └── governance/          # Governance framework", options: { breakLine: true } },
  { text: "├── templates/               # 12 Jinja2 templates", options: { breakLine: true } },
  { text: "├── company/                 # Generated company configs", options: { breakLine: true } },
  { text: "├── tests/                   # 1205 tests", options: { breakLine: true } },
  { text: "└── docs/                    # 30+ documentation files", options: { breakLine: true } }
], {
  x: 0.5, y: 1.2, w: 9, h: 4.0,
  fontSize: 10, fontFace: "Consolas",
  color: COLORS.darkGray, margin: 0
});

// Slide 14: Remaining Work
let remainingSlide = pres.addSlide();
setSlideBackground(remainingSlide, COLORS.white);
addSlideHeader(remainingSlide, "Remaining Work", "Sprint 4 Items");

// Remaining work items
remainingSlide.addText([
  { text: "Sprint 4 Planned Items", options: { bold: true, fontSize: 16, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "Performance optimization and load testing", options: { bullet: true, breakLine: true } },
  { text: "Advanced analytics and reporting", options: { bullet: true, breakLine: true } },
  { text: "Mobile dashboard application", options: { bullet: true, breakLine: true } },
  { text: "Integration with external AI services", options: { bullet: true, breakLine: true } },
  { text: "Advanced workflow automation", options: { bullet: true, breakLine: true } },
  { text: "Enterprise security features", options: { bullet: true, breakLine: true } },
  { text: "Multi-tenant support", options: { bullet: true, breakLine: true } },
  { text: "API rate limiting and quota management", options: { bullet: true, breakLine: true } }
], {
  x: 0.5, y: 1.2, w: 9, h: 4.0,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.darkGray, margin: 0
});

// Slide 15: Next Steps
let nextStepsSlide = pres.addSlide();
setSlideBackground(nextStepsSlide, COLORS.darkBlue);

// Title
nextStepsSlide.addText("Next Steps", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 32, fontFace: "Arial",
  color: COLORS.white, bold: true, margin: 0
});

// Recommendations
nextStepsSlide.addText([
  { text: "Recommendations", options: { bold: true, fontSize: 18, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "1. Begin Sprint 4 with performance optimization", options: { breakLine: true } },
  { text: "2. Expand dashboard with advanced analytics", options: { breakLine: true } },
  { text: "3. Implement mobile-responsive design", options: { breakLine: true } },
  { text: "4. Add integration with external AI services", options: { breakLine: true } },
  { text: "5. Enhance security and compliance features", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "Project is production-ready and fully functional", options: { italic: true, breakLine: true } },
  { text: "All major milestones achieved with high quality standards", options: { italic: true, breakLine: true } }
], {
  x: 0.5, y: 1.5, w: 9, h: 3.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.white, margin: 0
});

// Footer
nextStepsSlide.addText("AI Company Builder v0.3.0 | Built with Python, FastAPI, and Modern DevOps", {
  x: 0.5, y: 5.0, w: 9, h: 0.3,
  fontSize: 10, fontFace: "Arial",
  color: COLORS.white, italic: true, margin: 0
});

// Write the file
pres.writeFile({ fileName: "C:\\Users\\jmlus\\light-speed-holdings\\ai-company\\docs\\milestones-deck.pptx" })
  .then(() => {
    console.log("✅ Presentation created successfully!");
    console.log("📁 File: docs/milestones-deck.pptx");
  })
  .catch(err => {
    console.error("❌ Error creating presentation:", err);
  });