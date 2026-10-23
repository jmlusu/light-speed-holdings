import { Plugin } from "@opencode/plugin"

interface RuleViolation {
  ruleId: string
  severity: "error" | "warn" | "info"
  message: string
  tool?: string
  context?: Record<string, unknown>
}

const CONSTITUTION_PATH = ".ai-company/constitution"
const HARNESS_CHANGES_PATH = "harness/changes"
const EVIDENCE_DIRS = [
  "reports/evidence/",
  "audit/",
  ".opencode/audit/",
  "harness/changes/*/reviews/",
  "data/orchestrator/escalation_events.jsonl",
  "data/orchestrator/dead_letter.jsonl",
]

function checkPathPatterns(filePath: string, patterns: string[]): boolean {
  const normalized = filePath.replace(/\\/g, "/")
  return patterns.some(p => {
    const regex = p.replace(/\*\*/g, ".*").replace(/\*/g, "[^/]*")
    return new RegExp(`^${regex}$`).test(normalized)
  })
}

export default Plugin.define({
  id: "ls-harness-enforcer",
  async setup(ctx) {
    const storage = ctx.storage
    let isAuditing = false
    let auditEvidenceDir = ""

    return {
      "tool.execute.before": async (input, output) => {
        const { tool, args } = input
        const filePath = args?.path || args?.pattern || ""

        // 1. Constitution guards - block edits without process
        if (["edit", "write", "bash"].includes(tool) && filePath) {
          if (checkPathPatterns(filePath, [`${CONSTITUTION_PATH}/**`])) {
            // Allow reads, but block writes without ADR reference
            if (["edit", "write"].includes(tool)) {
              const violation: RuleViolation = {
                ruleId: "constitution-guard",
                severity: "error",
                message: `Constitution files are protected. Edits require ADR process. See AGENTS.md §Governance.`,
                tool,
                context: { path: filePath },
              }
              await ctx.client.app.log({
                body: { service: "ls-harness-enforcer", level: "error", message: `[${violation.ruleId}] ${violation.message}` },
              })
              throw new Error(`🚫 ${violation.message}`)
            }
          }
        }

        // 2. ECL active change context - require check before task docs
        if (["read", "edit", "write"].includes(tool) && filePath) {
          const isTaskDoc = filePath.includes("docs/") || filePath.includes("SPEC.md") || filePath.includes("spec/")
          if (isTaskDoc) {
            try {
              const summaryResult = await ctx.client.file.read({ path: `${HARNESS_CHANGES_PATH}/active/summary.md` })
              if (!summaryResult.content || !summaryResult.content.includes("active")) {
                const violation: RuleViolation = {
                  ruleId: "ecl-active-change-required",
                  severity: "warn",
                  message: "No active ECL change found. Read harness/changes/active/summary.md before working on task docs. See AGENTS.md §3.2.",
                  tool,
                  context: { path: filePath },
                }
                await ctx.client.app.log({
                  body: { service: "ls-harness-enforcer", level: "warn", message: `[${violation.ruleId}] ${violation.message}` },
                })
              }
            } catch {
              // No active change - warn but don't block
            }
          }
        }

        // 3. Audit evidence separation - block writes to evidence dirs during audit
        if (["edit", "write", "bash"].includes(tool) && filePath) {
          const isEvidenceDir = EVIDENCE_DIRS.some(dir => checkPathPatterns(filePath, [dir]))
          if (isEvidenceDir && isAuditing) {
            const violation: RuleViolation = {
              ruleId: "audit-evidence-separation",
              severity: "error",
              message: `AUDIT VIOLATION: Cannot write to evidence directory "${filePath}" during audit. Auditor read/write sets must be disjoint. See AGENTS.md §9.3.`,
              tool,
              context: { path: filePath },
            }
            await ctx.client.app.log({
              body: { service: "ls-harness-enforcer", level: "error", message: `[${violation.ruleId}] ${violation.message}` },
            })
            throw new Error(`🚫 ${violation.message}`)
          }
        }

        // 4. ECL lint check before commit (via bash git commit)
        if (tool === "bash" && args?.command?.includes("git commit")) {
          // Just log reminder - actual enforcement via pre-commit hooks
          await ctx.client.app.log({
            body: { service: "ls-harness-enforcer", level: "info", message: "Reminder: Run 'pwsh scripts/maintenance/lint-ecl.ps1' before commit. See AGENTS.md §5." },
          })
        }

        return output
      },

      "tool.execute.after": async (input, output) => {
        const { tool, args } = input

        // Track audit mode when reading evidence dirs
        if (tool === "read" && args?.path) {
          const isEvidenceRead = EVIDENCE_DIRS.some(dir => checkPathPatterns(args.path, [dir]))
          if (isEvidenceRead) {
            isAuditing = true
            auditEvidenceDir = args.path
          }
        }

        // Track when audit completes (reading audit output)
        if (tool === "read" && args?.path?.includes("reports/repo-audit-")) {
          isAuditing = false
          auditEvidenceDir = ""
        }

        return output
      },

      "session.created": async () => {
        await ctx.client.app.log({
          body: { service: "ls-harness-enforcer", level: "info", message: "📋 LightSpeed Harness Enforcer initialized (ECL, Constitution, Audit guards)." },
        })
      },
    }
  },
})
