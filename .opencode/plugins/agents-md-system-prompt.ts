import { Plugin } from "@opencode/plugin"

const AGENTS_MD_PATHS = [
  "AGENTS.md",
  ".ai-company/AGENTS.md",
  "CLAUDE.md",
  ".claude/CLAUDE.md",
]

export default Plugin.define({
  id: "agents-md-system-prompt",
  async setup(ctx) {
    const storage = ctx.storage

    // Load AGENTS.md content once per session
    let agentsContent = ""
    for (const path of AGENTS_MD_PATHS) {
      try {
        const result = await ctx.client.file.read({ path })
        if (result.content && result.content.length > 100) {
          agentsContent = result.content
          await storage.set("agents-md-path", path)
          break
        }
      } catch {
        // File doesn't exist, try next
      }
    }

    if (!agentsContent) {
      await ctx.client.app.log({
        body: {
          service: "agents-md-system-prompt",
          level: "warn",
          message: "⚠️ No AGENTS.md/CLAUDE.md found. System prompt injection skipped.",
        },
      })
      return {}
    }

    // Store for potential re-injection after compact
    await storage.set("agents-md-content", agentsContent)

    // Inject as system message at session start
    await ctx.client.session.createMessage({
      role: "system",
      content: `=== PROJECT AGENTS.md INSTRUCTIONS (from ${await storage.get("agents-md-path")}) ===\n\n${agentsContent}\n\n=== END AGENTS.md ===\n\nCRITICAL: You MUST follow these instructions in EVERY response, tool call, and decision. They are not suggestions.`,
    })

    await ctx.client.app.log({
      body: {
        service: "agents-md-system-prompt",
        level: "info",
        message: `✅ Injected AGENTS.md (${agentsContent.length} chars) as system prompt`,
      },
    })

    return {
      // Re-inject after session compaction (context reset)
      "session.compacted": async () => {
        const content = await storage.get("agents-md-content")
        const path = await storage.get("agents-md-path")
        if (content) {
          await ctx.client.session.createMessage({
            role: "system",
            content: `=== PROJECT AGENTS.md INSTRUCTIONS (from ${path}) ===\n\n${content}\n\n=== END AGENTS.md ===\n\nCRITICAL: You MUST follow these instructions in EVERY response, tool call, and decision. They are not suggestions.`,
          })
          await ctx.client.app.log({
            body: {
              service: "agents-md-system-prompt",
              level: "info",
              message: "🔄 Re-injected AGENTS.md after session compaction",
            },
          })
        }
      },
    }
  },
})
