---
name: implement-feature
description: Execute a feature implementation based on an approved feature plan. Use when the user wants to implement a feature, execute a feature plan, build a new feature, or says "implement feature", "build feature", "make the feature for issue #X". Requires a feature plan from @feature-planner to exist first.
---

# Implement Feature

Execute code changes based on an approved feature plan.

## Usage

```
/implement-feature {issue_number}
```

## Workflow

### Step 1: Load Feature Plan

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

Look for the feature plan:
```bash
# Try local file first
cat docs/feature-plans/FEATURE-$ARGUMENTS-plan.md

# If not found locally, fetch from GitHub
gh issue view $ARGUMENTS --json comments --jq '.comments[].body' | grep -A 1000 "# Feature Plan:"
```

**If no plan found:**
> No feature plan found for issue #{number}.
>
> Run `@feature-planner {issue_number}` first to create a feature plan.

### Step 2: Validate Prerequisites

Check the pre-implementation checklist from the plan:

```bash
# Verify tests pass before changes
python -m pytest --tb=short
```

**If tests fail:**
> Warning: Test suite has failures before starting. Fix existing tests first or confirm you want to proceed.

### Step 3: Confirm Database Changes

If the plan includes Data Model Changes:

> **Database Changes Required**
>
> The following changes need to be made in Anvil IDE:
> - {table changes from plan}
>
> Have you completed the database changes in Anvil IDE? (yes/no)

**If database changes not done:** Wait for user to complete them and pull changes before proceeding.

### Step 4: Create Worktree

Create an isolated worktree for the feature (instead of switching branches in the main repo):

```bash
# Ensure we have latest from remote
git fetch origin

# Get short description from issue title for directory and branch name
SHORT_DESC=$(gh issue view $ARGUMENTS --json title --jq '.title' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)
BRANCH_NAME="feature-$ARGUMENTS-$SHORT_DESC"
WORKTREE_DIR=~/GitHub/viper-metrics-worktrees/$ARGUMENTS-$SHORT_DESC

# Create worktree with new branch from published (main branch)
git worktree add "$WORKTREE_DIR" -b "$BRANCH_NAME" origin/published

# Change into the worktree
cd "$WORKTREE_DIR"
```

**Note:** Branch names must NOT contain slashes (Anvil requirement). Use `feature-123-description` format.

### Step 5: Execute Implementation Phases

Follow the plan's Implementation Steps phase by phase:

#### Phase 1: Data Layer (if applicable)
- Skip if no schema changes, or note that database changes were done in Anvil IDE
- Create any migration scripts specified

#### Phase 2: Server Layer
For each server function in the plan:

1. **Create or navigate to the module file:**
   - Use the exact path specified in the plan
   - Follow the OTS pattern if creating new module

2. **Implement the function:**
   - Use the exact code from the plan as a starting point
   - Add proper error handling
   - Include all authorization decorators

3. **Verify imports:**
   - Add necessary imports at top of file
   - Import from correct modules

#### Phase 3: Client Layer
For each form/component in the plan:

1. **Create form YAML** (in Anvil IDE if needed):
   - Note: Form YAML must be created/modified in Anvil IDE
   - List the required form structure for manual creation

2. **Implement form code:**
   - Follow the exact code structure from the plan
   - Wire up event handlers
   - Handle loading states and errors

3. **Add navigation:**
   - Connect to existing navigation as specified
   - Check permission requirements

#### Phase 4: Integration
- Wire up all components together
- Test the user flow end-to-end

**Important constraints:**
- Follow the plan's phased approach
- Complete each phase before moving to the next
- If something doesn't fit, STOP and ask

### Step 6: Write Tests

From the Testing Strategy section:

1. **Create new test files** if specified
2. **Add test functions** as defined in the plan
3. **Follow the test code** provided in the plan

Use the exact test structure from the plan when provided.

### Step 7: Run Tests

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

### Step 8: Manual Testing Checkpoint

Before committing, perform the manual testing steps from the plan:

> **Manual Testing Required**
>
> Please test the following scenarios:
> 1. {Test scenario 1 from plan}
> 2. {Test scenario 2 from plan}
>
> Did all manual tests pass? (yes/no)

**If issues found:** Fix them before proceeding.

### Step 9: Commit Changes

Stage and commit with proper message:

```bash
# Stage all changes
git add -A

# Commit with structured message
git commit -m "$(cat <<'EOF'
Feature #{issue_number}: {short_description}

- {Component 1 summary}
- {Component 2 summary}
- Added tests for {what}

Implements #{issue_number}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
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

# Verify tests still pass
python -m pytest --tb=short
```

### Step 11: Session Complete

Output:
> ## Implementation Complete
>
> **Issue:** #{number} - {title}
>
> **Worktree:** `{worktree_dir}`
>
> **Branch:** `{branch_name}`
>
> **Components Created/Modified:**
> - Server: {module changes}
> - Client: {form changes}
> - Tests: {test files}
>
> **Tests:** All passing ({count} tests)
>
> **Commit:** `{commit_hash}`
>
> ---
>
> ### Remaining Steps:
> 1. **Database changes** (if any): Verify in Anvil IDE
> 2. **Form YAML** (if any): Create in Anvil IDE
> 3. **Create PR:**
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

### Follow the Plan's Phases
- Complete Data Layer before Server Layer
- Complete Server Layer before Client Layer
- Don't skip phases even if they seem simple

### Database Changes Require Anvil IDE
- List all table/column changes clearly
- Wait for user confirmation before proceeding
- Note migration scripts that need to run

### Form YAML Requires Anvil IDE
- Provide the YAML structure in comments
- User must create forms in IDE
- Then implement the Python code

### One Phase at a Time
- Complete each phase before moving on
- Test after each major component
- Don't bundle unrelated changes

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
| Plan not found | "Run @feature-planner {number} first" |
| Database changes not done | Wait for user to complete in Anvil IDE |
| Form doesn't exist | Note that form YAML must be created in Anvil IDE first |
| Tests fail after changes | Analyze and fix, or ask for help |
| File doesn't exist | Check path, may need to create |
| Merge conflict | "Branch has conflicts. Resolve before continuing." |

---

## Constraints

**MUST:**
- Read the entire plan before starting
- Confirm database changes are complete (if any)
- Follow the phased implementation approach
- Run tests before and after changes
- Commit all changes before ending session

**MUST NOT:**
- Skip the manual testing checkpoint
- Ignore database/schema prerequisites
- Leave forms without their YAML created in IDE
- Leave uncommitted changes

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@feature-planner` | **Prerequisite** - Must have a feature plan |
| `@create-pr` | **Next step** - Creates PR from this branch |
