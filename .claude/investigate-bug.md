---
name: investigate-bug
description: Deep dive investigation of a GitHub issue to identify root cause, affected files, and scope. Use when the user wants to investigate a bug, analyze an issue, find the root cause, or says "investigate issue", "debug issue", "analyze bug", "what's causing issue #X". Creates an investigation report and posts it to the GitHub issue.
---

# Investigate Bug

Deep dive into a GitHub issue to identify root cause, affected code, and define fix scope.

## Usage

```
/investigate-bug {issue_number}
```

## Workflow

### Step 0: Branch Setup

**Ensure working from master branch** (staging with accumulated fixes):
```bash
git checkout master && git pull origin master
```
This ensures you investigate against the latest code including pending fixes.

> **Note**: `published` is production - only compare to it when checking live behavior.

### Step 1: Validate Input

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

Fetch the issue:
```bash
gh issue view $ARGUMENTS --json number,title,body,labels,state
```

**Validation checks:**
- Issue must exist
- Issue should have `bug` label (warn if missing, but continue)
- Issue should be open (warn if closed)

### Step 2: Extract Bug Context

Parse the issue body for:
- **Error messages** - Look for stack traces, exception text
- **Reproduction steps** - How to trigger the bug
- **Expected vs actual behavior** - What should happen vs what happens
- **Environment details** - Version, OS, browser, etc.
- **User-reported files** - Any files mentioned by the reporter

### Step 3: Code Investigation

Search for relevant code based on extracted context:

1. **Search for error messages:**
```bash
grep -rn "error_text_from_issue" --include="*.py"
```

2. **Find related functions/classes:**
```bash
grep -rn "function_name" --include="*.py"
```

3. **Read and trace the error path:**
- Start from the error location
- Trace backwards to find the root cause
- Document the call chain

### Step 4: Identify Root Cause

Analyze findings to determine:
- **Primary cause** - The actual bug (code error, missing check, etc.)
- **Contributing factors** - Conditions that expose the bug
- **Impact assessment** - What breaks, who is affected

### Step 5: Define Scope

Create explicit boundaries:

**WILL modify (In-Scope):**
- List specific files and functions
- Include line number ranges if known
- Note any new files needed

**WILL NOT modify (Out-of-Scope):**
- Related files that should not change
- Features/systems that are explicitly excluded
- Why they're excluded (prevent scope creep)

### Step 6: Testing Requirements

Identify what needs testing:
- **Unit tests** - Functions to test
- **Integration tests** - Flows to verify
- **Manual tests** - Steps to reproduce and verify fix
- **Regression risks** - What else might break

### Step 7: Data Assessment

Check if data remediation is needed:
- Are there corrupted records?
- Estimate count of affected records
- Note any queries to identify them

### Step 8: Generate Report

Create the investigation report using this format:

```markdown
# Investigation Report: Issue #{number}

**Issue:** {title}
**Investigated:** {date}
**Status:** Investigation Complete

---

## Summary

{2-3 sentence summary of the bug and its root cause}

---

## Root Cause Analysis

### Primary Cause
{Detailed explanation of what's causing the bug}

### Code Location
- **File:** `{file_path}`
- **Function:** `{function_name}`
- **Lines:** {start}-{end}

### Error Path
1. {Entry point}
2. {Intermediate step}
3. {Where error occurs}

### Contributing Factors
- {Factor 1}
- {Factor 2}

---

## Affected Files

| File | Type | Lines | Purpose |
|------|------|-------|---------|
| `{path}` | Primary | {range} | {why it needs changes} |
| `{path}` | Secondary | {range} | {why it needs changes} |

---

## Scope Definition

### WILL Modify (In-Scope)
- [ ] `{file1}` - {what changes}
- [ ] `{file2}` - {what changes}

### WILL NOT Modify (Out-of-Scope)
- `{file}` - {reason excluded}
- `{feature}` - {reason excluded}

---

## Testing Requirements

### Unit Tests
| Test | Purpose |
|------|---------|
| `test_{name}` | Verify {behavior} |

### Integration Tests
- [ ] {Scenario 1}
- [ ] {Scenario 2}

### Manual Verification
1. {Step to reproduce bug}
2. {Step to verify fix}
3. {Expected outcome}

### Regression Risks
- {Area 1} - {why it might break}
- {Area 2} - {why it might break}

---

## Data Remediation

**Needed:** {Yes/No}

{If yes:}
- **Affected records:** ~{count}
- **Tables:** {list}
- **Query to identify:** `{query}`

---

## Recommendations

1. {Priority recommendation}
2. {Secondary recommendation}
3. {Any warnings or concerns}

---

## Next Steps

Run `@fix-planner {issue_number}` to generate implementation plan.
```

### Step 9: Post to GitHub

Save locally and post to GitHub:

```bash
# Save to local file
mkdir -p docs/investigations
# Save report to: docs/investigations/INVESTIGATION-{issue_number}.md

# Post as GitHub comment
gh issue comment $ARGUMENTS --body-file docs/investigations/INVESTIGATION-$ARGUMENTS.md

# Add label
gh issue edit $ARGUMENTS --add-label "investigated"
```

### Step 10: Session Complete

Output:
> ## Investigation Complete
>
> **Issue:** #{number} - {title}
>
> **Root Cause:** {brief summary}
>
> **Report saved to:** `docs/investigations/INVESTIGATION-{number}.md`
>
> **Posted to:** GitHub issue as comment
>
> ---
>
> ### Next step:
> ```
> @fix-planner {issue_number}
> ```

---

## Guidelines

### Be Thorough But Focused
- Investigate enough to identify root cause
- Don't go down rabbit holes unrelated to the bug
- Document dead ends briefly

### Preserve Evidence
- Include actual error messages and stack traces
- Quote relevant code snippets
- Note file paths and line numbers

### Stay Objective
- Report findings, not opinions
- Separate facts from hypotheses
- Mark uncertain conclusions

### Scope Carefully
- Keep scope as small as possible
- Explicitly exclude related-but-separate issues
- Note potential follow-up issues

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Issue not found | "Issue #{n} not found. Check the number and try again." |
| No bug label | "⚠️ Issue #{n} doesn't have a 'bug' label. Proceeding with investigation anyway." |
| Cannot find code | "Could not locate code related to: {search}. Please provide more context." |
| Multiple possible causes | List all possibilities with confidence levels |

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@issue-triage` | **Predecessor** - May suggest issues to investigate |
| `@fix-planner` | **Next step** - Uses this investigation report |
