import { Plugin } from "@opencode/plugin"

interface Rule {
  id: string
  type: string
  description: string
  severity: "error" | "warn" | "info"
  [key: string]: unknown
}

interface RuleViolation {
  ruleId: string
  severity: "error" | "warn" | "info"
  message: string
  tool?: string
  context?: Record<string, unknown>
}

interface SessionState {
  agentsMdRead: boolean
  agentsMdPath: string
  toolHistory: ToolCall[]
  retryCounts: Record<string, number>
  sameErrorCounts: Record<string, number>
  hasActiveTodo: boolean
  estimatedSteps: number
  lastEditWritePath: string | null
  lastEditWriteTool: string | null
  verificationPending: boolean
  pivotedAfterError: boolean
  reportedLimitation: boolean
  // Task lifecycle tracking
  taskId: string | null
  taskObjective: string | null
  taskPhase: "queued" | "running" | "blocked" | "waiting_for_approval" | "failed" | "completed" | "cancelled" | "suspected_stalled" | null
  taskStartTime: number | null
  taskLastHeartbeat: number | null
  taskAgentId: string | null
  taskParentId: string | null
  taskBlockers: string[]
  taskValidationResults: Record<string, "passed" | "failed" | "skipped" | "not_run">
}

interface ToolCall {
  tool: string
  args: Record<string, unknown>
  timestamp: number
  error?: string
  errorType?: string
}

const RULES_PATH = ".opencode/rules.json"

function classifyErrorType(error: string): string {
  if (error.includes("ParserError") || error.includes("Parser Error")) return "parser"
  if (error.includes("FileNotFound") || error.includes("not found")) return "not_found"
  if (error.includes("Permission denied")) return "permission"
  if (error.includes("Command not found") || error.includes("not recognized")) return "cmd_not_found"
  return "unknown"
}

function checkCommandPatterns(command: string, patterns: string[]): boolean {
  return patterns.some(p => new RegExp(p).test(command))
}

function checkPathPatterns(filePath: string, patterns: string[]): boolean {
  const normalized = filePath.replace(/\\/g, "/")
  return patterns.some(p => {
    const regex = p
      .replace(/\*\*/g, ".*")
      .replace(/\*/g, "[^/]*")
    return new RegExp(`^${regex}$`).test(normalized)
  })
}

export default Plugin.define({
  id: "rule-enforcer",
  async setup(ctx) {
    const storage = ctx.storage
    let rules: Rule[] = []
    let sessionState: SessionState = {
      agentsMdRead: false,
      agentsMdPath: "",
      toolHistory: [],
      retryCounts: {},
      sameErrorCounts: {},
      hasActiveTodo: false,
      estimatedSteps: 0,
      lastEditWritePath: null,
      lastEditWriteTool: null,
      verificationPending: false,
      pivotedAfterError: false,
      reportedLimitation: false,
      // Task lifecycle tracking
      taskId: null,
      taskObjective: null,
      taskPhase: null,
      taskStartTime: null,
      taskLastHeartbeat: null,
      taskAgentId: null,
      taskParentId: null,
      taskBlockers: [],
      taskValidationResults: {},
    }

    // Load rules from file
    async function loadRules() {
      try {
        const result = await ctx.client.file.read({ path: RULES_PATH })
        if (result.content) {
          const parsed = JSON.parse(result.content)
          rules = parsed.rules || []
        }
      } catch (e) {
        await ctx.client.app.log({
          body: {
            service: "rule-enforcer",
            level: "error",
            message: `Failed to load rules: ${e}`,
          },
        })
        rules = []
      }
    }

    function getSessionState() {
      const state = storage.get("session-state") as SessionState | null
      if (!state) {
        return { ...sessionState }
      }
      return state
    }

    function saveSessionState(state: SessionState) {
      storage.set("session-state", state)
    }

    // Initial load
    await loadRules()

    return {
      // Track AGENTS.md reading and tool usage
      "tool.execute.after": async (input: any, output: any) => {
        sessionState = getSessionState()

        if (input.tool === "read" && output.result) {
          const filePath = output.args?.path || ""
          const fileName = filePath.split(/[/\\]/).pop()?.toLowerCase() || ""
          if (fileName === "agents.md" || fileName === "claude.md") {
            sessionState.agentsMdRead = true
            sessionState.agentsMdPath = filePath
            saveSessionState(sessionState)
          }
        }

        // Track todo writes
        if (input.tool === "todowrite" && output.result) {
          sessionState.hasActiveTodo = true
          saveSessionState(sessionState)
        }

        // Track edit/write for verification
        if (["edit", "write"].includes(input.tool)) {
          sessionState.lastEditWritePath = output.args?.path || ""
          sessionState.lastEditWriteTool = input.tool
          sessionState.verificationPending = true
          saveSessionState(sessionState)
        }

        // Track verification (read after edit/write)
        if (input.tool === "read" && sessionState.verificationPending) {
          const readPath = output.args?.path || ""
          if (readPath === sessionState.lastEditWritePath) {
            sessionState.verificationPending = false
            sessionState.lastEditWritePath = null
            sessionState.lastEditWriteTool = null
            saveSessionState(sessionState)
          }
        }

        // Track tool history for retry detection
        const toolCall: ToolCall = {
          tool: input.tool,
          args: input.args || {},
          timestamp: Date.now(),
        }

        if (output.error) {
          toolCall.error = output.error
          toolCall.errorType = classifyErrorType(output.error)

          // Update retry counts
          const cmdKey = JSON.stringify({ tool: input.tool, args: input.args })
          const prevCount = sessionState.retryCounts[cmdKey] || 0
          sessionState.retryCounts[cmdKey] = prevCount + 1

          // Update same-error counts
          const errorType = toolCall.errorType || "unknown"
          const prevErrorCount = sessionState.sameErrorCounts[errorType] || 0
          sessionState.sameErrorCounts[errorType] = prevErrorCount + 1

          // Check if pivoted to different tool
          if (prevErrorCount >= 1 && sessionState.toolHistory.length > 0) {
            const lastTool = sessionState.toolHistory[sessionState.toolHistory.length - 1].tool
            if (lastTool !== input.tool) {
              sessionState.pivotedAfterError = true
            }
          }
        }

        sessionState.toolHistory.push(toolCall)
        if (sessionState.toolHistory.length > 100) {
          sessionState.toolHistory = sessionState.toolHistory.slice(-50)
        }

        // Task lifecycle: update heartbeat on every tool execution
        if (sessionState.taskId) {
          sessionState.taskLastHeartbeat = Date.now()
        }

        saveSessionState(sessionState)
        return output
      },

      // Main enforcement hook
      "tool.execute.before": async (input: any, output: any) => {
        sessionState = getSessionState()
        const violations: RuleViolation[] = []

        for (const rule of rules) {
          const violation = await checkRule(rule, input, output, sessionState, ctx)
          if (violation) violations.push(violation)
        }

        // Handle violations by severity
        const errors = violations.filter(v => v.severity === "error")
        const warns = violations.filter(v => v.severity === "warn")
        const infos = violations.filter(v => v.severity === "info")

        // Log warnings and infos
        for (const v of [...warns, ...infos]) {
          await ctx.client.app.log({
            body: {
              service: "rule-enforcer",
              level: v.severity === "warn" ? "warn" : "info",
              message: `[${v.ruleId}] ${v.message}`,
            },
          })
        }

        // Throw on errors (block the tool)
        if (errors.length > 0) {
          const messages = errors.map(e => `🚫 ${e.message}`).join("\n")
          throw new Error(messages)
        }

        return output
      },

      // Session events
      "session.created": async () => {
        sessionState = {
          agentsMdRead: false,
          agentsMdPath: "",
          toolHistory: [],
          retryCounts: {},
          sameErrorCounts: {},
          hasActiveTodo: false,
          estimatedSteps: 0,
          lastEditWritePath: null,
          lastEditWriteTool: null,
          verificationPending: false,
          pivotedAfterError: false,
          reportedLimitation: false,
          // Task lifecycle tracking
          taskId: null,
          taskObjective: null,
          taskPhase: null,
          taskStartTime: null,
          taskLastHeartbeat: null,
          taskAgentId: null,
          taskParentId: null,
          taskBlockers: [],
          taskValidationResults: {},
        }
        saveSessionState(sessionState)

        await ctx.client.app.log({
          body: {
            service: "rule-enforcer",
            level: "info",
            message: `📋 Rule enforcer initialized. ${rules.length} rules loaded.`,
          },
        })
      },

      "session.compacted": async () => {
        sessionState = getSessionState()
        // Keep agentsMdRead but reset other state
        sessionState.toolHistory = []
        sessionState.retryCounts = {}
        sessionState.sameErrorCounts = {}
        sessionState.pivotedAfterError = false
        sessionState.reportedLimitation = false
        // Reset task lifecycle state
        sessionState.taskId = null
        sessionState.taskObjective = null
        sessionState.taskPhase = null
        sessionState.taskStartTime = null
        sessionState.taskLastHeartbeat = null
        sessionState.taskBlockers = []
        sessionState.taskValidationResults = {}
        saveSessionState(sessionState)

        await ctx.client.app.log({
          body: {
            service: "rule-enforcer",
            level: "info",
            message: "🔄 Session compacted: rule enforcer state partially reset.",
          },
        })
      },
    }
  },
})

async function checkRule(
  rule: Rule,
  input: any,
  output: any,
  state: SessionState,
  ctx: any
): Promise<RuleViolation | null> {
  const { tool, args } = input

  switch (rule.type) {
    case "command_pattern": {
      if (tool !== "bash") return null
      if (rule.tool && rule.tool !== "bash") return null

      const command = args?.command || ""
      if (checkCommandPatterns(command, rule.patterns as string[])) {
        return {
          ruleId: rule.id,
          severity: rule.severity,
          message: rule.message as string,
          tool: "bash",
          context: { command },
        }
      }
      return null
    }

    case "path_block": {
      const filePath = args?.path || args?.pattern || ""
      if (!filePath) return null

      const actions = rule.actions as string[]
      if (!actions.includes(tool)) return null

      if (checkPathPatterns(filePath, rule.patterns as string[])) {
        return {
          ruleId: rule.id,
          severity: rule.severity,
          message: `Blocked: ${tool} on protected path "${filePath}"`,
          tool,
          context: { path: filePath },
        }
      }
      return null
    }

    case "tool_preference": {
      if (tool !== rule.blocked_tool) return null

      const command = args?.command || ""
      const patterns = rule.blocked_patterns as string[]
      if (checkCommandPatterns(command, patterns)) {
        return {
          ruleId: rule.id,
          severity: rule.severity,
          message: (rule.message as string) + ` Use ${rule.suggested_tool} instead.`,
          tool,
          context: { command, suggested: rule.suggested_tool },
        }
      }
      return null
    }

    case "tool_sequence": {
      const triggerTools = rule.trigger_tools as string[]
      if (!triggerTools.includes(tool)) return null

      // Check if verification is pending from previous edit/write
      if (rule.id === "verify-after-edit" && state.verificationPending) {
        if (tool !== "read") {
          const gap = state.toolHistory.filter(t =>
            ["read", "edit", "write", "bash", "grep", "glob", "task"].includes(t.tool)
          ).length
          if (gap > (rule.max_gap as number)) {
            return {
              ruleId: rule.id,
              severity: rule.severity,
              message: rule.message as string,
              tool,
              context: { pendingVerification: state.lastEditWritePath },
            }
          }
        }
      }
      return null
    }

    case "session_behavior": {
      // AGENTS.md required check
      if (rule.id === "agents-md-required") {
        if (!state.agentsMdRead && tool !== "read") {
          return {
            ruleId: rule.id,
            severity: rule.severity,
            message: rule.message as string,
            tool,
            context: {},
          }
        }
        return null
      }

      // Retry budget checks
      if (rule.id === "retry-budget-same-command") {
        const cmdKey = JSON.stringify({ tool, args })
        const count = state.retryCounts[cmdKey] || 0
        if (count > 1) {
          return {
            ruleId: rule.id,
            severity: rule.severity,
            message: rule.message as string,
            tool,
            context: { retryCount: count },
          }
        }
        return null
      }

      if (rule.id === "retry-budget-different-syntax") {
        const recentErrors = state.toolHistory
          .slice(-10)
          .filter(t => t.tool === tool && t.error)
        if (recentErrors.length > 2) {
          return {
            ruleId: rule.id,
            severity: rule.severity,
            message: rule.message as string,
            tool,
            context: { recentErrorCount: recentErrors.length },
          }
        }
        return null
      }

      if (rule.id === "retry-budget-escalation") {
        const recentErrors = state.toolHistory
          .slice(-5)
          .filter(t => t.error)
        if (recentErrors.length >= 3 && !state.reportedLimitation) {
          return {
            ruleId: rule.id,
            severity: rule.severity,
            message: rule.message as string,
            tool,
            context: { errorCount: recentErrors.length },
          }
        }
        return null
      }

      // Two-strike rule
      if (rule.id === "two-strike-rule") {
        for (const [errorType, count] of Object.entries(state.sameErrorCounts)) {
          if (count >= 2 && !state.pivotedAfterError) {
            return {
              ruleId: rule.id,
              severity: rule.severity,
              message: rule.message as string,
              tool,
              context: { errorType, count },
            }
          }
        }
        return null
      }

      // Running findings required (simplified)
      if (rule.id === "running-findings-required") {
        const toolCount = state.toolHistory.length
        if (toolCount > 5) {
          return null // Requires reasoning access
        }
        return null
      }

      // Early exit
      if (rule.id === "early-exit-enforcement") {
        const recent = state.toolHistory.slice(-5)
        const notFoundCount = recent.filter(t =>
          t.errorType === "not_found"
        ).length
        if (notFoundCount >= 3) {
          return {
            ruleId: rule.id,
            severity: rule.severity,
            message: rule.message as string,
            tool,
            context: { notFoundCount },
          }
        }
        return null
      }

      // Require todo for complex tasks
      if (rule.id === "require-todo-for-complex-tasks") {
        if (state.toolHistory.length > 10 && !state.hasActiveTodo) {
          return {
            ruleId: rule.id,
            severity: rule.severity,
            message: rule.message as string,
            tool,
            context: { toolCount: state.toolHistory.length },
          }
        }
        return null
      }

      return null
    }

    case "response_pattern": {
      // Would need access to model response - not available in tool hooks
      return null
    }

    default:
      return null
  }
}
