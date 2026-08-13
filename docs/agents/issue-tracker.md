# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues, using the `gh pr` equivalents:

- **Read a PR**: `gh pr view <number> --comments` and `gh pr diff <number>` for the diff.
- **List external PRs for triage**: `gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments` then keep only `authorAssociation` of `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE` (drop `OWNER`/`MEMBER`/`COLLABORATOR`).
- **Comment / label / close**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either — resolve with `gh pr view 42` and fall back to `gh issue view 42`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

## Wayfinding operations

How `/wayfinder` expresses its map, tickets, blocking, and frontier queries in this repo.

### The map

A single GitHub issue labelled `wayfinder:map`. Found with:

```bash
gh issue list --state all --label "wayfinder:map" --json number,title,state
```

### Tickets

Child issues of the map, each carrying one `wayfinder:<type>` label — `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`.

Parent-child wiring uses GitHub **sub-issues** (native hierarchy) where the `gh` CLI supports it:

```bash
gh issue create --title "<ticket title>" --body "<question>" --label "wayfinder:grilling"
gh api --method POST repos/jmlusu/light-speed-holdings/issues/<map-number>/sub_issues -f sub_issue_id=<ticket-id>
```

If sub-issues are unavailable, fall back to listing the child ticket references in the map's body.

### Blocking

GitHub's `gh` CLI exposes no native issue-dependency command, so blocking uses the **body-convention fallback**: each ticket lists its blocking tickets by name and number in its body, e.g. `Blocked by: <Ticket name> (#42)`. A ticket is **unblocked** when every ticket it names as a blocker is closed.

### Frontier

The open, unblocked, unclaimed tickets — the edge of the known. Find them by querying the ticket-type labels and resolving blockers by hand:

```bash
gh issue list --state open --label "wayfinder:research" --json number,title,assignees
gh issue list --state open --label "wayfinder:prototype" --json number,title,assignees
gh issue list --state open --label "wayfinder:grilling" --json number,title,assignees
gh issue list --state open --label "wayfinder:task" --json number,title,assignees
```

An unclaimed ticket has an empty `assignees` array; claiming is assigning yourself before any work. Filter the results to tickets whose body-declared blockers are all closed.
