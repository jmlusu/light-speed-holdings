# Follow-up reminder: dev-machine bootstrap task (ai-company bootstrap)
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show(
    "REMINDER: Follow up on the dev-machine bootstrap task`n`n`ai-company bootstrap` finished and needs review. Run it again or verify the missing env vars.",
    "Follow-up: Bootstrap Task"
) | Out-Null
