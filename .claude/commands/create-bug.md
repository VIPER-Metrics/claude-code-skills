# Create Bug Issue

Guide the user through creating a well-documented bug report as a GitHub issue.

**Usage**: `/create-bug {brief description}` or just `/create-bug` for guided mode

---

## Phase 0: Initial Context

1. **Check for description** in `$ARGUMENTS`:
   - If provided: Use as the starting point
   - If empty: Ask "What bug or issue are you experiencing?"

2. **Confirm this is a bug**, not something else:
   - **Bug**: Something is broken, erroring, or behaving incorrectly
   - **Hotfix**: Small tweak that isn't broken → Suggest `/create-hotfix`
   - **Feature**: New functionality → Suggest `/create-feature`

   If unclear, ask: "Is this something that's broken/erroring, or is it a change request?"

---

## Phase 1: Gather Bug Details

3. **Ask about the component**:
   > "Which part of the app is affected?"
   > (e.g., Inspections, Defects, Assets, ServiceBoard, Reports, etc.)

4. **Ask about current behavior**:
   > "What is happening now? (the incorrect behavior)"

   Probe for specifics:
   - Is there an error message?
   - Does it crash, hang, or show wrong data?
   - Is it a UI issue or a data issue?

5. **Ask about expected behavior**:
   > "What should happen instead? (the correct behavior)"

6. **Ask about reproduction**:
   > "How do you trigger this bug?"

   Get step-by-step if possible:
   - What page/form are you on?
   - What action triggers it?
   - Does it happen every time or intermittently?
   - Any specific data conditions (certain asset, user, company)?

7. **Ask about impact**:
   > "How severe is this?"
   - **Critical**: App unusable, data loss, security issue
   - **High**: Major feature broken, blocking work
   - **Medium**: Feature partially broken, has workaround
   - **Low**: Minor annoyance, cosmetic issue

8. **Ask for additional context**:
   > "Any other details? (error messages, screenshots, session links, affected users)"

---

## Phase 2: Codebase Investigation (Optional)

9. **If user mentions specific files or areas**, investigate:
   - Search for the affected code
   - Find related error handling
   - Note file paths and line numbers

10. **Look for patterns**:
    - Has this been reported before? Check existing issues
    - Are there similar bugs in related code?

---

## Phase 3: Create the Issue

11. **Ensure bug label exists**:
    ```bash
    gh label list | grep -q "^bug" || echo "bug label should exist"
    ```

12. **Draft the issue** using this template:

```markdown
## Type
Bug 🐛

## Component
{Module/Form name}
- `{file_path}` - {brief description if known}

## Description
{Clear summary of the bug}

## Current Behavior
{What happens now - the problem}

## Expected Behavior
{What should happen - the correct behavior}

## Steps to Reproduce
1. {Step 1}
2. {Step 2}
3. {Step 3}

## Error Messages/Logs
{If applicable - paste error messages, stack traces, or link to session logs}

## Environment
- **Affected users/companies**: {if known}
- **Frequency**: {Always / Sometimes / Rare}
- **Workaround**: {if any}

## Additional Context
{Screenshots, session links, related issues, etc.}

## Priority
{Critical/High/Medium/Low} - {brief justification}

---
*Created via /create-bug command*
```

13. **Create the issue** on GitHub:
    ```bash
    gh issue create \
      --title "Bug: {concise title}" \
      --body "{issue body from template}" \
      --label "bug"
    ```

14. **Add priority label** if appropriate:
    - Critical bugs: Also add `priority: critical` or similar if it exists

---

## Phase 4: Confirm & Next Steps

15. **Show the result**:
    > Bug issue created: #{issue_number}
    >
    > {issue URL}
    >
    > **Next steps:**
    > - `/investigate-bug {issue_number}` - Deep investigation to find root cause
    > - `/fix-bug {issue_number}` - Go straight to fixing (for simpler bugs)

---

## Guidelines

- **Be specific** - Vague bug reports lead to wasted investigation time
- **Get reproduction steps** - "It doesn't work" isn't actionable
- **Note the environment** - Which users, companies, browsers are affected
- **Link related issues** - Check if this is a duplicate or related to existing issues
- **Don't investigate too deeply** - This skill creates the issue; `/investigate-bug` does deep analysis

---

## Question Flow Summary

| # | Question | Purpose |
|---|----------|---------|
| 1 | What's the bug? | Initial context |
| 2 | Which component? | Categorization |
| 3 | Current behavior? | The problem |
| 4 | Expected behavior? | The goal |
| 5 | How to reproduce? | Actionability |
| 6 | Severity? | Prioritization |
| 7 | Other details? | Context |
