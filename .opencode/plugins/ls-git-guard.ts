import { Plugin } from "@opencode/plugin"

interface RuleViolation {
  ruleId: string
  severity: "error" | "warn" | "info"
  message: string
  tool?: string
  context?: Record<string, unknown>
}

interface SessionState {
  gitHygieneChecked: boolean
  stashInspected: boolean
  divergenceMapped: boolean
  lastBranchOp: string | null
  lastStashOp: string | null
}

const PROTECTED_BRANCHES = ["main", "develop"]
const BRANCH_OPERATIONS = ["checkout", "switch", "merge", "rebase", "pull"]

export default Plugin.define({
  id: "ls-git-guard",
  async setup(ctx) {
    const storage = ctx.storage
    let sessionState: SessionState = {
      gitHygieneChecked: false,
      stashInspected: false,
      divergenceMapped: false,
      lastBranchOp: null,
      lastStashOp: null,
    }

    function getSessionState() {
      const state = storage.get("session-state") as SessionState | null
      if (!state) return { ...sessionState }
      return state
    }

    function saveSessionState(state: SessionState) {
      storage.set("session-state", state)
    }

    function isProtectedBranch(branch: string): boolean {
      return PROTECTED_BRANCHES.includes(branch.toLowerCase())
    }

    function isBranchOperation(command: string): boolean {
      const lower = command.toLowerCase()
      return BRANCH_OPERATIONS.some(op => lower.includes(`git ${op}`))
    }

    function isStashOperation(command: string): boolean {
      const lower = command.toLowerCase()
      return lower.includes("git stash")
    }

    function isMergeOperation(command: string): boolean {
      return command.toLowerCase().includes("git merge")
    }

    function isRebaseOperation(command: string): boolean {
      return command.toLowerCase().includes("git rebase")
    }

    function isPushToProtected(command: string): boolean {
      const lower = command.toLowerCase()
      return lower.includes("git push") && PROTECTED_BRANCHES.some(b => lower.includes(b))
    }

    async function logViolation(violation: RuleViolation) {
      await ctx.client.app.log({
        body: {
          service: "ls-git-guard",
          level: violation.severity === "error" ? "error" : violation.severity === "warn" ? "warn" : "info",
          message: `[${violation.ruleId}] ${violation.message}`,
        },
      })
    }

    return {
      "tool.execute.before": async (input: any, output: any) => {
        const { tool, args } = input
        const command = args?.command || ""
        const violations: RuleViolation[] = []

        sessionState = getSessionState()

        // 1. Require git status + git submodule status before first branch/merge operation
        if (tool === "bash" && isBranchOperation(command) && !sessionState.gitHygieneChecked) {
          violations.push({
            ruleId: "git-hygiene-preflight",
            severity: "warn",
            message: "Git hygiene preflight not performed. Run 'git status' and 'git submodule status' before branch operations. See AGENTS.md §Git & Repository Management Hygiene.",
            tool: "bash",
            context: { command },
          })
        }

        // 2. Require stash inspection before checkout/switch when stashes may exist
        if (tool === "bash" && (command.includes("git checkout") || command.includes("git switch")) && !sessionState.stashInspected) {
          violations.push({
            ruleId: "git-stash-inspection",
            severity: "warn",
            message: "Switching branches without inspecting stashes. Run 'git stash list' and 'git stash show -p' to prevent accidental work loss. See AGENTS.md §Git & Repository Management Hygiene.",
            tool: "bash",
            context: { command },
          })
        }

        // 3. Require divergence mapping before complex rebase/consolidation
        if (tool === "bash" && isRebaseOperation(command) && !sessionState.divergenceMapped) {
          violations.push({
            ruleId: "git-divergence-mapping",
            severity: "warn",
            message: "Complex rebase without divergence map. Run 'git log --oneline --all --graph' to map branch divergence before rebasing. See AGENTS.md §Git & Repository Management Hygiene.",
            tool: "bash",
            context: { command },
          })
        }

        // 4. Warn on push to protected branches (main, develop)
        if (tool === "bash" && isPushToProtected(command)) {
          violations.push({
            ruleId: "git-no-direct-push-protected-branches",
            severity: "warn",
            message: `Direct push to protected branch detected. Use PR flow: push feature branch, then 'gh pr create'. See AGENTS.md §5 and constitution 11-GIT-STANDARDS.md.`,
            tool: "bash",
            context: { command },
          })
        }

        // 5. Warn on bare git stash push without -m
        if (tool === "bash" && command.toLowerCase().includes("git stash push") && !command.includes("-m")) {
          violations.push({
            ruleId: "git-stash-descriptive-label",
            severity: "warn",
            message: "Stash created without descriptive label. Use 'git stash push -m \"description_of_work\"' for traceability. See AGENTS.md §Git & Repository Management Hygiene.",
            tool: "bash",
            context: { command },
          })
        }

        // 6. Warn on git merge without prior submodule audit
        if (tool === "bash" && isMergeOperation(command) && !command.includes("submodule")) {
          // Check if submodules exist
          try {
            const subResult = await ctx.client.file.read({ path: ".gitmodules" })
            if (subResult.content) {
              violations.push({
                ruleId: "git-submodule-audit-before-merge",
                severity: "warn",
                message: "Repository has submodules. Run 'git submodule status' and 'git submodule update --init --recursive' before merging. See AGENTS.md §Git & Repository Management Hygiene.",
                tool: "bash",
                context: { command },
              })
            }
          } catch {
            // No .gitmodules file
          }
        }

        // Log warnings
        for (const v of violations) {
          await logViolation(v)
        }

        // Track state changes
        if (tool === "bash") {
          if (command.includes("git status") && command.includes("git submodule status")) {
            sessionState.gitHygieneChecked = true
          }
          if (command.includes("git stash list")) {
            sessionState.stashInspected = true
          }
          if (command.includes("git log") && command.includes("--all") && command.includes("--graph")) {
            sessionState.divergenceMapped = true
          }
          if (isBranchOperation(command)) {
            sessionState.lastBranchOp = command
          }
          if (isStashOperation(command)) {
            sessionState.lastStashOp = command
          }
          saveSessionState(sessionState)
        }

        return output
      },

      "session.created": async () => {
        sessionState = {
          gitHygieneChecked: false,
          stashInspected: false,
          divergenceMapped: false,
          lastBranchOp: null,
          lastStashOp: null,
        }
        saveSessionState(sessionState)

        await ctx.client.app.log({
          body: {
            service: "ls-git-guard",
            level: "info",
            message: "🔀 LightSpeed Git Guard initialized (hygiene, stash, divergence, protected-branch checks).",
          },
        })
      },

      "session.compacted": async () => {
        sessionState = getSessionState()
        // Keep hygiene state but reset tracking
        sessionState.lastBranchOp = null
        sessionState.lastStashOp = null
        saveSessionState(sessionState)
      },
    }
  },
})
