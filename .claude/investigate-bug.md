# Bug Investigation Agent

Thoroughly investigate GitHub issue #$ARGUMENTS and prepare all context needed for `/fix-bug` to implement the solution.

## Phase 0: Validation & Setup

1. **Fetch the issue** from GitHub using `gh issue view $ARGUMENTS --json title,body,labels,comments,author,createdAt`

2. **Validate issue type** - Check if the issue has a `bug` label:
   - If YES: Continue with investigation
   - If NO: Stop and ask the user:
     > "This issue isn't labeled as a bug."
     >
     > Labels found: {list labels}
     >
     > The `/investigate-bug` command is designed for bug fixes. For new features or enhancements, consider using `/scope-issue` instead.
     >
     > How would you like to proceed?
     > 1. Add "bug" label and continue investigation
     > 2. Use /scope-issue instead (for features/enhancements)
     > 3. Continue investigation anyway

3. **Extract key information** from the issue:
   - Error messages and stack traces
   - Affected files/line numbers mentioned
   - Steps to reproduce (if provided)
   - Affected companies/users
   - Related issues mentioned

---

## Phase 1: Code Discovery

4. **Search for error locations** - Use stack traces and error messages to find:
   - Primary error location (file and line number)
   - All functions in the call stack
   - Related error handling code

5. **Read affected code** - Read each file involved:
   - The file where the error occurs
   - Files that call into the error location
   - Files that the error location calls
   - Any defensive/fallback handling that exists

6. **Map the code paths** - Trace how we get to the error:
   - Entry points (API endpoints, UI events, background tasks)
   - Data flow through the system
   - Conditions that trigger the error path

---

## Phase 2: Root Cause Analysis

7. **Identify the root cause** - Determine:
   - What is happening (the symptom)
   - Why it's happening (the cause)
   - When it happens (the conditions/triggers)
   - How often it happens (frequency/severity)

8. **Check for related occurrences** - Search for:
   - Similar error patterns elsewhere in the codebase
   - Related issues or previous fixes
   - Comments or TODOs about known issues

9. **Understand the impact**:
   - Which users/companies are affected
   - What functionality is broken
   - Is there data corruption or just UX issues
   - Is there a workaround

---

## Phase 3: Define Scope Boundaries

10. **Document what WILL be modified** - List specific:
    - Files that need changes
    - Functions that need updates
    - The nature of each change (fix, add handling, refactor)

11. **Document what WON'T be touched** - Explicitly list:
    - Fragile or complex systems to avoid
    - Related but out-of-scope areas
    - Architecture that should remain unchanged
    - **Why each item is excluded** (risk, complexity, not related)

    Example format:
    > ### What We Won't Touch
    > - **{System/Component}** - {Why it's excluded and what could break if we did touch it}

12. **Identify risks** if excluded areas were modified:
    - What could break
    - What testing would be required
    - Why it's not worth the risk for this fix

---

## Phase 4: Data Analysis (If Applicable)

13. **For data-related bugs**, investigate:
    - How many records are affected
    - Which companies/users have bad data
    - Can data be recovered or must it be reconstructed
    - What validation is needed before remediation

14. **For duplicate/integrity issues**, determine:
    - Which record should be kept (evaluation criteria)
    - What signals indicate "active use" (edits, linked records, attachments)
    - What should happen to the archived/removed records
    - Is manual review needed for any cases

---

## Phase 5: Plan the Fix

15. **Outline the proposed fix**:
    - Specific code changes needed
    - Order of operations
    - Any data remediation steps
    - Rollback plan if something goes wrong

16. **Define testing requirements**:
    - How to reproduce the original bug
    - How to verify the fix works
    - Regression tests needed
    - Edge cases to check

17. **Identify test data needs**:
    - Specific records/UUIDs to test with
    - Companies/environments to verify in
    - Mock data or conditions to create

---

## Phase 6: Document & Update Issue

18. **Create Investigation Report** with this structure:

```markdown
## Bug Investigation Report

### Issue Summary
- **Issue**: #{number} - {title}
- **Component**: {affected module/system}
- **Severity**: {Critical/High/Medium/Low}
- **Affected**: {companies/users impacted}

### Root Cause Analysis
**What's happening**: {symptom description}

**Why it's happening**: {root cause explanation}

**Trigger conditions**: {what causes it to occur}

### Affected Code (Will Be Modified)
- `{file_path}:{line}` - {what change is needed}
- `{file_path}:{line}` - {what change is needed}

### What We Won't Touch
- **{System/Component}** - {why excluded, what could break}
- **{System/Component}** - {why excluded, what could break}

### Proposed Fix
{Step-by-step description of the fix}

### Data Remediation (If Applicable)
- Records affected: {count}
- Remediation approach: {description}
- Evaluation criteria: {how to determine correct action per record}

### Testing Plan
**Reproduce Bug**:
- {steps to trigger original bug}

**Verify Fix**:
- {steps to confirm fix works}

**Regression Tests**:
- {related functionality to verify still works}

### Ready for /fix-bug
- [ ] Root cause identified
- [ ] Affected files documented
- [ ] Scope boundaries defined (what we won't touch)
- [ ] Fix approach outlined
- [ ] Testing plan defined
- [ ] Data remediation planned (if applicable)
```

19. **Post investigation to GitHub issue** as a comment:
    ```bash
    gh issue comment $ARGUMENTS --body "{investigation report}"
    ```

20. **Confirm readiness** - Tell the user:
    > Investigation complete for issue #{number}.
    >
    > The investigation report has been added to the GitHub issue.
    >
    > When you're ready to implement the fix, run:
    > `/fix-bug {issue_number}`

---

## Guidelines

- **Read before concluding** - Always read the actual code, don't assume from names
- **Be explicit about exclusions** - The "What We Won't Touch" section builds confidence
- **Consider data carefully** - For data bugs, understand what "correct" looks like before planning fixes
- **Check for patterns** - If a bug exists in one place, it may exist in similar code
- **Don't fix during investigation** - This command investigates only; `/fix-bug` implements
- **Update the issue** - Always post findings to GitHub so they're preserved
- **Ask when uncertain** - If scope boundaries are unclear, ask the user before proceeding
