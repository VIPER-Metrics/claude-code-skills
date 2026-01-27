---
name: implement-fix
description: Execute a bug fix based on an approved implementation plan. Use when the user wants to implement a fix, execute a fix plan, make the code changes, or says "implement fix", "execute fix", "make the changes for issue #X", "fix issue #X". Requires a fix plan from @fix-planner to exist first.
---

# Implement Fix

Execute code changes based on an approved fix plan.

## Usage

```
/implement-fix {issue_number}
```

## Workflow

### Step 1: Load Fix Plan

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

Look for the fix plan:
```bash
# Try local file first
cat docs/fix-plans/FIX-$ARGUMENTS-plan.md

# If not found locally, fetch from GitHub
gh issue view $ARGUMENTS --json comments --jq '.comments[].body' | grep -A 1000 "# Fix Plan:"
```

**If no plan found:**
> No fix plan found for issue #{number}.
>
> Run `@fix-planner {issue_number}` first to create a fix plan.

### Step 2: Validate Prerequisites

Check the pre-implementation checklist from the plan:

```bash
# Verify tests pass before changes
python -m pytest --tb=short
```

**If tests fail:**
> ⚠️ Test suite has failures before starting. Fix existing tests first or confirm you want to proceed.

### Step 3: Create Worktree

Create an isolated worktree for the fix (instead of switching branches in the main repo):

```bash
# Ensure we have latest from remote
git fetch origin

# Get short description from issue title for directory and branch name
SHORT_DESC=$(gh issue view $ARGUMENTS --json title --jq '.title' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)
BRANCH_NAME="fix-$ARGUMENTS-$SHORT_DESC"
WORKTREE_DIR=~/GitHub/viper-metrics-worktrees/$ARGUMENTS-$SHORT_DESC

# Create worktree with new branch from published (main branch)
git worktree add "$WORKTREE_DIR" -b "$BRANCH_NAME" origin/published

# Change into the worktree
cd "$WORKTREE_DIR"
```

**Note:** Branch names must NOT contain slashes (Anvil requirement). Use `fix-123-description` format.

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

### Step 6: Run Tests

Execute the test suite:
```bash
# Run all tests
python -m pytest --tb=short

# Or if specific test command in plan
{test_command_from_plan}
```

**If tests fail:**
- Analyze the failure
- If it's the new test: check if implementation is wrong
- If it's an existing test: check for regression
- Fix and re-run until all pass

### Step 7: Data Remediation (if applicable)

If the plan includes a Data Remediation section:

1. **Create the remediation script:**
```bash
mkdir -p scripts/remediation
# Write script to: scripts/remediation/fix_{issue_number}_remediation.py
```

2. **Follow the script template** from the plan

3. **DO NOT run the script** - just create it for manual execution later

### Step 8: Commit Changes

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

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Step 9: Verify Final State

Final checks:
```bash
# Confirm all changes committed
git status

# Show what was changed
git diff HEAD~1 --stat

# Verify tests still pass
python -m pytest --tb=short
```

### Step 10: Session Complete

Output:
> ## Implementation Complete
>
> **Issue:** #{number} - {title}
>
> **Worktree:** `{worktree_dir}`
>
> **Branch:** `{branch_name}`
>
> **Changes:**
> - {file1}: {change summary}
> - {file2}: {change summary}
>
> **Tests:** ✅ All passing ({count} tests)
>
> **Commit:** `{commit_hash}`
>
> ---
>
> ### Next step:
> ```
> @create-pr {issue_number}
> ```
>
> ### After PR is merged:
> ```bash
> # Remove the worktree
> git worktree remove {worktree_dir}
> ```

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

### Keep Tests Green
- Run tests frequently
- Don't move on with failing tests
- If stuck, report the failure

### Document Deviations
- If you must deviate from plan, document why
- Note any additional changes needed
- Suggest plan updates for future

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Plan not found | "Run @fix-planner {number} first" |
| Code doesn't match plan | STOP - "Code at {file}:{line} doesn't match plan. Was it modified?" |
| Tests fail after changes | Analyze and fix, or ask for help |
| File doesn't exist | STOP - "File {path} from plan doesn't exist" |
| Merge conflict | "Branch has conflicts. Resolve before continuing." |

---

## Constraints

**MUST:**
- Read the plan before making any changes
- Only modify files listed in the plan
- Run tests before and after changes
- Commit all changes before ending session

**MUST NOT:**
- Modify files outside the plan's scope
- Skip test execution
- Leave uncommitted changes
- Run data remediation scripts (manual step)

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@fix-planner` | **Prerequisite** - Must have a fix plan |
| `@create-pr` | **Next step** - Creates PR from this branch |
