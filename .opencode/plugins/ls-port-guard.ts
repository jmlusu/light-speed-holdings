import { Plugin } from "@opencode/plugin"

interface RuleViolation {
  ruleId: string
  severity: "error" | "warn" | "info"
  message: string
  tool?: string
  context?: Record<string, unknown>
}

const DASHBOARD_PORTS = {
  prod: 8420,
  dev: 8421,
}
const VITE_PORTS = {
  dev: 1441,
  preview: 1440,
}

const DASHBOARD_CMDS = ["ai-company dashboard", "uv run ai-company dashboard"]
const VITE_CMDS = ["npm run dev", "npm run preview", "vite"]

export default Plugin.define({
  id: "ls-port-guard",
  async setup(ctx) {
    return {
      "tool.execute.before": async (input, output) => {
        const { tool, args } = input
        const command = args?.command || ""

        // 1. Dashboard commands must use correct ports
        if (tool === "bash" && command) {
          for (const dashCmd of DASHBOARD_CMDS) {
            if (command.includes(dashCmd)) {
              // Check for wrong port flags
              if (command.includes("--port 1440") || command.includes("--port 1441")) {
                const violation: RuleViolation = {
                  ruleId: "dashboard-wrong-port",
                  severity: "error",
                  message: `Dashboard ports: prod=8420, dev=8421. Vite ports (1440/1441) are for external app only. See AGENTS.md §12-13.`,
                  tool,
                  context: { command, correctPorts: DASHBOARD_PORTS },
                }
                await ctx.client.app.log({
                  body: { service: "ls-port-guard", level: "error", message: `[${violation.ruleId}] ${violation.message}` },
                })
                throw new Error(`🚫 ${violation.message}`)
              }

              // Warn if no explicit port (defaults to 8420 prod)
              if (!command.includes("--port")) {
                await ctx.client.app.log({
                  body: { service: "ls-port-guard", level: "warn", message: "Dashboard defaults to prod port 8420. For dev, use --port 8421. See AGENTS.md §13." },
                })
              }
            }
          }

          // 2. Vite commands must use correct ports
          for (const viteCmd of VITE_CMDS) {
            if (command.includes(viteCmd)) {
              if (command.includes("--port 8420") || command.includes("--port 8421")) {
                const violation: RuleViolation = {
                  ruleId: "vite-wrong-port",
                  severity: "error",
                  message: `Vite ports: dev=1441, preview=1440. Dashboard ports (8420/8421) are for internal API only. See AGENTS.md §12-13.`,
                  tool,
                  context: { command, correctPorts: VITE_PORTS },
                }
                await ctx.client.app.log({
                  body: { service: "ls-port-guard", level: "error", message: `[${violation.ruleId}] ${violation.message}` },
                })
                throw new Error(`🚫 ${violation.message}`)
              }
            }
          }

          // 3. Port conflict detection (common mistakes)
          const portPatterns = [
            { pattern: /--port\s+(\d+)/g, ports: { 8420: "dashboard-prod", 8421: "dashboard-dev", 1440: "vite-preview", 1441: "vite-dev" } },
          ]

          for (const { pattern, ports } of portPatterns) {
            let match
            while ((match = pattern.exec(command)) !== null) {
              const port = parseInt(match[1])
              if (ports[port]) {
                const service = ports[port]
                const isDashboard = command.includes("dashboard")
                const isVite = VITE_CMDS.some(v => command.includes(v))

                if (isDashboard && port >= 1440 && port <= 1441) {
                  // Already caught above
                } else if (isVite && (port === 8420 || port === 8421)) {
                  // Already caught above
                }
              }
            }
          }
        }

        // 4. Config file checks - verify CORS allowlist in dashboard config
        if (["edit", "write"].includes(tool) && args?.path) {
          const filePath = args.path
          if (filePath.includes("dashboard") && (filePath.endsWith(".py") || filePath.endsWith(".ts") || filePath.endsWith(".json") || filePath.endsWith(".yml"))) {
            // Just log reminder
            await ctx.client.app.log({
              body: { service: "ls-port-guard", level: "info", message: "Ensure CORS allowlist includes both dashboard (8420/8421) and Vite (1440/1441) origins. See AGENTS.md §12-13." },
            })
          }
        }

        return output
      },

      "session.created": async () => {
        await ctx.client.app.log({
          body: { service: "ls-port-guard", level: "info", message: "🔌 LightSpeed Port Guard initialized (Dashboard 8420/8421 vs Vite 1440/1441)." },
        })
      },
    }
  },
})
