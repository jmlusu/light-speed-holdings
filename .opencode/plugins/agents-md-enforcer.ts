import { Plugin } from "@opencode/plugin"

const AGENTS_MD_PATHS = [
  "AGENTS.md",
  ".ai-company/AGENTS.md",
  "CLAUDE.md",
  ".claude/CLAUDE.md",
]

function isAgentsFile(path: string): boolean {
  const fileName = path.split(/[/\\]/).pop()?.toLowerCase() || ""
  return AGENTS_MD_PATHS.some((p) => fileName === p.toLowerCase())
}

function findAgentsMd(projectDir: string): string | null {
  // We can't do sync fs in plugin, but we can track common locations
  return null // Will be handled by session storage
}

export default Plugin.define({
  id: "agents-md-enforcer",
  async setup(ctx) {
    const storage = ctx.storage

    // Initialize session state
    await storage.set("agents-md-read", false)
    await storage.set("agents-md-path", "")

    return {
      // On session creation, inject reminder
      "session.created": async () => {
        await storage.set("agents-md-read", false)
        await storage.set("agents-md-path", "")

        // Log a reminder that will appear in session
        await ctx.client.app.log({
          body: {
            service: "agents-md-enforcer",
            level: "warn",
            message: "📋 SESSION START: You MUST read AGENTS.md (or CLAUDE.md) before proceeding. Use the read tool to load it first.",
          },
        })
      },

      // Track when AGENTS.md is read
      "tool.execute.after": async (input, output) => {
        if (input.tool === "read" && output.result) {
          const filePath = output.args?.path || ""
          if (isAgentsFile(filePath)) {
            await storage.set("agents-md-read", true)
            await storage.set("agents-md-path", filePath)

            await ctx.client.app.log({
              body: {
                service: "agents-md-enforcer",
                level: "info",
                message: `✅ AGENTS.md loaded from "${filePath}". You may now proceed.`,
              },
            })
          }
        }
        return output
      },

      // Enforce on tool execution - warn if AGENTS.md not read
      "tool.execute.before": async (input, output) => {
        // Skip enforcement for read tool itself (allow reading AGENTS.md)
        if (input.tool === "read") {
          return output
        }

        // Skip for session/internal tools
        if (["session", "permission"].some(t => input.tool.startsWith(t))) {
          return output
        }

        const agentsRead = await storage.get("agents-md-read")
        const agentsPath = await storage.get("agents-md-path")

        if (!agentsRead) {
          // First violation - warn but allow
          const violationCount = (await storage.get("violation-count")) || 0
          const newCount = violationCount + 1
          await storage.set("violation-count", newCount)

          if (newCount === 1) {
            await ctx.client.app.log({
              body: {
                service: "agents-md-enforcer",
                level: "error",
                message: `🚫 BLOCKED: You must read AGENTS.md before using tools. Use 'read' tool on AGENTS.md first. This is violation #${newCount}.`,
              },
            })

            // Throw to block the tool
            throw new Error(
              `🚫 ENFORCED: You must read AGENTS.md (or CLAUDE.md) before using any tools. ` +
              `Run: read({ path: "AGENTS.md" }) or read({ path: "CLAUDE.md" }) first. ` +
              `This was violation #${newCount}.`
            )
          } else if (newCount <= 3) {
            // Escalating warnings
            await ctx.client.app.log({
              body: {
                service: "agents-md-enforcer",
                level: "error",
                message: `🚫 VIOLATION #${newCount}: Still haven't read AGENTS.md. Tool "${input.tool}" blocked.`,
              },
            })
            throw new Error(
              `🚫 VIOLATION #${newCount}: You have not read AGENTS.md yet. ` +
              `Tool "${input.tool}" is blocked until you read the instructions file. ` +
              `Use: read({ path: "AGENTS.md" })`
            )
          } else {
            // Hard block after 3 violations
            await ctx.client.app.log({
              body: {
                service: "agents-md-enforcer",
                level: "error",
                message: `🔴 HARD BLOCK: ${newCount} violations. Session requires AGENTS.md compliance.`,
              },
            })
            throw new Error(
              `🔴 HARD BLOCK: ${newCount} policy violations. ` +
              `You MUST read AGENTS.md before continuing. ` +
              `No tools will work until compliance is achieved.`
            )
          }
        }

        // Verify the AGENTS.md content was actually read (not just the tool called)
        if (agentsRead && agentsPath) {
          // Optionally verify content was substantial
          const contentLength = (await storage.get("agents-md-length")) || 0
          if (contentLength < 100) {
            await ctx.client.app.log({
              body: {
                service: "agents-md-enforcer",
                level: "warn",
                message: `⚠️ AGENTS.md read but content seems short (${contentLength} chars). Please ensure you read the full file.`,
              },
            })
        }

        return output
      },

      // Track content length when reading
      "tool.execute.after": async (input, output) => {
        if (input.tool === "read" && output.result) {
          const filePath = output.args?.path || ""
          if (isAgentsFile(filePath)) {
            const content = output.result.content || ""
            await storage.set("agents-md-length", content.length)
          }
        }
        return output
      },

      // Reset on session compact (new context)
      "session.compacted": async () => {
        await storage.set("agents-md-read", false)
        await storage.set("agents-md-path", "")
        await storage.set("violation-count", 0)

        await ctx.client.app.log({
          body: {
            service: "agents-md-enforcer",
            level: "warn",
            message: "🔄 Session compacted: AGENTS.md must be re-read for new context.",
          },
        })
      },
    }
  },
})
