---
name: issue-triage
description: Fetch and prioritize open GitHub issues for a repository. Use when managing GitHub issues, triaging bugs, prioritizing work, reviewing issue backlog, or when user asks to "triage issues", "show open issues", "prioritize issues", or "what should I work on next". Ranks issues by priority (Critical/P0 → High/P1 → Old bugs → Other) and displays as a scannable markdown table.
---

# Issue Triage

Fetch, rank, and display open GitHub issues by priority for efficient backlog management.

## Workflow

### 1. Fetch and Rank Issues

Run the fetch script:

```bash
python3 scripts/fetch_issues.py
```

Or specify a repository:

```bash
python3 scripts/fetch_issues.py --repo owner/repo
```

### 2. Format Output

Parse the JSON output and display as markdown table:

| # | Title | Priority | Labels | Age | Excerpt | Link |
|---|-------|----------|--------|-----|---------|------|
| 42 | Fix login crash | Critical/P0 label | `critical`, `bug` | 3d | User reports app crashes when... | [#42](url) |

### 3. Follow-up

After displaying the table, ask: "Which issue number would you like to investigate further?"

When user selects an issue, suggest running the investigation skill:

> To investigate this issue, run:
> ```
> @investigate-bug {issue_number}
> ```

Or fetch full details with:

```bash
gh issue view <number> --repo <repo>
```

## Priority Ranking Logic

1. **Critical/P0**: Labels containing `critical`, `p0`, `priority: critical`, `severity: critical`
2. **High-priority/P1**: Labels containing `high-priority`, `p1`, `priority: high`
3. **Aging bugs**: `bug` label AND created > 7 days ago
4. **Standard**: All other open issues

Within each tier, older issues rank higher.

## Error Handling

| Error | Message to User |
|-------|-----------------|
| Not in git repo | "Run from a git repository or specify --repo owner/repo" |
| gh not installed | "Install GitHub CLI: https://cli.github.com/" |
| Not authenticated | "Run `gh auth login` to authenticate" |
| Repo not found | "Repository not found or not accessible. Check the repo name and your permissions." |
| No issues | "✅ No open issues found in {repo}" |

## Example Output

```
## Open Issues for owner/repo (12 total)

| # | Title | Priority | Labels | Age | Excerpt | Link |
|---|-------|----------|--------|-----|---------|------|
| 89 | Database connection drops | Critical/P0 label | `critical`, `backend` | 2d | Production users experiencing... | [#89](url) |
| 67 | Memory leak in worker | High-priority/P1 label | `p1`, `performance` | 5d | Memory usage grows unbounded... | [#67](url) |
| 45 | Button alignment broken | Bug (12 days old) | `bug`, `ui` | 12d | Submit button misaligned on... | [#45](url) |
| 23 | Add dark mode | Standard priority | `enhancement` | 30d | Users have requested dark... | [#23](url) |

**Which issue number would you like to investigate further?**
```

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@investigate-bug` | **Next step** - Deep dive into selected issue |
| `@fix-planner` | **After investigation** - Creates implementation plan |
| `@implement-fix` | **After planning** - Executes the fix |
| `@create-pr` | **Final step** - Creates pull request |

## Complete Workflow

```
@issue-triage
    ↓ Select issue #142
@investigate-bug 142
    ↓ Posts investigation report
@fix-planner 142
    ↓ Posts fix plan
@implement-fix 142
    ↓ Commits changes
@create-pr 142
    ↓ Opens PR
```
