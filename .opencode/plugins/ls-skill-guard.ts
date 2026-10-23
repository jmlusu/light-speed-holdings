import { Plugin } from "@opencode/plugin"

interface RuleViolation {
  ruleId: string
  severity: "error" | "warn" | "info"
  message: string
  tool?: string
  context?: Record<string, unknown>
}

const RETIRED_SKILLS = [
  "claude-mem-",
  "scroll-craft",
  "greploop",
]

const APPROVED_VENDORS_PATH = "docs/APPROVED-VENDORS.md"

export default Plugin.define({
  id: "ls-skill-guard",
  async setup(ctx) {
    let approvedVendors: string[] = []
    let skillsLockChecked = false

    // Load approved vendors list
    async function loadApprovedVendors() {
      try {
        const result = await ctx.client.file.read({ path: APPROVED_VENDORS_PATH })
        if (result.content) {
          // Extract vendor names from the file (simple extraction)
          approvedVendors = result.content
            .split("\n")
            .filter(line => line.trim() && !line.startsWith("#"))
            .map(line => line.split("|")[1]?.trim() || line.trim())
            .filter(v => v.length > 0)
        }
      } catch {
        approvedVendors = []
      }
    }

    return {
      "tool.execute.before": async (input, output) => {
        const { tool, args } = input

        // 1. Subagent vs Skill namespace validation
        if (tool === "task" && args?.subagent_type) {
          const subagentType = args.subagent_type

          // Check if it's a skill name being used as subagent_type
          const isSkillName = subagentType.includes("-") && (
            subagentType.startsWith("ls-") ||
            subagentType.startsWith("hyperframes-") ||
            subagentType.startsWith("k-dense-") ||
            subagentType.startsWith("ecl-") ||
            subagentType.endsWith("-engineer") ||
            subagentType.endsWith("-lead") ||
            subagentType.endsWith("-owner") ||
            subagentType.endsWith("-director") ||
            subagentType.endsWith("-manager")
          )

          if (isSkillName) {
            const violation: RuleViolation = {
              ruleId: "subagent-skill-namespace-violation",
              severity: "error",
              message: `"${subagentType}" appears to be a skill name, not a valid subagent_type. Subagents and skills are separate namespaces. See AGENTS.md §14 "Dispatch guardrails".`,
              tool,
              context: { subagentType },
            }
            await ctx.client.app.log({
              body: { service: "ls-skill-guard", level: "error", message: `[${violation.ruleId}] ${violation.message}` },
            })
            throw new Error(`🚫 ${violation.message}`)
          }
        }

        // 2. Skill installation hygiene - check skills-lock.json after npx skills
        if (tool === "bash" && args?.command?.includes("npx skills")) {
          if (!skillsLockChecked) {
            await ctx.client.app.log({
              body: { service: "ls-skill-guard", level: "warn", message: "After 'npx skills' install: run 'git status', revert unrequested skills, commit corrected skills-lock.json. See AGENTS.md §14 Skills CLI install hygiene." },
            })
            skillsLockChecked = true
          }
        }

        // 3. Retired skills blocking
        if (["read", "glob", "grep"].includes(tool) && args?.path) {
          const path = args.path
          for (const retired of RETIRED_SKILLS) {
            if (path.includes(retired)) {
              const violation: RuleViolation = {
                ruleId: "retired-skill-blocked",
                severity: "error",
                message: `Accessing retired skill: ${retired}. Retired 2026-09-23 per AGENTS.md §9.2. Skills deleted; local data purged.`,
                tool,
                context: { path, retiredSkill: retired },
              }
              await ctx.client.app.log({
                body: { service: "ls-skill-guard", level: "error", message: `[${violation.ruleId}] ${violation.message}` },
              })
              throw new Error(`🚫 ${violation.message}`)
            }
          }
        }

        // 4. Skill transmission ban - would need to inspect skill code
        // This is a runtime check - log reminder for skill development
        if (["edit", "write"].includes(tool) && args?.path?.includes(".agents/skills/")) {
          await ctx.client.app.log({
            body: { service: "ls-skill-guard", level: "info", message: "Skill development: Ensure no local data transmission to non-approved vendors. Check docs/APPROVED-VENDORS.md. See AGENTS.md §9.2 Skill Third-Party Transmission Ban." },
          })
        }

        return output
      },

      "tool.execute.after": async (input, output) => {
        // Reset skills-lock check on new session
        if (input.tool === "bash" && input.args?.command?.includes("git status")) {
          skillsLockChecked = false
        }
        return output
      },

      "session.created": async () => {
        await loadApprovedVendors()
        await ctx.client.app.log({
          body: { service: "ls-skill-guard", level: "info", message: `🛡️ LightSpeed Skill Guard initialized (Approved vendors: ${approvedVendors.length}, Retired skills blocked).` },
        })
      },
    }
  },
})
