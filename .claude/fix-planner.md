---
name: fix-planner
description: Generate an actionable implementation plan from a bug investigation report. Use when the user wants to plan a bug fix, create an implementation plan, prepare for fixing an issue, or says "plan fix", "create fix plan", "plan implementation", or "how should I fix issue #X". Requires an investigation report from @investigate-bug to exist on the issue first.
---

# Fix Planner Skill

Generate an actionable implementation plan from a bug investigation report.

## Usage

```
/fix-planner {issue_number}
```

## Description

This skill takes a GitHub issue number that has been investigated by `@investigate-bug` and creates a detailed, step-by-step implementation plan. It extracts the investigation context, generates specific code changes, testing strategies, and risk assessments.

## Workflow

### Step 1: Input Validation

Accept the issue number from `$ARGUMENTS`. If no argument provided, ask the user for the issue number.

Fetch the issue details:
```bash
gh issue view $ARGUMENTS --json title,body,labels,comments
```

Look for an investigation report in the comments (typically created by `@investigate-bug`). The investigation report should contain sections like:
- Root Cause Analysis
- Affected Files
- Scope/Boundaries
- Testing Requirements

**If no investigation report found:**
> No investigation report found for issue #{number}.
>
> Run `@investigate-bug {issue_number}` first to create an investigation report.

### Step 2: Extract Investigation Context

Parse the investigation report to extract:

1. **Root Cause Analysis** - What is actually causing the bug
2. **Affected Files and Line Numbers** - Specific locations that need modification
3. **In-Scope Changes** - What will be modified as part of this fix
4. **Out-of-Scope Boundaries** - What explicitly should NOT be touched
5. **Testing Requirements** - What needs to be tested
6. **Data Remediation Needs** - If there's corrupted/incorrect data to fix

### Step 3: Generate Implementation Plan

Create the plan with this exact structure:

---

```markdown
# Fix Plan: Issue #{issue_number}

**Issue Title:** {title}
**Created:** {date}
**Investigation:** {link to investigation comment}

## Summary

{Brief 2-3 sentence summary of what this fix will do and why}

---

## Pre-Implementation Checklist

- [ ] Create feature branch: `fix/issue-{number}-{short-description}`
- [ ] Verify current test suite passes: `python -m pytest` or appropriate command
- [ ] Backup affected data (if data remediation involved)
- [ ] Review investigation report thoroughly
- [ ] Confirm understanding of root cause

---

## Implementation Steps

### Change 1: {Brief description}

**File:** `{file_path}`
**Lines:** {start_line}-{end_line}

**Current Code:**
```python
{existing code snippet}
```

**Proposed Change:**
```python
{new code snippet}
```

**Why This Fixes It:**
{Explanation tying back to root cause - e.g., "The root cause is X, and this change addresses it by Y"}

**Edge Cases to Handle:**
- {edge case 1}
- {edge case 2}

---

### Change 2: {Brief description}
{Repeat structure for each file/change}

---

## Testing Strategy

### Unit Tests to Add/Modify

| Test File | Test Name | Purpose |
|-----------|-----------|---------|
| `{test_file}` | `test_{name}` | {what it verifies} |

**Test Code:**
```python
def test_{name}():
    """Test that {description}"""
    # Arrange
    {setup}

    # Act
    {action}

    # Assert
    {verification}
```

### Integration Tests

- [ ] {Integration scenario 1}
- [ ] {Integration scenario 2}

### Manual Testing Steps

1. **Setup:** {how to prepare the test environment}
2. **Reproduce Original Bug:**
   - {step 1}
   - {step 2}
   - Expected (before fix): {buggy behavior}
3. **Verify Fix:**
   - {step 1}
   - {step 2}
   - Expected (after fix): {correct behavior}

### Regression Verification

Check that these existing features still work:
- [ ] {feature 1 that could be affected}
- [ ] {feature 2 that could be affected}

---

## Data Remediation (if applicable)

### Script Location
`scripts/remediation/fix_{issue_number}_remediation.py`

### Records to Process
- **Count:** {estimated number of affected records}
- **Criteria:** {SQL/query to identify affected records}
- **Table(s):** {database tables involved}

### Remediation Script
```python
"""
Remediation script for Issue #{issue_number}
Run with: python scripts/remediation/fix_{issue_number}_remediation.py --dry-run
"""

def find_affected_records():
    """Identify records needing remediation"""
    pass

def remediate_record(record):
    """Fix a single record"""
    pass

def validate_remediation(record):
    """Verify the fix was applied correctly"""
    pass

def main(dry_run=True):
    records = find_affected_records()
    print(f"Found {len(records)} records to remediate")

    if dry_run:
        print("DRY RUN - no changes made")
        return

    for record in records:
        remediate_record(record)
        validate_remediation(record)
```

### Validation Checks
- [ ] Record count matches expected
- [ ] Spot-check {n} records manually
- [ ] Run validation query: `{query}`

### Rollback Plan
```sql
-- Rollback query (if needed)
{rollback SQL}
```

---

## Code Review Checklist

- [ ] All modified files are listed in scope from investigation
- [ ] No out-of-scope boundaries violated
- [ ] Tests cover the primary fix
- [ ] Tests cover identified edge cases
- [ ] Error handling is appropriate
- [ ] Logging is adequate for debugging
- [ ] Documentation updated (if public API changed)
- [ ] No new security vulnerabilities introduced
- [ ] Follows VIPER Metrics coding standards
- [ ] Database migrations included (if schema changes)

---

## Risk Assessment

### Dependencies That Might Break
| Dependency | Risk Level | Mitigation |
|------------|------------|------------|
| {component} | {Low/Medium/High} | {how to address} |

### Performance Implications
- {Any performance considerations}
- {Database query impact}
- {Memory/CPU concerns}

### Deployment Considerations
- [ ] {deployment step 1}
- [ ] {deployment step 2}
- [ ] {any feature flags needed}

### Monitoring/Alerting Needs
- {What to monitor after deployment}
- {Alert thresholds to set}

---

## Effort Estimate

| Task | Hours |
|------|-------|
| Code changes | {hours} |
| Unit tests | {hours} |
| Integration tests | {hours} |
| Manual testing | {hours} |
| Code review | {hours} |
| Data remediation | {hours, or N/A} |
| Documentation | {hours, or N/A} |
| **Total** | **{total hours}** |

---

## Next Steps

1. Review this plan and request changes if needed
2. When approved, run: `@implement-fix {issue_number}`
3. Create PR and request code review
4. Run data remediation (if applicable) after code deployment
```

---

### Step 4: Risk Assessment

Analyze the proposed changes for:

1. **Breaking Dependencies**
   - What other code calls the modified functions?
   - Are there API contracts that might change?
   - External integrations affected?

2. **Performance Impact**
   - Will this add database queries?
   - Any loops that could be expensive?
   - Memory usage concerns?

3. **Deployment Risks**
   - Does this need a database migration?
   - Feature flags recommended?
   - Blue/green deployment needed?

4. **Monitoring Needs**
   - What metrics should we watch post-deployment?
   - Any new alerts to configure?

### Step 5: Estimate Effort

Provide realistic time estimates based on:
- Complexity of changes
- Number of files affected
- Testing requirements
- Data remediation scope

Be conservative - it's better to over-estimate than under-estimate.

### Step 6: Save the Plan

Create the docs directory if it doesn't exist:
```bash
mkdir -p docs/fix-plans
```

Save the plan:
```bash
# The plan should be saved to: docs/fix-plans/FIX-{issue-number}-plan.md
```

### Step 7: Post to GitHub

Add the plan as a comment on the issue:
```bash
gh issue comment $ARGUMENTS --body-file docs/fix-plans/FIX-$ARGUMENTS-plan.md
```

### Step 8: Add Label

Mark the issue as ready for implementation:
```bash
gh issue edit $ARGUMENTS --add-label "ready-to-implement"
```

### Step 9: Confirm to User

Output:
> ## Fix Plan Created
>
> **Issue:** #{number} - {title}
>
> **Plan saved to:** `docs/fix-plans/FIX-{number}-plan.md`
>
> **Posted to:** GitHub issue as comment
>
> ---
>
> ### Review the plan and when approved, run:
> ```
> @implement-fix {issue_number}
> ```

---

## Guidelines

### Be Specific
- Always include exact line numbers
- Show actual code snippets, not descriptions
- Name specific test files and functions

### Call Out Risks
- Don't hide potential problems
- Rate risks as Low/Medium/High
- Provide mitigation strategies

### Handle Incomplete Investigations
If the investigation report is missing key information:
- List what's missing
- Ask the user for clarification
- Don't guess at root causes or affected files

### Complex Fixes
For fixes that span multiple files or systems:
- Break into numbered phases
- Add checkpoints between phases
- Consider feature flags for gradual rollout

### Data Changes
For any fix involving data:
- Always include rollback steps
- Require dry-run capability in scripts
- Include validation queries

### Tie Back to Root Cause
Every proposed change should clearly explain how it addresses the identified root cause. If a change can't be tied back, question whether it belongs in this fix.

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@investigate-bug` | **Prerequisite** - Must run first to create investigation report |
| `@implement-fix` | **Next step** - Executes this plan |
| VIPER Metrics Standards | **Reference** - Follow coding conventions |

---

## Example Output

```
## Fix Plan Created

**Issue:** #142 - Error when downloading inspection images

**Plan saved to:** `docs/fix-plans/FIX-142-plan.md`

**Posted to:** GitHub issue as comment

---

### Review the plan and when approved, run:
```
@implement-fix 142
```
```
