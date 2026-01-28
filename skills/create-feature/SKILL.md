---
name: create-feature
description: Create a well-structured GitHub feature request through guided discovery. Use when the user has a feature idea and wants to create a GitHub issue, or says "create feature", "new feature", "I want to add...", "create issue for feature", or "help me spec out a feature". Investigates the codebase, asks clarifying questions, and creates a comprehensive feature issue.
---

# Create Feature

Transform a feature idea into a well-structured GitHub issue through guided investigation and discovery.

## Usage

```
/create-feature {brief feature description}
```

Or just:
```
/create-feature
```

## Description

This skill helps you go from a rough feature idea to a comprehensive, well-documented GitHub issue. It:

1. **Takes your initial idea** - Even a rough description works
2. **Investigates the codebase** - Finds related code, patterns, and potential integration points
3. **Asks clarifying questions** - Helps you think through edge cases and requirements
4. **Creates a GitHub issue** - With proper structure, labels, and technical context

## Workflow

### Phase 1: Initial Input

Accept the feature idea from `$ARGUMENTS`. If no argument provided, ask the user:

> What feature would you like to create? Give me a brief description - it doesn't need to be perfect, I'll help you refine it.

Store the initial description for later use.

### Phase 2: Codebase Investigation

Before asking questions, investigate the codebase to understand context:

#### 2.1 Find Related Code

Search for functionality similar to or related to the proposed feature:

```bash
# Search for related keywords
grep -rn "relevant_keyword" --include="*.py" | head -20

# Find similar patterns
grep -rn "similar_feature" --include="*.py" | head -20
```

#### 2.2 Identify Integration Points

Determine where this feature might fit:

- **Existing modules** - Which OTS module would this belong in?
- **UI location** - Where would users access this feature?
- **Data model** - What tables might be involved?
- **Related features** - What existing features does this interact with?

#### 2.3 Check for Prior Work

Look for any existing attempts or related issues:

```bash
# Check for related issues
gh issue list --search "related_keyword" --state all --limit 5

# Check for related code comments or TODOs
grep -rn "TODO.*related_keyword" --include="*.py" | head -10
```

### Phase 3: Follow-Up Questions

Based on investigation findings, ask clarifying questions to refine the feature. Use the AskUserQuestion tool for structured questions.

**Always ask these categories:**

#### 3.1 User Story / Motivation

> **Who needs this feature and why?**
> - Who is the primary user? (Operator, Admin, etc.)
> - What problem does this solve?
> - What's the business value?

#### 3.2 Acceptance Criteria

> **How will we know this feature is complete?**
> Based on my investigation, I found [related patterns]. Would you like to:
> - Option A: {approach similar to existing feature}
> - Option B: {different approach}
> - Option C: Let me describe my requirements

#### 3.3 Scope Definition

> **What should be included and excluded?**
> - Must-have functionality
> - Nice-to-have (can defer to future)
> - Explicitly out of scope

#### 3.4 Edge Cases

Based on codebase investigation, ask about specific edge cases:

> **I noticed [existing pattern]. How should this feature handle:**
> - {edge case 1 discovered during investigation}
> - {edge case 2 discovered during investigation}

#### 3.5 Technical Context (if relevant)

Ask about any technical decisions that emerged from investigation:

> **I found that [related feature] uses [pattern]. Should we:**
> - Follow the same pattern?
> - Try a different approach? (specify)

### Phase 4: Synthesize Requirements

Compile all gathered information into a structured format:

1. **Feature title** - Clear, concise, action-oriented
2. **User story** - As a [user], I want [feature] so that [benefit]
3. **Acceptance criteria** - Specific, testable requirements
4. **Use cases** - Concrete scenarios
5. **Technical context** - Relevant code findings
6. **Out of scope** - What this feature intentionally excludes
7. **Mockups/sketches** - If UI related, suggest sketching the flow

### Phase 5: Generate Issue

Create the GitHub issue with this structure:

```markdown
## User Story

As a **{user_role}**, I want to **{action}** so that **{benefit}**.

## Background / Motivation

{Why is this feature needed? What problem does it solve?}

{Include any relevant context from issue discussion or user feedback}

## Acceptance Criteria

- [ ] {Criterion 1 - specific and testable}
- [ ] {Criterion 2 - specific and testable}
- [ ] {Criterion 3 - specific and testable}

## Use Cases

### Use Case 1: {Name}
**Given** {precondition}
**When** {action}
**Then** {expected result}

### Use Case 2: {Name}
**Given** {precondition}
**When** {action}
**Then** {expected result}

## Technical Context

**Related code:**
- `{file_path}` - {how it relates}
- `{file_path}` - {how it relates}

**Potential integration points:**
- {module/system 1}
- {module/system 2}

**Existing patterns to follow:**
- {pattern 1 from investigation}

## UI/UX Considerations

{If applicable}
- Where does this fit in navigation?
- What's the user flow?
- Any mockups or wireframes?

## Out of Scope

The following are explicitly NOT part of this feature:
- {Item 1 - why excluded}
- {Item 2 - consider for future issue}

## Open Questions

{Any unresolved questions to discuss}

## Dependencies

- {Any features or work this depends on}
- {Any features that depend on this}
```

### Phase 6: Create the Issue

Present the draft to the user for review:

> ## Draft Feature Issue
>
> **Title:** {title}
>
> {Full issue body}
>
> ---
>
> Does this look good? I can:
> 1. **Create the issue** as-is
> 2. **Modify** specific sections
> 3. **Add more detail** to any area

Once approved, create the issue:

```bash
gh issue create \
  --title "{title}" \
  --body "{body}" \
  --label "enhancement"
```

### Phase 7: Confirm and Next Steps

Output after successful creation:

> ## Feature Issue Created
>
> **Issue:** #{number} - {title}
> **Link:** {github_issue_url}
>
> ---
>
> ### Next steps:
>
> **When ready to implement, run:**
> ```
> /feature-planner {issue_number}
> ```
>
> **To see all open features:**
> ```
> /issue-triage
> ```

---

## Question Templates

Use these question patterns based on feature type:

### For UI Features

- Where in the app should this live? (Navigation, existing page, new page?)
- Who needs to see/use this? (What permissions?)
- What data should be displayed?
- What actions can users take?

### For API/Backend Features

- What inputs does this need?
- What outputs/responses?
- What errors should it handle?
- What permissions are required?

### For Reporting Features

- What data should be included?
- What filters/parameters?
- What export formats?
- Who should have access?

### For Integration Features

- What external system?
- What data flows in/out?
- How should errors be handled?
- What's the sync frequency?

---

## Guidelines

### Ask Focused Questions

- Don't overwhelm with too many questions at once
- Group related questions together
- Provide context from your investigation to help answers
- Offer options when you've found relevant patterns

### Scope Appropriately

- Features should be completable in a reasonable timeframe
- If too large, suggest breaking into multiple issues
- Identify MVP vs. future enhancements

### Include Technical Context

- Reference specific files and patterns you found
- This helps whoever implements the feature
- Don't over-specify implementation details (that's for planning phase)

### Make It Actionable

- Acceptance criteria should be testable
- Use cases should be specific scenarios
- Avoid vague requirements like "should be fast"

---

## Error Handling

| Scenario | Action |
|----------|--------|
| User provides very vague input | Ask for clarification with examples |
| No related code found | Proceed but note this is a new area |
| Similar issue already exists | Show the existing issue and ask if this is related |
| Feature seems very large | Suggest breaking into phases/multiple issues |
| User unsure about requirements | Provide options based on investigation |

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@issue-triage` | **Alternative start** - May reveal needs before creating |
| `@feature-planner` | **Next step** - Creates implementation plan from this issue |
| `@implement-feature` | **After planning** - Executes the implementation |
| `@create-pr` | **Final step** - Creates pull request |

---

## Complete Workflow

```
/create-feature "Add bulk export for assets"
    ↓ Investigates codebase
    ↓ Asks clarifying questions
    ↓ Creates issue #156
/feature-planner 156
    ↓ Creates implementation plan
/implement-feature 156
    ↓ Writes the code
/create-pr 156
    ↓ Opens PR for review
```

---

## Example Session

**User:** `/create-feature add ability to bulk archive assets`

**Assistant:**
> Let me investigate the codebase to understand the current asset management patterns...
>
> **Investigation Findings:**
> - Assets are managed in `client_code/Assets/` and `server_code/AssetsOTS/`
> - Current archive functionality exists for individual assets in `archive_asset()`
> - Bulk operations pattern used in `Defects/` for bulk close-out
>
> **Follow-up Questions:**
>
> 1. **Who needs this?** Is this for admins managing large fleets, or should operators also have access?
>
> 2. **How should assets be selected?** I found these patterns in the codebase:
>    - Checkbox selection in DataGrid (like defects)
>    - Filter-then-action (archive all matching a filter)
>    - Which approach fits better?
>
> 3. **What validation is needed?** Should we:
>    - Block archiving assets with open defects?
>    - Block archiving assets currently hired out?
>    - Warn but allow?
>
> 4. **Should this be reversible?** (Bulk unarchive?)

**User:** `Admins only. Checkbox selection like defects. Warn about defects but allow. Yes, reversible.`

**Assistant:**
> Got it! Here's the draft issue...
> [Shows full issue draft]
> Does this look good to create?

**User:** `Yes, create it`

**Assistant:**
> ## Feature Issue Created
>
> **Issue:** #156 - Add bulk archive/unarchive functionality for assets
> **Link:** https://github.com/VIPER-Metrics/viper-metrics-v2-0/issues/156
>
> ### Next steps:
> ```
> /feature-planner 156
> ```
