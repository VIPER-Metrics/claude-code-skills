---
name: create-pr
description: Generate and create a GitHub pull request for a completed implementation. Use when the user wants to create a PR, submit changes for review, open a pull request, or says "create PR", "make PR", "submit PR for issue #X", "open pull request". Works for both bug fixes and feature implementations.
---

# Create PR

Generate and create a GitHub pull request from a completed implementation (bug fix or feature).

## Usage

```
/create-pr {issue_number}
```

## Workflow

### Step 1: Validate State

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

Verify prerequisites:
```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Should be on a fix-* or feature-* branch
if [[ ! "$CURRENT_BRANCH" =~ ^(fix|feature)- ]]; then
    echo "Warning: Not on a fix or feature branch"
fi

# Check for uncommitted changes
git status --porcelain

# Check if we're in a worktree
git worktree list | grep "$(pwd)"
```

**Validations:**
- Must be on a `fix-*` or `feature-*` branch
- No uncommitted changes
- Branch has commits ahead of base

### Step 2: Determine PR Type and Base Branch

```bash
CURRENT_BRANCH=$(git branch --show-current)

# All PRs go to master (staging)
BASE_BRANCH="master"

if [[ "$CURRENT_BRANCH" =~ ^fix- ]]; then
    PR_TYPE="Bug Fix"
    LABEL="bug"
elif [[ "$CURRENT_BRANCH" =~ ^feature- ]]; then
    PR_TYPE="Feature"
    LABEL="enhancement"
else
    # Ask user
    echo "Could not determine PR type from branch name"
fi
```

**Branch strategy:**
- All branches are created from `master` (staging)
- All PRs go to `master` (staging)
- `master` is periodically released to `published` (production)

### Step 3: Gather Context

Fetch information for PR description:

```bash
# Get issue details
gh issue view $ARGUMENTS --json title,body,labels

# Get the relevant plan from wiki
if [[ -f "wiki/issues/$ARGUMENTS/fix-plan.md" ]]; then
    PLAN_FILE="wiki/issues/$ARGUMENTS/fix-plan.md"
elif [[ -f "wiki/issues/$ARGUMENTS/feature-plan.md" ]]; then
    PLAN_FILE="wiki/issues/$ARGUMENTS/feature-plan.md"
fi

# Get investigation report if it exists (bug fixes)
if [[ -f "wiki/issues/$ARGUMENTS/investigation.md" ]]; then
    cat "wiki/issues/$ARGUMENTS/investigation.md"
fi

# Get test plan
if [[ -f "wiki/issues/$ARGUMENTS/test-plan.md" ]]; then
    cat "wiki/issues/$ARGUMENTS/test-plan.md"
fi

# Get commit history on this branch
git log $BASE_BRANCH..HEAD --oneline

# Get changed files
git diff $BASE_BRANCH --stat
```

### Step 4: Generate PR Description

Create the PR description based on type:

#### For Bug Fixes:
```markdown
## Summary

{2-3 sentence summary from fix plan}

Fixes #{issue_number}

## Root Cause

{Brief explanation of the bug's root cause from investigation}

## Solution

{How this PR fixes the root cause}

## Changes Made

| File | Change |
|------|--------|
| `{file1}` | {what changed} |
| `{file2}` | {what changed} |

## Testing

### Test Plan
See full test plan: [wiki/issues/{number}/test-plan.md](wiki/issues/{number}/test-plan.md)

### Verification Summary
- [ ] Bug reproduction confirmed (fails before fix)
- [ ] Fix verified working
- [ ] Regression tests passed
- [ ] Edge cases tested

## Data Remediation

{If applicable:}
- **Script:** `scripts/remediation/fix_{number}_remediation.py`
- **Run after merge:** Yes/No
- **Estimated records:** {count}

{If not applicable:}
N/A - No data remediation required

## Code Review Checklist

- [ ] Changes match the approved fix plan
- [ ] Only files in scope were modified
- [ ] No out-of-scope changes
- [ ] Error handling is appropriate
- [ ] Code follows VIPER Metrics conventions

## Related Documentation

- [Investigation Report](wiki/issues/{number}/investigation.md)
- [Fix Plan](wiki/issues/{number}/fix-plan.md)
- [Test Plan](wiki/issues/{number}/test-plan.md)

---
*Generated with Claude Code*
```

#### For Features:
```markdown
## Summary

{2-3 sentence summary from feature plan}

Implements #{issue_number}

## Changes Made

| File | Change |
|------|--------|
| `{file1}` | {what was added} |
| `{file2}` | {what was added} |

## New Functionality

{Description of what the feature does}

## Testing

### Test Plan
See full test plan: [wiki/issues/{number}/test-plan.md](wiki/issues/{number}/test-plan.md)

### Verification Summary
- [ ] All acceptance criteria met
- [ ] Use cases tested
- [ ] Permissions working correctly
- [ ] Regression tests passed

## Anvil IDE Tasks

{If applicable:}
- [ ] Database changes applied
- [ ] Form YAML created
- [ ] Permissions configured

{If not applicable:}
N/A - No Anvil IDE tasks required

## Code Review Checklist

- [ ] Changes match the approved feature plan
- [ ] Only files in scope were modified
- [ ] Server functions have proper authorization
- [ ] Error handling is appropriate
- [ ] Code follows VIPER Metrics conventions

## Related Documentation

- [Feature Plan](wiki/issues/{number}/feature-plan.md)
- [Test Plan](wiki/issues/{number}/test-plan.md)

---
*Generated with Claude Code*
```

### Step 5: Push Branch

Push to remote:
```bash
# Push with upstream tracking
git push -u origin $(git branch --show-current)
```

### Step 6: Create Pull Request

Create the PR using GitHub CLI:

```bash
# All PRs go to master (staging)
BASE="master"

# Create PR
gh pr create \
  --title "{Type} #{issue_number}: {short_title}" \
  --body-file /tmp/pr-description.md \
  --base $BASE \
  --label "$LABEL"
```

**PR Title Format:**
- Bug fixes: `Fix #{number}: {Short description}`
- Features: `Feature #{number}: {Short description}`

### Step 7: Link PR to Issue

Add comment to original issue:
```bash
PR_URL=$(gh pr view --json url --jq '.url')
gh issue comment $ARGUMENTS --body "Pull request created: $PR_URL"
```

### Step 8: Update Labels

```bash
# Add PR-submitted label to issue
gh issue edit $ARGUMENTS --add-label "pr-submitted"

# Remove planning labels if present
gh issue edit $ARGUMENTS --remove-label "ready-to-implement" 2>/dev/null || true
gh issue edit $ARGUMENTS --remove-label "planned" 2>/dev/null || true
```

### Step 9: Session Complete

Output:
> ## Pull Request Created
>
> **Issue:** #{number} - {title}
>
> **PR:** {pr_url}
>
> **Branch:** `{branch_name}` → `{base_branch}`
>
> **Type:** {Bug Fix / Feature}
>
> **Files changed:** {count}
>
> ---
>
> ### Next steps:
> 1. Request code review
> 2. Address review feedback
> 3. Merge when approved
> 4. Run data remediation if needed (post-deployment)
>
> ### Worktree cleanup (after merge):
> ```bash
> git worktree remove {worktree_path}
> ```

---

## Branch Strategy

```
published (production)
    ↑
    │ (periodic release)
    │
master (staging)
    ↑
    ├── fix-123-bug-name          # Bug fixes merge to staging
    └── feature-789-feature-name  # Features merge to staging
```

**Why staging first?**
- All changes go through `master` (staging) for testing
- `master` is periodically released to `published` (production)
- This ensures all changes are tested before reaching production

---

## Guidelines

### Clear Descriptions
- Summarize changes concisely
- Explain the "why" not just the "what"
- Link to all related documentation

### Reference Wiki Documents
- Always link to investigation (for bugs)
- Always link to plan (fix-plan or feature-plan)
- Always link to test-plan

### Complete Checklists
- Fill out all checklist items
- Don't leave items unchecked without explanation
- Add custom items if relevant

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Not on fix/feature branch | "Switch to the correct branch or specify worktree path" |
| Uncommitted changes | "Commit or stash changes before creating PR" |
| No commits on branch | "No changes to submit. Run /implement-fix or /implement-feature first" |
| PR already exists | Show existing PR URL: "PR already exists: {url}" |
| Push fails | "Push failed. Check permissions and try: `git push -u origin {branch}`" |
| Wiki files missing | Warn but continue - include issue link instead |

---

## PR Title Format

Use consistent format:
```
{Type} #{issue_number}: {Short description}
```

Examples:
- `Fix #142: Resolve image download AttributeError`
- `Fix #89: Prevent database connection timeout`
- `Feature #789: Add bulk export for inspection reports`
- `Feature #456: Implement dark mode support`

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/implement-fix` | **Prerequisite** - For bug fixes |
| `/implement-feature` | **Prerequisite** - For features |
| `/issue-triage` | **Cycle complete** - Returns to triage for next issue |

---

## Wiki Structure Reference

When creating a PR, these files should exist:

**For Bug Fixes:**
```
wiki/issues/{number}/
├── investigation.md    # From /investigate-bug
├── fix-plan.md         # From /fix-planner
└── test-plan.md        # From /implement-fix
```

**For Features:**
```
wiki/issues/{number}/
├── feature-plan.md     # From /feature-planner
└── test-plan.md        # From /implement-feature
```

---

## Complete Workflow Reference

### Bug Fix Workflow:
```
/investigate-bug 142
    ↓ Creates investigation.md
/fix-planner 142
    ↓ Creates fix-plan.md
/implement-fix 142
    ↓ Creates test-plan.md, commits code (branch from master)
/create-pr 142
    ↓ Opens PR to master (staging)
    → Code Review → Merge → Test in staging → Release to published
```

### Feature Workflow:
```
/feature-planner 789
    ↓ Creates feature-plan.md
/implement-feature 789
    ↓ Creates test-plan.md, commits code (branch from master)
/create-pr 789
    ↓ Opens PR to master (staging)
    → Code Review → Merge → Test in staging → Release to published
```
