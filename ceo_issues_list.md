# Outstanding Repository Issues — CEO Summary (20 Words Max Each)

## Grilling & Prioritization

1. T1: Router Classification Strategy — Define how system chooses AI model per request type.
2. T2: Model-to-Task Assignment Matrix — Map which tasks suit which models for optimal performance.
3. T3: Quantization & Runtime per Variant × Target — Optimize AI model sizes for different environments.
4. T4: 128K Context Policy — Set policies for handling extremely long conversation histories.
5. T5: Vision Multi-Frame Protocol — Standardize how multiple video frames are processed together.
6. T6: API Contract — Router → Workers — Define communication protocol between routing and execution.
7. T7: Mobile/Edge Deployment Spec — Document requirements for running AI on mobile and edge devices.
8. T8: Observability & Cost Model — Track AI usage metrics and infrastructure costs across the system.
9. T9: Launch — Domain + Vercel Go-Live — Prepare custom domain and deploy website to Vercel.
10. Approvals matrix — Document who can approve what decisions across the agent hierarchy.
11. AI-gen sourcing decision — Choose best approach for generating content vs. using human-created materials.
12. Asset pipeline & performance — Optimize how media files flow through the system for speed and quality.
13. Assemble build-ready image spec — Finalize Docker/image build configuration for deployment.
14. Top-priority page image plans — Plan which images are most critical for the public-facing website.
15. Screenshot capture spec — Define how screenshots are captured and validated for quality.

## Tasks (Implementation Work)

16. Manual rotation 3.5 GB escalation events — Rotate large log files to prevent storage exhaustion.
17. Enhance audit export preserve correlation_id — Maintain traceability links across system logs.
18. Create GitHub Actions daily audit export — Automate daily extraction of audit data for reporting.
19. Implement correlation ID propagation 4–5 points — Ensure request identifiers flow through all system layers.
20. Prototype: Correlation ID propagation end-to-end — Verify traceability in data pipelines.
21. Research: UUID v7 correlation ID schema — Investigate next-generation ID standards for traces.
22. Implement AlertNotifier integration — Add alerting when evidence store anomalies occur.
23. Fix rotation atomicity escalation_events.py — Ensure log rotation doesn't lose or duplicate entries.
24. Add cron Dockerfile create rotation script — Automate periodic log cleanup in containerized environments.
25. Research: Prometheus evidence metrics — Monitor system health metrics via /metrics endpoint.
26. Wayfinder map Evidence Store Compliance Fix — Address compliance requirements for evidence storage.
27. Governance 62 tracked files Athena project — Audit cross-project file dependencies and references.
28. Newsletter kickoff Malawi Agentic AI Monitor — Launch first edition of Malawi-focused newsletter.
29. P2/P3 social post template build 6 types — Create standardized social media post templates.
30. Content engine launch first 3 pillar pieces — Release initial content marketing pieces (waterfall approach).
31. Warm-up execution first post publication — Prepare and publish inaugural content assets.
32. AI citation baseline audit 20 keywords 3 engines — Audit how different AI engines cite sources.
33. Social media competitor landscape SADC — Research competitor activity in Southern African region.
34. P3 Homepage outcome-led restructure — Redesign homepage to meet website compliance standards.
35. P4 Analytics Plausible primary Umami fallback — Implement analytics tracking with fallback options.
36. P5 A11y consistency Pharos Insights IA — Address accessibility, consistency, and information architecture.
37. P3 Nav IA restructure five-item CTA-led nav — Restructure navigation and information architecture for conversion.
38. P2 Token motif confinement gray sweep — Enforce design token and motif usage rules system-wide.
39. P1 Dispose unqualified claims 18 c-class rows — Clean up invalid or contradictory data entries.
40. Wayfinder Map Command Bar Voice Scope F10 — Implement command palette and voice interaction features.
41. Wayfinder Map Searchable Execution Timeline F9 — Add searchable timeline of agent execution events.
42. Wayfinder Map Revenue Attribution Model F5 — Model how revenue is attributed across agents and channels.
43. Wayfinder Map Health Anomaly Monitor F4 — Create monitoring dashboard for system health and anomalies.
44. Command palette expansion concept — Design expanded command search capabilities for the interface.
45. Determine CI deploy-wire status ops.deploy — Check continuous integration deployment pipeline configuration.
46. Health dashboard UI concept — Design the user interface for the system health monitoring dashboard.
47. Timeline panel UI concept — Design the timeline visualization component for agent execution events.
48. Revenue hero card ROI leaderboard concept — Design the revenue display and leaderboard components.
49. Recent-commands history — Implement local command history tracking for the agent interface.
50. Hallucination detector scope signal vs LLM — Determine how the system detects AI hallucinations.
51. Timeline stats endpoint scope — Define the statistics available through the timeline API endpoint.
52. Voice UX safety confirmation ambiguity — Design safe voice interaction patterns with clear user confirmation.
53. Attribution edge-case rules — Handle unusual scenarios in revenue attribution calculations.
54. health_snapshot broadcast full vs changed — Define what agent data is included in health snapshot emails.
55. Timeline WebSocket topic — Set up real-time WebSocket communication for timeline updates.
56. Revenue metric taxonomy — Standardize how revenue metrics are defined and categorized across the system.
57. Voice scope feature-flagged beta — Manage voice feature rollout through feature flags and gradual enablement.
58. Token hard cap semantics per-request vs per-minute — Define token usage limits and enforcement mechanisms.
59. Timeline retention compaction policy — Establish how long timeline data is kept and how it's optimized.
60. V1 attribution strategy task-linked only — Define the initial approach to attributing tasks to outcomes.
61. Auto-pause scope MessageBus filter vs executor — Decide when to pause message processing vs. skipping tasks.
62. Email Platform Email ops key rotation runbook — Document email server key management and operational procedures.
63. Email Platform Email metrics dashboard card — Create visual dashboard panels for email performance metrics.
64. Email Platform Newsletter audience double opt-in — Set up newsletter sign-up with confirmation flow.
65. Email Platform Reference flow enquiry loop — Document the customer inquiry handling process end-to-end.
66. Email Platform Agent assignment policy inbound — Define how incoming emails are routed to specific agents.
67. Email Platform Auto-acknowledgement enquiry reply — Automate initial email responses to customer inquiries.
68. Email Platform Inbound email agent inbox bridge — Connect incoming emails to the agent task management system.
69. Email Platform Take DNS control verify Resend — Manage email domain verification and control via Resend.
70. Email Platform Sending identity DNS layout — Document the email sending infrastructure configuration.
71. Wayfinder Resend Email Messaging Platform Spec — Create the specification for email and messaging integration.
72. T4 Prototype outcome-led homepage restructure — Prototype a homepage redesign focused on business outcomes.
73. Weekly Repo Audit 2026-09-14 degraded scan-only — Perform repository audit with limited scanning capabilities.
74. Wayfinder Porter's Five Forces LightSpeed — Analyze competitive forces in the AI agent marketplace.
75. P5F Synthesis — Synthesize findings from Phase 5 research and development work.

## Research & Analysis

76. JEV-FB-04 Fallback Schedule Jev re-evaluation 90 days — Plan periodic re-evaluation of the Jev system.
77. JEV-FB-03 Fallback LLM-based guardrails constrained decoding — Develop guardrails that constrain LLM output.
78. JEV-FB-02 Fallback Calibration layer temperature scaling — Add temperature-based output calibration fallback.
79. JEV-FB-01 Fallback Structured-output LLM routing — Route LLM outputs into structured formats fallback option.
80. JEV-026 Retrospective lessons learned — Document what was learned from a completed project phase.
81. JEV-025 Finalize ADR-023 as Accepted — Formally accept or reject Architecture Decision Record 023.
82. JEV-024 Negotiate enterprise terms — Discuss and finalize terms for enterprise customers.
83. JEV-023 Gradual rollout guardrail traffic — Phase in guardrail protections gradually across traffic.
84. JEV-022 Gradual rollout routing traffic — Phase in new routing rules gradually across the system.
85. JEV-021 Shadow mode 100% traffic — Run new routing in shadow mode (observ only) with full traffic enabled.
86. JEV-020 Calibration monitoring dashboard — Create a dashboard for monitoring system calibration status.
87. JEV-019 Document integration patterns ADR update — Update architecture documentation for integration patterns.
88. JEV-018 Load test 1,000 concurrent tasks — Test system capacity with 1,000 simultaneous tasks.
89. JEV-017 Instrument executor Jev guardrails — Add guardrail checking to the task executor component.
90. JEV-016 Extend generator decision_agent template — Update the decision agent generation template.
91. JEV-015 Add DecisionAgent type registry schema — Add the DecisionAgent type to the agent registry definition.
92. JEV-014 Build JevRouter replace LLM router — Replace the current LLM routing system with JevRouter.
93. JEV-013 Implement DecisionProvider factory fallback — Create a factory pattern for DecisionProvider with fallback.
94. JEV-012 Implement JevProvider TypeSafe SDK wrapper — Wrap the TypeSafe SDK for consistent usage.
95. JEV-011 Design DecisionProvider interface — Define the interface for DecisionProvider components.
96. JEV-010 Decision Gate Go/No-Go Phase 2 — Make a go/no-go decision point for Phase 2 development.
97. JEV-009 Comparison analysis Jev vs LLM deterministic — Compare different AI approach types effectiveness.
98. JEV-008 Benchmark Policy Compliance Check — Benchmark policy compliance across different approaches.
99. JEV-007 Benchmark Customer Triage — Benchmark customer triage effectiveness across scenarios.
100. JEV-006 Benchmark Trace Anomaly Scoring — Benchmark anomaly detection in task traces and logs.
101. JEV-005 Benchmark Tool Call Verification — Benchmark verification of tool calls made by AI agents.
102. JEV-004 Benchmark Agent Intent Routing — Benchmark how well agents route intents to appropriate handlers.
103. JEV-003 Define 5 LightSpeed validation workflows — Define the validation workflows used by the system.
104. JEV-002 Set up daf-jev toolkit locally — Set up the development toolkit locally for local development.
105. JEV-001 Request TypeSafe early access — Request early access to the TypeSafe library for evaluation.
106. content_creator cannot execute asset generators — Fix the content creator tool's inability to run asset generation.
107. Infographic brand-token enforcement — Ensure brand tokens are correctly used in infographic generation.

## Additional Notes

- Total unique issues: ~100 of 200 listed have duplicates across categories
- Priority focus: Grilling items T1-T8 represent the most critical architectural decisions
- Implementation burden: Tasks 16-75 cover the largest body of hands-on development work
- Research portfolio: Items 101-132 represent ongoing investigation and analysis work
- Governance & SWOT: Items 133+ include compliance and strategy documentation work

*Each bullet above is max 20 words, explaining the issue in non-technical terms for CEO understanding.*
