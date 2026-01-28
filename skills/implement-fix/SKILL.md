---
name: implement-fix
description: Execute a bug fix based on an approved implementation plan. Use when the user wants to implement a fix, execute a fix plan, make the code changes, or says "implement fix", "execute fix", "make the changes for issue #X", "fix issue #X". Requires a fix plan from @fix-planner to exist first.
---

# Implement Fix

Execute code changes based on an approved fix plan using git worktrees for isolated development.

## Usage

```
/implement-fix {issue_number}
```

## Workflow

### Step 1: Load Fix Plan

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

Look for the fix plan at `wiki/issues/$ARGUMENTS/fix-plan.md`:
```bash
# Load the fix plan from wiki
cat wiki/issues/$ARGUMENTS/fix-plan.md
```

**If no plan found:**
> No fix plan found for issue #{number}.
>
> Run `/fix-planner {issue_number}` first to create a fix plan.

Also load the investigation report for context:
```bash
cat wiki/issues/$ARGUMENTS/investigation.md
```

### Step 2: Create Git Worktree

Use git worktrees to enable parallel development on multiple branches:

```bash
# Get short description from issue title
ISSUE_NUM=$ARGUMENTS
TITLE=$(gh issue view $ISSUE_NUM --json title --jq '.title' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g' | cut -c1-30)
BRANCH_NAME="fix-${ISSUE_NUM}-${TITLE}"
WORKTREE_PATH="$HOME/GitHub/viper-metrics-worktrees/${ISSUE_NUM}-${TITLE}"

# Ensure we're up to date with staging
git fetch origin

# Create the branch from master (staging)
git branch "$BRANCH_NAME" origin/master 2>/dev/null || echo "Branch already exists"

# Create the worktree
git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"

# Navigate to the worktree
cd "$WORKTREE_PATH"
```

**If worktree already exists:**
```bash
# Just navigate to existing worktree
cd "$WORKTREE_PATH"
git status
```

### Step 3: Validate Prerequisites

Check the pre-implementation checklist from the plan:

```bash
# Verify we're in the correct worktree
pwd
git branch --show-current

# Confirm clean state
git status
```

### Step 4: Execute Code Changes

For each change in the Implementation Steps:

1. **Read the target file:**
   - Verify the current code matches what the plan expects
   - If different, STOP and report the discrepancy

2. **Make the change:**
   - Apply only the specific change from the plan
   - Preserve surrounding code exactly
   - Follow the plan's edge case handling

3. **Verify the change:**
   - Re-read the file to confirm change applied correctly

**Important constraints:**
- ONLY modify files listed in the plan's scope
- ONLY change lines specified in the plan
- If plan says "don't modify X", do NOT touch X
- If something seems wrong, STOP and ask

### Step 5: Write/Update Tests

From the Testing Strategy section:

1. **Create new test files** if specified
2. **Add test functions** as defined in the plan
3. **Follow the test code** provided in the plan

Use the exact test structure from the plan when provided.

### Step 6: Create Test Plan

Create a detailed test plan document and save to wiki:

Save to: `wiki/issues/$ARGUMENTS/test-plan.md`

```markdown
---
title: "Test Plan: Issue #$ARGUMENTS"
date: $(date +%Y-%m-%d)
author: Claude
status: ready
issue: $ARGUMENTS
tags: [testing, bug-fix]
---

# Test Plan: Issue #{issue_number}

**Issue:** #{issue_number} - {title}
**Branch:** `{branch_name}`
**Worktree:** `{worktree_path}`

---

## Pre-Fix State (Reproduce Bug)

### Steps to Reproduce
1. {step 1}
2. {step 2}
3. {step 3}

### Expected (Buggy) Behavior
- {what currently happens incorrectly}

### Evidence
- Screenshot/log location: {if applicable}

---

## Post-Fix Verification

### Steps to Verify Fix
1. {step 1}
2. {step 2}
3. {step 3}

### Expected (Correct) Behavior
- {what should happen after fix}

---

## Regression Tests

Check that these related features still work:

| Feature | Test Steps | Expected Result | Status |
|---------|------------|-----------------|--------|
| {feature 1} | {how to test} | {expected} | ⬜ |
| {feature 2} | {how to test} | {expected} | ⬜ |
| {feature 3} | {how to test} | {expected} | ⬜ |

---

## Edge Cases

| Scenario | Test Steps | Expected Result | Status |
|----------|------------|-----------------|--------|
| {edge case 1} | {how to test} | {expected} | ⬜ |
| {edge case 2} | {how to test} | {expected} | ⬜ |

---

## Automated Tests

| Test File | Test Name | Purpose | Status |
|-----------|-----------|---------|--------|
| `{test_file}` | `test_{name}` | {what it verifies} | ⬜ |

---

## Test Environment

- **App URL:** https://app.vipermetrics.com (or staging)
- **Test Company:** {company name}
- **Test User:** {user email}
- **Browser:** Chrome (latest)

---

## Sign-Off

- [ ] Bug reproduction confirmed before fix
- [ ] Fix verified working
- [ ] Regression tests passed
- [ ] Edge cases tested
- [ ] Automated tests passing
- [ ] Ready for PR review

**Tested By:** _______________
**Date:** _______________
```

### Step 7: Post Test Plan to GitHub

Add the test plan as a comment on the issue:
```bash
gh issue comment $ARGUMENTS --body-file wiki/issues/$ARGUMENTS/test-plan.md
```

### Step 7.5: Sync Test Plan to Main Repo Wiki

Copy the test plan back to the main repo's wiki folder so it's available outside the worktree:

```bash
# Get the main repo path
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"

# Create the wiki folder in main repo if it doesn't exist
mkdir -p "$MAIN_REPO/wiki/issues/$ARGUMENTS"

# Copy the test plan to main repo wiki
cp wiki/issues/$ARGUMENTS/test-plan.md "$MAIN_REPO/wiki/issues/$ARGUMENTS/"
```

This ensures the test plan is accessible from the main repo for reference, even before the PR is merged.

### Step 8: Data Remediation (if applicable)

If the plan includes a Data Remediation section:

1. **Create the remediation script:**
```bash
mkdir -p scripts/remediation
# Write script to: scripts/remediation/fix_{issue_number}_remediation.py
```

2. **Follow the script template** from the plan

3. **DO NOT run the script** - just create it for manual execution later

### Step 9: Commit Changes

Stage and commit with proper message:

```bash
# Stage all changes
git add -A

# Commit with structured message
git commit -m "$(cat <<'EOF'
Fix #{issue_number}: {short_description}

- {Change 1 summary}
- {Change 2 summary}
- Added tests for {what}

Closes #{issue_number}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 10: Verify Final State

Final checks:
```bash
# Confirm all changes committed
git status

# Show what was changed
git diff HEAD~1 --stat

# Confirm branch and worktree
git branch --show-current
pwd
```

### Step 11: Session Complete

Output:
> ## Implementation Complete
>
> **Issue:** #{number} - {title}
>
> **Branch:** `{branch_name}`
>
> **Worktree:** `{worktree_path}`
>
> **Changes:**
> - {file1}: {change summary}
> - {file2}: {change summary}
>
> **Commit:** `{commit_hash}`
>
> **Test Plan:** `wiki/issues/{number}/test-plan.md` (also posted to GitHub issue)
>
> ---
>
> ### Next steps:
> 1. Run manual tests from the test plan
> 2. When verified, run: `/create-pr {issue_number}`
>
> ### Worktree commands:
> ```bash
> # Return to this worktree later
> cd {worktree_path}
>
> # List all worktrees
> git worktree list
>
> # Remove after PR merged
> git worktree remove {worktree_path}
> ```

---

## Git Worktree Reference

### Why Worktrees?
- Work on multiple bug fixes simultaneously
- Each fix is isolated in its own directory
- No need to stash/switch branches
- Can run different versions side-by-side

### Common Commands
```bash
# List all worktrees
git worktree list

# Create new worktree
git worktree add ~/GitHub/viper-metrics-worktrees/{name} {branch}

# Remove worktree (after PR merged)
git worktree remove ~/GitHub/viper-metrics-worktrees/{name}

# Prune stale worktree references
git worktree prune
```

### Directory Structure
```
~/GitHub/viper-metrics-v2-0/                    # Main repo
~/GitHub/viper-metrics-worktrees/
├── 123-fix-login-error/                        # Worktree for issue #123
├── 456-pagination-bug/                         # Worktree for issue #456
└── {issue}-{short-name}/                       # Pattern for new worktrees
```

All branches are created from `master` (staging) and PRs go to `master`.

---

## Guidelines

### Follow the Plan Exactly
- Don't improvise or add extra changes
- Don't "improve" code outside the plan's scope
- If the plan is wrong, stop and update it first

### One Change at a Time
- Make each change from the plan separately
- Verify after each change
- Commit logical chunks if plan is large

### Document Everything
- Create comprehensive test plans
- Post updates to GitHub issue
- Note any deviations from plan

### Keep the Worktree Clean
- Commit all changes before leaving
- Don't mix changes from other issues
- Remove worktree after PR merged

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Plan not found | "Run /fix-planner {number} first" |
| Code doesn't match plan | STOP - "Code at {file}:{line} doesn't match plan. Was it modified?" |
| File doesn't exist | STOP - "File {path} from plan doesn't exist" |
| Worktree already exists | Navigate to existing worktree and continue |
| Branch already exists | Use existing branch for worktree |

---

## Constraints

**MUST:**
- Read the plan before making any changes
- Only modify files listed in the plan
- Create and post test plan to GitHub
- Commit all changes before ending session
- Use worktrees for branch isolation

**MUST NOT:**
- Modify files outside the plan's scope
- Leave uncommitted changes
- Run data remediation scripts (manual step)
- Work directly on published/main branch

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/fix-planner` | **Prerequisite** - Must have a fix plan |
| `/create-pr` | **Next step** - Creates PR from this branch |

---

## Wiki Structure

After implementation, the wiki should contain (in both worktree AND main repo):
```
wiki/issues/$ARGUMENTS/
├── investigation.md    # From /investigate-bug
├── fix-plan.md         # From /fix-planner
└── test-plan.md        # From /implement-fix (this skill)
```

The test plan is created in the worktree and synced back to the main repo's wiki folder so it's accessible for reference even before the PR is merged.
