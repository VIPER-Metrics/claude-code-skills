# Bug Fixer Agent

Investigate and fix GitHub issue #$ARGUMENTS

## Phase 0: Triage & Branch Setup

1. **Fetch the issue** from GitHub using `gh issue view $ARGUMENTS`

2. **Check for existing investigation** - Look for a "Bug Investigation Report" in the issue comments:
   - If found: Use the investigation as your guide - it contains root cause, affected files, scope boundaries, and testing plan
   - If not found: You'll do investigation in Phase 1 (consider suggesting `/investigate-bug` first for complex issues)
   - The investigation's "What We Won't Touch" section defines strict boundaries - respect them

3. **Create isolation branch immediately**:
   - Determine base branch: Run `git remote show origin | grep 'HEAD branch'` to find the default branch (usually `published` for Anvil apps)
   - If that fails, check if `origin/published` exists with `git branch -r | grep origin/published`
   - Use `published` if it exists, otherwise fall back to `master`
   - `git checkout {base_branch} && git pull origin {base_branch}`
   - `git checkout -b fix-{issue_number}-{short-description}`
   - This isolates your work from other changes during investigation

4. **Quick assessment** - Classify the bug:
   - **Trivial**: Typo, missing null check, obvious one-liner → Skip to streamlined flow
   - **Standard**: Clear bug with known scope → Full workflow
   - **Complex**: Architectural issue, unclear cause, multiple systems → Full workflow + extra investigation (or suggest `/investigate-bug` first)

5. **For TRIVIAL bugs only** - Use streamlined flow:
   - Read affected file, implement fix, commit, PR
   - Skip detailed analysis phases
   - Still run code-reviewer agent for security check

6. **For Standard/Complex bugs** - Continue to Phase 1

---

## Phase 1: Investigation

6. **Check for related issues** mentioned in the issue (duplicates, similar issues)
7. **Parse the stack trace** to identify affected files and line numbers
8. **Read the relevant code files** mentioned in the stack trace
9. **Investigate root cause** - understand why the error occurs

## Phase 2: Analysis

10. **Summarize findings** including:
    - What triggers the error
    - Root cause hypothesis
    - Affected code paths
11. **Propose a fix** - describe the minimal change needed
12. **Identify potential side effects** - what else might this change affect?

## Phase 3: Human Review Checkpoint (HOLD POINT)

13. **STOP AND PRESENT PLAN FOR REVIEW** - Before writing any code, present to the user:
    - Summary of the proposed fix
    - List of files that will be modified
    - Specific code changes planned (pseudocode or description)
    - Any data remediation needed
    - Potential risks or concerns

    **Ask explicitly**: "Here is my proposed fix. Please review and let me know if you'd like any changes before I implement it."

    **Wait for user approval before proceeding to implementation.**

14. **Implement the fix** with minimal, focused changes (branch was created in Phase 0)

## Phase 4: Testing & Verification

15. **Document reproduction steps** - How to trigger the original bug:
    - What URL/route to navigate to
    - What data conditions are required (e.g., missing record, null field)
    - What user state is needed (permissions, company, session)

16. **Verify the fix** - Confirm the fix addresses the root cause:
    - Trace through the code path with the fix applied
    - Confirm the error condition is now handled
    - Check that the user experience is appropriate (error message, redirect, etc.)

17. **Check for regressions** - Ensure normal functionality still works:
    - Test the happy path (valid data, normal conditions)
    - Test related functionality that shares the same code
    - Look for other callers of modified functions

18. **Identify edge cases** to include in test plan:
    - Null/undefined values
    - Empty collections
    - Permission boundaries
    - Concurrent access scenarios

19. **Create test plan checklist** for PR:
    ```
    - [ ] Bug scenario: {describe how to reproduce and verify fix}
    - [ ] Happy path: {describe normal usage that should still work}
    - [ ] Edge case: {describe edge cases to verify}
    ```

20. **Commit changes** with message format:
    ```
    Fix: {short description}

    {detailed explanation}

    Fixes #{issue_number}
    ```

## Phase 5: Agent Review

21. **Determine if specialist agent review is needed** based on the fix type:
    - **anvil-client-yaml-specialist**: If fix involves YAML form definitions, UI components, data bindings, or event handlers
    - **anvil-backend-specialist**: If fix involves server modules, database queries, server functions, or security controls
    - **maintenance-planner**: If fix affects maintenance workflows or user experience patterns
22. **Run appropriate agent(s)** to review the changes if applicable
23. **Incorporate agent feedback** into the fix if needed

## Phase 6: Delivery

24. **Push branch** and **create PR** with:
    - Summary of changes
    - Root cause explanation
    - Test plan checklist
    - Link to the issue
    - Note which agents reviewed the fix (if any)
25. **Comment on the issue** with investigation summary and PR link

## Guidelines

- **ALWAYS stop at Phase 3 for human review** - Never implement code changes without explicit user approval
- Keep fixes minimal and focused - don't refactor surrounding code
- Always read the code before proposing changes
- Check for similar patterns elsewhere that might need the same fix
- Consider edge cases and error handling
- Test plan should cover the bug scenario and regression cases
- Use specialist agents for complex changes in their domain
- **Always run code-reviewer agent** after implementation, even for trivial fixes
- **Respect investigation boundaries** - If an investigation report exists, the "What We Won't Touch" section defines strict scope boundaries. Do not modify excluded systems/components without explicit user approval.
- **For complex bugs** - Consider running `/investigate-bug` first to thoroughly analyze root cause and define scope before implementing fixes
