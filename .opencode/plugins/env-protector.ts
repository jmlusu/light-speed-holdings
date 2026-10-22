import { Plugin } from "@opencode/plugin"

const PROTECTED_FILES = [
  ".env",
  ".env.local",
  ".env.staging.example",
  ".env.example",
  ".env.production",
  ".env.development",
]

function isProtectedFile(path: string): boolean {
  const fileName = path.split(/[/\\]/).pop()?.toLowerCase() || ""
  return PROTECTED_FILES.some((protectedFile) =>
    fileName === protectedFile.toLowerCase() ||
    fileName.endsWith("." + protectedFile.toLowerCase())
  )
}

export default Plugin.define({
  id: "env-protector",
  async setup(ctx) {
    return {
      "tool.execute.before": async (input, output) => {
        // Block read tool
        if (input.tool === "read") {
          const filePath = output.args?.path || ""
          if (isProtectedFile(filePath)) {
            throw new Error(
              `🛡️  Blocked: Reading protected environment file "${filePath}" is not allowed. ` +
              `These files contain sensitive secrets.`
            )
          }
        }

        // Block edit tool (modifying env files)
        if (input.tool === "edit") {
          const filePath = output.args?.path || ""
          if (isProtectedFile(filePath)) {
            throw new Error(
              `🛡️  Blocked: Editing protected environment file "${filePath}" is not allowed.`
            )
          }
        }

        // Block write tool (creating env files)
        if (input.tool === "write") {
          const filePath = output.args?.path || ""
          if (isProtectedFile(filePath)) {
            throw new Error(
              `🛡️  Blocked: Creating protected environment file "${filePath}" is not allowed.`
            )
          }
        }

        // Block glob tool on protected files
        if (input.tool === "glob") {
          const pattern = output.args?.pattern || ""
          if (PROTECTED_FILES.some(p => pattern.includes(p))) {
            throw new Error(
              `🛡️  Blocked: Glob pattern "${pattern}" targets protected environment files.`
            )
          }
        }

        // Block grep tool on protected files
        if (input.tool === "grep") {
          const path = output.args?.path || ""
          if (path && isProtectedFile(path)) {
            throw new Error(
              `🛡️  Blocked: Grep on protected environment file "${path}" is not allowed.`
            )
          }
        }

        return output
      },
    }
  },
})
