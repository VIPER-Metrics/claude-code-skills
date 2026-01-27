# Create Hotfix Issue

Create a GitHub issue for a small tweak, improvement, or change that isn't a bug or a full feature.

**Usage**: `/create-hotfix {description}` or just `/create-hotfix` for guided mode

---

## Phase 0: Gather Requirements

1. **Check for description** in `$ARGUMENTS`:
   - If provided: Use as the starting point for the hotfix
   - If empty: Ask the user to describe the small change they want

2. **Ask clarifying questions** (if needed):
   - What specific behavior needs to change?
   - Which part of the app is affected (module/form/page)?
   - Is there a specific file or function you know needs updating?
   - What should happen after the change? (expected outcome)

3. **Determine scope** - Confirm this is a hotfix, not something larger:
   - **Hotfix**: Small, focused change (UI tweak, text change, minor logic adjustment, config update)
   - **Bug**: Something is broken/erroring → Suggest `/investigate-bug` instead
   - **Feature**: New functionality → Suggest `/create-feature` instead

   If unclear, ask: "This sounds like it could be a {bug/feature}. Would you like me to create a hotfix issue, or use the appropriate workflow for a {bug/feature}?"

---

## Phase 1: Codebase Investigation (Optional)

4. **Search for relevant code** (if user mentions specific area):
   - Find the affected files/components
   - Understand current implementation
   - Note any related code that might be affected

5. **Document affected areas**:
   - Primary file(s) that will likely need changes
   - Related files to be aware of (but likely won't change)

---

## Phase 2: Create the Issue

6. **Ensure hotfix label exists**:
   ```bash
   gh label list | grep -q "hotfix" || gh label create "hotfix" --description "Small tweak or improvement" --color "FFA500"
   ```

7. **Draft the issue** using this template:

```markdown
## Summary
{One-line description of the change}

## Current Behavior
{What happens now / what exists now}

## Desired Behavior
{What should happen after the change}

## Affected Area
- **Module**: {e.g., Inspections, Defects, Assets}
- **File(s)**: {if known, list likely files}

## Implementation Notes
{Any context gathered from codebase investigation}
{Or: "To be determined during implementation"}

## Acceptance Criteria
- [ ] {Specific, testable outcome 1}
- [ ] {Specific, testable outcome 2}
```

8. **Create the issue** on GitHub:
   ```bash
   gh issue create \
     --title "{concise title}" \
     --body "{issue body from template}" \
     --label "hotfix"
   ```

9. **Confirm to user**:
   > Hotfix issue created: #{issue_number}
   >
   > {issue URL}
   >
   > When you're ready to implement, you can:
   > - Work on it directly (it's a small change)
   > - Or run `/fix-bug {issue_number}` for structured workflow

---

## Guidelines

- **Keep it small** - Hotfixes are for quick wins, not architectural changes
- **Be specific** - Vague descriptions lead to scope creep
- **One change per issue** - If multiple changes are needed, create multiple issues
- **Don't over-investigate** - For small changes, minimal context is often enough
- **Use judgment on labels** - Add relevant module labels if they exist (e.g., "Inspections", "Defects")

---

## Examples of Good Hotfixes

- "Change button text from 'Submit' to 'Save Changes'"
- "Add loading spinner to asset search"
- "Update default sort order on defect list to newest first"
- "Remove deprecated field from inspection form"
- "Increase timeout for PDF export from 30s to 60s"

## Examples That Are NOT Hotfixes

- "Redesign the navigation menu" → Feature
- "Fix crash when opening inspections" → Bug
- "Add user authentication" → Feature
- "Something is broken but I don't know what" → Bug investigation
