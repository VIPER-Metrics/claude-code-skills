---
name: xero-time-entries
description: Generate Xero time entry JSON files from git commits for monthly billing. Use when the user wants to create time entries, generate billing data, prepare monthly invoices, upload time to Xero, or says "time entries", "monthly billing", "invoice hours", or "log time".
---

# Xero Time Entry Generator

Generate time entry JSON files from git commit history, organized by client, ready for upload to Xero Projects via the VIPER Admin app.

## Usage

```
/xero-time-entries
/xero-time-entries february 2026
```

## Context

- **Upload app:** VIPER Admin (`~/GitHub/VIPER-Admin`)
- **Upload form:** `client_code/UploadTimeEntries/` - accepts JSON files
- **Output directory:** `~/GitHub/xero-time-entries/`
- **Repos to scan:** `~/GitHub/viper-metrics-v2-0`, `~/GitHub/viper-operator`, `~/GitHub/viper-inspect`

### JSON Schema (accepted by upload form)

```json
{
  "project": "Partial match against Xero project name (auto-selects dropdown)",
  "task": "Exact match against task name within the project (auto-selects dropdown)",
  "entries": [
    {
      "developer": "First name (Rick, Jarred, Divyesh)",
      "date": "YYYY-MM-DD",
      "hours": 8.5,
      "description": "What was worked on"
    }
  ]
}
```

### Git Author to Developer Mapping

| Git Authors | Developer Name |
|-------------|---------------|
| `Rick-VIPER`, `rick@vipermetrics.com` | Rick |
| `Jarred-Viper`, `jarred@vipermetrics.com` | Jarred |
| `Divyesh`, `divyesh-vipermetrics`, `divyesh@vipermetrics.com` | Divyesh |

## Workflow

### Step 1: Determine Time Period

If `$ARGUMENTS` contains a month/date range, use it. Otherwise ask:

> What billing period should I generate time entries for?

Options:
- Last month (most common)
- Current month so far
- Custom date range

Determine the `--since` and `--until` dates for git log.

### Step 2: Identify Clients

Ask the user:

> Which clients are we generating time entries for?

Show these known clients as options (allow multiple selection):
- **Paramount** - Custom development
- **David Campbell Transport (Campbells)** - Implementation/support hours
- **EG (Energy Group)** - Training/support
- **Central OOTH (Centrals)** - Support hours
- Other (specify)

### Step 3: Fetch Git Commits

For each VIPER repo, fetch commits for the billing period:

```bash
# For each repo in: viper-metrics-v2-0, viper-operator, viper-inspect
cd ~/GitHub/{repo}
git log --format="%ad | %an | %s" --date=short --since="{start}" --until="{end}" --no-merges
```

### Step 4: Organize by Developer and Date

Group all commits by:
1. **Developer** (map git authors to first names)
2. **Date** (YYYY-MM-DD)

Present a summary table to the user:

```
Developer | Date       | Commits | Repos
----------|------------|---------|------
Rick      | 2026-02-03 | 5       | viper-metrics-v2-0
Rick      | 2026-02-04 | 3       | viper-metrics-v2-0, viper-inspect
Jarred    | 2026-02-03 | 4       | viper-metrics-v2-0
...
```

### Step 5: Assign Work to Clients

For each developer-date combination, show the commit messages and ask the user to assign them to a client. Group consecutive days where possible.

> **Rick - 2026-02-03** (5 commits):
> - Fix defect sync duplicate detection
> - Add pagination to service board
> - Update asset hire header calculation
>
> Which client should this day be assigned to?

Provide the client list from Step 2 as options. Allow splitting a day across clients if needed (rare).

### Step 6: Determine Hours

For each developer-date, ask about hours or use defaults:

> What are the standard daily hours?

Typical values:
- Rick: 8.5 - 9.0 hours
- Jarred: 8.5 - 9.0 hours
- Divyesh: 8.5 - 9.0 hours

Ask if the user wants to set hours per-day or use a default for each developer.

### Step 7: Generate Descriptions

For each developer-date entry, synthesize a concise description from the commit messages:
- Combine related commits into a single description
- Keep descriptions under 80 characters
- Focus on the feature/fix, not implementation details
- Use comma separation for multiple topics

**Good:** "Defect sync: duplicate detection, cascade errors"
**Bad:** "Fix merge optimization edge case when version_ts == edited_ts"

### Step 8: Ask About Project and Task Names

For each client, ask:

> What Xero project and task name should I use for **{client}**?
>
> Previous month used:
> - Project: `{previous project name if available}`
> - Task: `{previous task name if available}`
>
> Keep the same project and update the month in the task name?

Check `~/GitHub/xero-time-entries/` for previous month's files to suggest defaults.

### Step 9: Generate JSON Files

Write one JSON file per client to `~/GitHub/xero-time-entries/`:

**Filename pattern:** `{month}_{year}_{client_short}.json`
Example: `february_2026_paramount.json`

```json
{
  "project": "Custom Development - PO: maintenancesoftwareMF",
  "task": "Paramount Custom Development February 2026",
  "entries": [
    {
      "developer": "Rick",
      "date": "2026-02-03",
      "hours": 9.0,
      "description": "Defect sync: duplicate detection, cascade errors"
    }
  ]
}
```

### Step 10: Summary and Next Steps

Present a summary:

> ## Time Entries Generated
>
> | Client | File | Entries | Total Hours |
> |--------|------|---------|-------------|
> | Paramount | `february_2026_paramount.json` | 7 | 61.0 |
> | Campbells | `february_2026_campbells.json` | 6 | 52.5 |
> | ... | ... | ... | ... |
>
> **Total:** {n} entries, {h} hours across {c} clients
>
> ### To upload:
> 1. Open VIPER Admin at https://admin.vipermetrics.com
> 2. Go to **Upload Time Entries**
> 3. Upload each JSON file - project and task will auto-select
> 4. Verify staff mappings and click **Upload to Xero**

---

## Guidelines

### Handling Ambiguous Commits
- If a commit could apply to multiple clients, ask the user
- General platform fixes (error handling, CI) - ask which client to bill to
- If a branch name references an issue number, check which client it relates to

### Splitting Days
- A developer usually works for one client per day
- If commits clearly span two clients on the same day, split the hours
- Ask the user when unsure

### Weekends and Non-Working Days
- Flag any commits on weekends for user confirmation
- Some developers may work weekends - don't assume they don't

### Previous Month Reference
- Always check `~/GitHub/xero-time-entries/` for last month's files
- Use previous project names and patterns as defaults
- The task name typically follows: `{Client} {Type} {Month} {Year}`

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No commits found for a developer | Note it and ask if they were on leave |
| Very few commits on a day | Ask if it was a short day or commits were squashed |
| Commits only in one repo | Normal - most work is in viper-metrics-v2-0 |
| Unknown git author | Ask user to identify the developer |
| No previous month files | Ask user for project/task names from scratch |
