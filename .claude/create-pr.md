---
name: create-pr
description: Generate and create a GitHub pull request for a completed bug fix. Use when the user wants to create a PR, submit changes for review, open a pull request, or says "create PR", "make PR", "submit PR for issue #X", "open pull request". Requires changes to be committed on a fix branch.
---

# Create PR

Generate and create a GitHub pull request from a completed bug fix implementation.

## Usage

```
/create-pr {issue_number}
```

## Workflow

### Step 1: Validate State

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

Verify prerequisites:
```bash
# Get current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Check we're on a fix or feature branch (worktree pattern uses fix-{n} or feature-{n})
if [[ ! "$CURRENT_BRANCH" =~ ^(fix|feature)- ]]; then
    echo "Not on a fix/feature branch. Current: $CURRENT_BRANCH"
fi

# Check for uncommitted changes
git status --porcelain

# Verify this is a worktree (optional - provides context)
git worktree list | grep "$(pwd)"
```

**Validations:**
- Must be on a `fix-*` or `feature-*` branch (worktree pattern)
- No uncommitted changes
- Branch has commits ahead of base (`published`)

### Step 2: Gather Context

Fetch information for PR description:

```bash
# Get issue details
gh issue view $ARGUMENTS --json title,body,labels

# Get fix plan (for summary)
cat docs/fix-plans/FIX-$ARGUMENTS-plan.md 2>/dev/null || \
  gh issue view $ARGUMENTS --json comments --jq '.comments[] | select(.body | contains("# Fix Plan:")) | .body'

# Get commit history on this branch (from published base)
git log origin/published..HEAD --oneline

# Get changed files
git diff origin/published --stat
```

### Step 3: Generate PR Description

Create the PR description:

```markdown
## Summary

{2-3 sentence summary from fix plan}

Fixes #{issue_number}

## Changes Made

{List each file changed with brief description}

- `{file1}`: {what changed}
- `{file2}`: {what changed}

## Root Cause

{Brief explanation of the bug's root cause from investigation}

## Solution

{How this PR fixes the root cause}

## Testing Done

### Automated Tests
- [ ] All existing tests pass
- [ ] Added new tests:
  - `test_{name1}`: {what it tests}
  - `test_{name2}`: {what it tests}

### Manual Testing
- [ ] Reproduced original bug (confirmed it fails before fix)
- [ ] Verified fix resolves the issue
- [ ] Checked for regressions in related features

## Code Review Checklist

- [ ] Changes match the approved fix plan
- [ ] Only files in scope were modified
- [ ] No out-of-scope changes
- [ ] Error handling is appropriate
- [ ] Code follows project conventions
- [ ] No new security vulnerabilities

## Data Remediation

{If applicable:}
- **Script:** `scripts/remediation/fix_{number}_remediation.py`
- **Run after merge:** Yes/No
- **Estimated records:** {count}

{If not applicable:}
N/A - No data remediation required

## Deployment Notes

{Any special deployment considerations}

## Related Links

- Issue: #{issue_number}
- Investigation: {link to investigation comment}
- Fix Plan: {link to fix plan comment}

---

🤖 Generated with [Claude Code](https://claude.ai/code)
```

### Step 4: Push Branch

Push to remote:
```bash
# Push with upstream tracking
git push -u origin $(git branch --show-current)
```

### Step 5: Create Pull Request

Create the PR using GitHub CLI:

```bash
gh pr create \
  --title "Fix #{issue_number}: {short_title}" \
  --body-file /tmp/pr-description.md \
  --base published \
  --label "bug-fix"
```

Or with inline body using heredoc:
```bash
gh pr create --title "Fix #$ARGUMENTS: {title}" --body "$(cat <<'EOF'
{PR description from Step 3}
EOF
)"
```

### Step 6: Link PR to Issue

Add comment to original issue:
```bash
PR_URL=$(gh pr view --json url --jq '.url')
gh issue comment $ARGUMENTS --body "Pull request created: $PR_URL"
```

### Step 7: Update Labels

```bash
# Add PR-submitted label to issue
gh issue edit $ARGUMENTS --add-label "pr-submitted"

# Remove ready-to-implement if present
gh issue edit $ARGUMENTS --remove-label "ready-to-implement" 2>/dev/null || true
```

### Step 8: Session Complete

Output:
> ## Pull Request Created
>
> **Issue:** #{number} - {title}
>
> **PR:** {pr_url}
>
> **Worktree:** `{current_directory}`
>
> **Branch:** `{branch_name}` → `published`
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
> 5. **Clean up worktree** after merge:
>    ```bash
>    cd ~/GitHub/viper-metrics-v2-0  # Return to main repo
>    git worktree remove {worktree_dir}
>    ```

---

## Guidelines

### Clear Descriptions
- Summarize changes concisely
- Explain the "why" not just the "what"
- Link to relevant context

### Complete Checklist
- Fill out all checklist items
- Don't leave items unchecked without explanation
- Add custom items if relevant

### Proper Linking
- Always reference the issue number
- Link to investigation and fix plan
- Connect related PRs if any

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Not on fix/feature branch | "You're not in a worktree. Create one with: `git worktree add ~/GitHub/viper-metrics-worktrees/{n}-{name} -b fix-{n}-{name} origin/published`" |
| Uncommitted changes | "Commit or stash changes before creating PR" |
| No commits on branch | "No changes to submit. Run @implement-fix first" |
| PR already exists | Show existing PR URL: "PR already exists: {url}" |
| Push fails | "Push failed. Check permissions and try: `git push -u origin {branch}`" |
| Not in a worktree | "Navigate to the worktree directory: `cd ~/GitHub/viper-metrics-worktrees/{issue}-{name}`" |

---

## PR Title Format

Use consistent format:
```
Fix #{issue_number}: {Short description}
```

Examples:
- `Fix #142: Resolve image download AttributeError`
- `Fix #89: Prevent database connection timeout`
- `Fix #67: Handle null values in user preferences`

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@implement-fix` | **Prerequisite** - Must have committed changes |
| `@issue-triage` | **Cycle complete** - Returns to triage for next issue |

---

## Complete Workflow Reference

```
@issue-triage
    ↓ "Which issue?" → #142
@investigate-bug 142
    ↓ Posts investigation report
@fix-planner 142
    ↓ Posts fix plan
@implement-fix 142
    ↓ Commits changes to branch
@create-pr 142
    ↓ Opens PR
    → Code Review → Merge → Deploy
```
