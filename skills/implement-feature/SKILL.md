---
name: implement-feature
description: Execute a feature implementation based on an approved feature plan. Use when the user wants to implement a feature, execute a feature plan, build a new feature, or says "implement feature", "build feature", "make the feature for issue #X". Requires a feature plan from /feature-planner to exist first.
---

# Implement Feature

Execute code changes based on an approved feature plan using git worktrees for isolated development.

## Usage

```
/implement-feature {issue_number}
```

## Workflow

### Step 1: Load Feature Plan

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

Look for the feature plan at `wiki/issues/$ARGUMENTS/feature-plan.md`:
```bash
# Load the feature plan from wiki
cat wiki/issues/$ARGUMENTS/feature-plan.md
```

**If no plan found:**
> No feature plan found for issue #{number}.
>
> Run `/feature-planner {issue_number}` first to create a feature plan.

### Step 2: Create Git Worktree

Use git worktrees to enable parallel development on multiple branches.

**IMPORTANT:** Always branch from `master` (staging), not `published` (production).

```bash
# Get short description from issue title
ISSUE_NUM=$ARGUMENTS
TITLE=$(gh issue view $ISSUE_NUM --json title --jq '.title' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g' | cut -c1-30)
BRANCH_NAME="feature-${ISSUE_NUM}-${TITLE}"
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

**Branch naming convention:** `feature-{issue_number}-{short-description}`
- No slashes (Anvil restriction)
- Lowercase with hyphens
- Max 50 characters total

### Step 3: Check for Database Changes

Review the plan's "Data Model Changes" section.

**If database changes are required:**
> **Database Changes Required**
>
> The following changes must be made in the Anvil IDE before proceeding:
>
> | Table | Change |
> |-------|--------|
> | {table} | {change description} |
>
> Please confirm these changes have been made in Anvil, or type "skip" to proceed without them.

Wait for user confirmation before continuing.

### Step 4: Validate Prerequisites

Check the pre-implementation checklist from the plan:

```bash
# Verify we're in the correct worktree
pwd
git branch --show-current

# Confirm clean state
git status
```

### Step 5: Execute Implementation Phases

Follow the plan's phased implementation:

#### Phase 1: Data Layer (if applicable)

**Note:** Most data layer changes require Anvil IDE. For code-based changes:

1. **Create data access functions** in the appropriate OTS module
2. **Add any data validation** logic
3. **Create migration scripts** (for manual execution later)

```bash
# If migration script needed
mkdir -p scripts/migrations
# Write script to: scripts/migrations/feature_{issue_number}_migration.py
```

**DO NOT run migration scripts** - just create them for manual execution.

#### Phase 2: Server Layer

For each server function in the plan:

1. **Read the target module:**
   - Verify the file exists
   - Check for any conflicts with existing code

2. **Add new functions:**
   - Follow the exact function signatures from the plan
   - Include all decorators (`@anvil.server.callable`, `@authorisation_required`, etc.)
   - Handle edge cases as specified

3. **Verify the changes:**
   - Re-read the file to confirm changes applied correctly

```python
# Standard VIPER server function pattern
@anvil.server.callable
@authorisation_required("{Permission Name}")
@track_server_function
def {function_name}({parameters}):
    """Docstring explaining purpose"""
    # Implementation
    pass
```

#### Phase 3: Client Layer

For each form/component in the plan:

1. **Create new form files** if specified:
   - `__init__.py` for form code
   - Form YAML must be created in Anvil IDE

2. **Modify existing forms:**
   - Read the target file first
   - Apply only the specific changes from the plan
   - Preserve existing functionality

3. **Add event handlers:**
   - Wire up button clicks, data bindings, etc.
   - Follow the user flow from the plan

**Note for new forms:**
> The form YAML structure must be created in Anvil IDE. The Python code can be added here.

#### Phase 4: Integration

1. **Connect to navigation:**
   - Add links/buttons to access the new feature
   - Update menu items if needed

2. **Wire up permissions:**
   - Ensure proper permission checks are in place
   - Test with appropriate user roles

3. **Connect components:**
   - Link forms together
   - Set up data flow between components

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
tags: [testing, feature]
---

# Test Plan: Issue #{issue_number}

**Issue:** #{issue_number} - {title}
**Branch:** `{branch_name}`
**Worktree:** `{worktree_path}`

---

## Feature Overview

{Brief description of what the feature does}

---

## Acceptance Criteria Verification

| Criterion | Test Steps | Expected Result | Status |
|-----------|------------|-----------------|--------|
| {criterion 1} | {how to test} | {expected} | ⬜ |
| {criterion 2} | {how to test} | {expected} | ⬜ |
| {criterion 3} | {how to test} | {expected} | ⬜ |

---

## Use Case Testing

### Use Case 1: {name}
**Steps:**
1. {step 1}
2. {step 2}
3. {step 3}

**Expected Result:** {what should happen}
**Status:** ⬜

### Use Case 2: {name}
**Steps:**
1. {step 1}
2. {step 2}

**Expected Result:** {what should happen}
**Status:** ⬜

---

## Edge Cases

| Scenario | Test Steps | Expected Result | Status |
|----------|------------|-----------------|--------|
| {edge case 1} | {how to test} | {expected} | ⬜ |
| {edge case 2} | {how to test} | {expected} | ⬜ |

---

## Permission Testing

| Permission | User Role | Expected Behavior | Status |
|------------|-----------|-------------------|--------|
| {permission} | {role with} | Can access feature | ⬜ |
| {permission} | {role without} | Cannot access feature | ⬜ |

---

## Integration Testing

| Integration Point | Test Steps | Expected Result | Status |
|-------------------|------------|-----------------|--------|
| {component 1} | {how to test} | {expected} | ⬜ |
| {component 2} | {how to test} | {expected} | ⬜ |

---

## Regression Tests

Check that these existing features still work:

| Feature | Test Steps | Expected Result | Status |
|---------|------------|-----------------|--------|
| {feature 1} | {how to test} | {expected} | ⬜ |
| {feature 2} | {how to test} | {expected} | ⬜ |

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

- [ ] All acceptance criteria verified
- [ ] Use cases tested
- [ ] Edge cases tested
- [ ] Permissions working correctly
- [ ] Integration points verified
- [ ] Regression tests passed
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

### Step 8: Commit Changes

Stage and commit with proper message:

```bash
# Stage all changes
git add -A

# Commit with structured message
git commit -m "$(cat <<'EOF'
Feature #{issue_number}: {short_description}

- {Component 1}: {what was added}
- {Component 2}: {what was added}
- Added tests for {what}

Implements #{issue_number}

Co-Authored-By: Claude <noreply@anthropic.com>
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

# Confirm branch and worktree
git branch --show-current
pwd
```

### Step 10: Session Complete

Output:
> ## Feature Implementation Complete
>
> **Issue:** #{number} - {title}
>
> **Branch:** `{branch_name}` (from `master`)
>
> **Worktree:** `{worktree_path}`
>
> **Changes:**
> - {file1}: {what was added}
> - {file2}: {what was added}
>
> **Commit:** `{commit_hash}`
>
> **Test Plan:** `wiki/issues/{number}/test-plan.md` (also posted to GitHub issue)
>
> ---
>
> ### Remaining Manual Steps:
> {List any database changes, form YAML, or other Anvil IDE tasks}
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
- Work on multiple features simultaneously
- Each feature is isolated in its own directory
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
~/GitHub/viper-metrics-v2-0/                    # Main repo - stays on `published`
~/GitHub/viper-metrics-worktrees/
├── 123-login-error/                            # Worktree for fix issue #123
├── 789-bulk-export/                            # Worktree for feature issue #789
└── {issue}-{short-name}/                       # Pattern for new worktrees
```

---

## Branch Strategy

```
published (production)
    │
    └── master (staging) ◄── Branch features from here
            │
            └── feature-789-bulk-export ◄── Your feature branch
```

**Why master?**
- `master` is the staging branch where features are tested
- `published` is production - never branch directly from it
- Features go: `feature branch` → `master` (staging) → `published` (production)

---

## Guidelines

### Follow the Plan Exactly
- Don't improvise or add extra features
- Don't "improve" code outside the plan's scope
- If the plan is wrong, stop and update it first

### Respect Anvil Constraints
- Database table changes → Anvil IDE
- Form YAML creation → Anvil IDE
- Code files → Can be edited here
- No slashes in branch names

### Phase by Phase
- Complete each phase before moving to the next
- Data layer must be ready before server layer
- Server layer must be ready before client layer

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
| Plan not found | "Run /feature-planner {number} first" |
| Database changes pending | List changes and wait for confirmation |
| File doesn't exist | Create it if it's a new file per plan, otherwise STOP |
| Worktree already exists | Navigate to existing worktree and continue |
| Branch already exists | Use existing branch for worktree |
| Form YAML needed | Note: "Create form YAML in Anvil IDE: {details}" |

---

## Constraints

**MUST:**
- Read the plan before making any changes
- Branch from `master` (staging), not `published`
- Use worktrees for branch isolation
- Use simple branch names (no slashes)
- Check for database changes before coding
- Create and post test plan to GitHub
- Commit all changes before ending session
- List any manual Anvil IDE tasks

**MUST NOT:**
- Modify files outside the plan's scope
- Skip database change confirmation
- Create branch from `published`
- Use slashes in branch names
- Leave uncommitted changes
- Run migration scripts (manual step)
- Work directly on published/master branch

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/feature-planner` | **Prerequisite** - Must have a feature plan |
| `/create-pr` | **Next step** - Creates PR from this branch |

---

## Wiki Structure

After implementation, the wiki should contain:
```
wiki/issues/$ARGUMENTS/
├── feature-plan.md    # From /feature-planner
└── test-plan.md       # From /implement-feature (this skill)
```

---

## Example Session

```
> /implement-feature 789

Loading feature plan for issue #789...

**Database Changes Required**

The following changes must be made in the Anvil IDE:

| Table | Change |
|-------|--------|
| reports | Add column `export_format` (text) |

Please confirm these changes have been made, or type "skip".

> done

Creating worktree from master...
Branch: feature-789-bulk-export-reports
Worktree: ~/GitHub/viper-metrics-worktrees/789-bulk-export-reports

Implementing Phase 2: Server Layer...
- Created: server_code/ReportsOTS/BulkExport.py
- Added: bulk_export_reports() function

Implementing Phase 3: Client Layer...
- Modified: client_code/Reports/ReportList/__init__.py
- Added: Export button and handler

Creating test plan...
Saved to: wiki/issues/789/test-plan.md
Posted to GitHub issue #789

## Feature Implementation Complete

**Issue:** #789 - Add bulk export for reports
**Branch:** `feature-789-bulk-export-reports`
**Worktree:** `~/GitHub/viper-metrics-worktrees/789-bulk-export-reports`

### Remaining Manual Steps:
- [ ] Create form YAML for ExportDialog in Anvil IDE

### Next steps:
1. Run manual tests from the test plan
2. When verified, run: `/create-pr 789`
```
