---
name: feature-planner
description: Generate an actionable implementation plan from a GitHub feature request issue. Use when the user wants to plan a new feature, create an implementation plan, prepare for building a feature, or says "plan feature", "create feature plan", "plan implementation for feature", or "how should I implement issue #X".
---

# Feature Planner Skill

Generate an actionable implementation plan from a GitHub feature request issue.

## Usage

```
/feature-planner {issue_number}
```

## Description

This skill takes a GitHub issue number for a feature request or enhancement and creates a detailed, step-by-step implementation plan. It analyzes the requirements, identifies affected areas of the codebase, generates specific implementation steps, testing strategies, and risk assessments. The plan is saved locally AND posted back to GitHub for easy reference.

## Workflow

### Step 1: Input Validation

Accept the issue number from `$ARGUMENTS`. If no argument provided, ask the user for the issue number.

Fetch the issue details:
```bash
gh issue view $ARGUMENTS --json number,title,body,labels,state,comments,milestone
```

**Validation checks:**
- Issue must exist
- Check for `enhancement`, `feature`, or similar labels (warn if missing, but continue)
- Warn if issue is closed

**If issue not found:**
> Issue #{number} not found. Check the number and try again.

### Step 2: Extract Feature Requirements

Parse the issue body to identify:

1. **User Story / Motivation** - Why is this feature needed? Who benefits?
2. **Acceptance Criteria** - What defines "done"? Expected behaviors
3. **Use Cases** - Specific scenarios the feature should handle
4. **UI/UX Requirements** - Any mockups, wireframes, or interaction details
5. **Technical Constraints** - Performance requirements, platform considerations
6. **Out of Scope** - What explicitly should NOT be included

Also check issue comments for:
- Additional requirements or clarifications
- Design decisions already discussed
- Previous implementation attempts or learnings

### Step 3: Codebase Analysis

Investigate the codebase to understand:

1. **Related existing code:**
```bash
# Search for similar functionality
grep -rn "related_keyword" --include="*.py"
```

2. **Identify integration points:**
   - Which modules will the feature interact with?
   - What existing patterns should be followed?
   - Are there reusable components?

3. **Database considerations:**
   - New tables or columns needed?
   - Existing tables to query or modify?
   - Data migration requirements?

4. **UI components:**
   - Existing forms/pages to modify?
   - New forms/pages needed?
   - Reusable components available?

### Step 4: Architecture Design

Based on requirements and codebase analysis, design the solution:

1. **Component breakdown:**
   - What new modules/classes are needed?
   - How do they fit into existing architecture?

2. **Data model:**
   - Schema changes needed?
   - Relationships to existing entities?

3. **API/Interface design:**
   - New server functions needed?
   - Changes to existing interfaces?

4. **UI flow:**
   - User journey through the feature
   - Integration with existing navigation

### Step 5: Generate Implementation Plan

Create the plan with this exact structure:

---

```markdown
# Feature Plan: Issue #{issue_number}

**Issue Title:** {title}
**Created:** {date}
**Issue Link:** {github_issue_url}

## Summary

{Brief 2-3 sentence summary of what this feature will do and why it's needed}

---

## Requirements Analysis

### User Story
{Who wants this feature and why - from issue body}

### Acceptance Criteria
- [ ] {Criterion 1 from issue}
- [ ] {Criterion 2 from issue}
- [ ] {Criterion 3 from issue}

### Use Cases
1. **{Use case name}:** {Description of the scenario}
2. **{Use case name}:** {Description of the scenario}

### Out of Scope
- {Item explicitly excluded from this feature}
- {Related enhancement for future consideration}

---

## Pre-Implementation Checklist

- [ ] Create worktree from **published** (main branch):
  ```bash
  git fetch origin
  git worktree add ~/GitHub/viper-metrics-worktrees/{number}-{short-name} -b feature-{number}-{short-description} origin/published
  cd ~/GitHub/viper-metrics-worktrees/{number}-{short-name}
  ```
- [ ] Review acceptance criteria with stakeholder (if unclear)
- [ ] Verify current test suite passes
- [ ] Backup database (if schema changes involved)
- [ ] Review VIPER Metrics coding standards

> **Note**: We use git worktrees to isolate work on each issue. Branch from `published` (main branch).

---

## Architecture Overview

### Component Diagram
```
{ASCII diagram showing component relationships}

Example:
┌─────────────────┐     ┌──────────────────┐
│  Client Form    │────▶│  Server Module   │
│  (FeatureName)  │     │  (FeatureOTS)    │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Database Table  │
                        │  (feature_data)  │
                        └──────────────────┘
```

### Data Model Changes

| Table | Change Type | Description |
|-------|-------------|-------------|
| `{table_name}` | {New/Modify} | {What changes and why} |

**Schema:**
```python
# New table definition (if applicable)
app_tables.{table_name}:
  - column1: text
  - column2: number
  - column3: link_single(other_table)
```

### New Server Functions

| Function | Module | Purpose |
|----------|--------|---------|
| `{function_name}` | `{ModuleOTS}` | {What it does} |

### UI Components

| Component | Location | Type |
|-----------|----------|------|
| `{FormName}` | `client_code/{path}` | {New/Modify} |

---

## Implementation Steps

### Phase 1: Data Layer
{Database and data model changes - do these first}

#### Step 1.1: {Database change description}

**Table:** `{table_name}`

**Changes:**
- Add column `{column_name}` ({type})
- Add index on `{column_name}` (if needed)

**Migration Script (if needed):**
```python
# Run in Anvil shell or create migration task
for row in app_tables.{table}.search():
    row['new_column'] = {default_value}
```

**Note:** Database table changes must be done in Anvil IDE - create list of changes for manual implementation.

---

### Phase 2: Server Layer
{Backend business logic}

#### Step 2.1: {Server function description}

**File:** `server_code/{ModuleOTS}/{filename}.py`

**New Function:**
```python
@anvil.server.callable
@authorisation_required("{Permission Name}")
@track_server_function
def {function_name}({parameters}):
    """
    {Docstring explaining purpose}

    Args:
        {param}: {description}

    Returns:
        {return_description}
    """
    # Implementation
    pass
```

**Why This Approach:**
{Explanation of design decisions, patterns followed, etc.}

**Edge Cases to Handle:**
- {edge case 1}
- {edge case 2}

---

### Phase 3: Client Layer
{Frontend forms and components}

#### Step 3.1: {Form/component description}

**File:** `client_code/{path}/{FormName}/__init__.py`

**Form Structure:**
```yaml
# Form YAML (create in Anvil IDE)
components:
  - type: Label
    name: lbl_title
    text: "{Title}"
  - type: DataGrid
    name: grid_data
    columns:
      - id: col_1
        title: "{Column Title}"
```

**Form Code:**
```python
class {FormName}({FormNameTemplate}):
    def __init__(self, **properties):
        self.init_components(**properties)
        # Initialization code

    def btn_action_click(self, **event_args):
        """Handle action button click"""
        pass
```

**User Flow:**
1. User navigates to {location}
2. User sees {initial state}
3. User performs {action}
4. System responds with {result}

---

### Phase 4: Integration
{Connecting components together}

#### Step 4.1: {Integration description}

**Connect to Navigation:**
- Add link in `{navigation_location}`
- Permission: `{required_permission}`

**Wire Up Events:**
```python
# In {parent_form}
def open_{feature}(self, **event_args):
    open_form('{FormName}')
```

---

## Testing Strategy

### Unit Tests to Add

| Test File | Test Name | Purpose |
|-----------|-----------|---------|
| `{test_file}` | `test_{name}` | {what it verifies} |

**Test Code:**
```python
def test_{function_name}_happy_path():
    """Test that {description}"""
    # Arrange
    {setup}

    # Act
    result = {function_name}({args})

    # Assert
    assert result == {expected}


def test_{function_name}_edge_case():
    """Test that {edge case handling}"""
    # Arrange
    {setup}

    # Act & Assert
    with pytest.raises({ExpectedError}):
        {function_name}({invalid_args})
```

### Integration Tests

- [ ] {End-to-end scenario 1}
- [ ] {End-to-end scenario 2}

### Manual Testing Steps

1. **Setup:** {how to prepare the test environment}
2. **Test Scenario 1: {name}**
   - Navigate to {location}
   - Perform {action}
   - Expected: {result}
3. **Test Scenario 2: {name}**
   - {steps}
   - Expected: {result}

### Acceptance Criteria Verification

| Criterion | How to Verify | Status |
|-----------|---------------|--------|
| {Criterion 1} | {Test method} | [ ] |
| {Criterion 2} | {Test method} | [ ] |

---

## Permissions & Security

### Required Permissions

| Permission | Needed For | New? |
|------------|------------|------|
| `{Permission Name}` | {Why needed} | {Yes/No} |

### Security Considerations

- {Data validation requirements}
- {Authorization checks}
- {Sensitive data handling}

---

## Code Review Checklist

- [ ] All acceptance criteria addressed
- [ ] Follows VIPER Metrics coding patterns
- [ ] Server functions have proper authorization decorators
- [ ] Error handling is appropriate
- [ ] Logging is adequate for debugging
- [ ] No hardcoded values (use configuration)
- [ ] No security vulnerabilities (OWASP top 10)
- [ ] Database queries are efficient
- [ ] UI is responsive and accessible
- [ ] Code is well-documented

---

## Risk Assessment

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {risk 1} | {Low/Med/High} | {Low/Med/High} | {mitigation} |

### Dependencies

| Dependency | Risk Level | Notes |
|------------|------------|-------|
| {External API/service} | {Low/Med/High} | {what could go wrong} |
| {Existing module} | {Low/Med/High} | {what could go wrong} |

### Performance Implications

- {Expected load increase}
- {Database query impact}
- {Memory/CPU concerns}

### Deployment Considerations

- [ ] {Deployment step 1}
- [ ] {Feature flag needed?}
- [ ] {Data migration timing}

---

## Documentation Updates

| Document | Update Needed |
|----------|---------------|
| User guide | {What to add} |
| API docs | {What to add} |
| Training materials | {What to add} |

---

## Effort Estimate

| Task | Hours |
|------|-------|
| Data layer changes | {hours} |
| Server functions | {hours} |
| UI components | {hours} |
| Integration | {hours} |
| Unit tests | {hours} |
| Integration tests | {hours} |
| Manual testing | {hours} |
| Code review | {hours} |
| Documentation | {hours} |
| **Total** | **{total hours}** |

---

## Future Enhancements

{Ideas for follow-up features that came up during planning but are out of scope}

- {Enhancement 1} - Consider for future issue
- {Enhancement 2} - Consider for future issue

---

## Next Steps

1. Review this plan and request changes if needed
2. Make database changes in Anvil IDE (if any)
3. When approved, run: `@implement-feature {issue_number}`
4. Create PR and request code review
```

---

### Step 6: Risk Assessment

Analyze the proposed changes for:

1. **Technical Risks**
   - What could fail during implementation?
   - External dependencies that might break?
   - Complex integrations to watch?

2. **Performance Impact**
   - New database queries
   - Additional API calls
   - Memory/CPU requirements

3. **Deployment Risks**
   - Database migrations needed?
   - Feature flags recommended?
   - Rollback strategy?

4. **User Impact**
   - Learning curve for users?
   - Changes to existing workflows?

### Step 7: Estimate Effort

Provide realistic time estimates based on:
- Complexity of new components
- Number of files affected
- Integration requirements
- Testing requirements

Be conservative - it's better to over-estimate than under-estimate.

### Step 8: Save the Plan

Create the docs directory if it doesn't exist:
```bash
mkdir -p docs/feature-plans
```

Save the plan:
```bash
# The plan should be saved to: docs/feature-plans/FEATURE-{issue-number}-plan.md
```

### Step 9: Post to GitHub

Add the plan as a comment on the issue:
```bash
gh issue comment $ARGUMENTS --body-file docs/feature-plans/FEATURE-$ARGUMENTS-plan.md
```

### Step 10: Add Label

Mark the issue as having a plan:
```bash
gh issue edit $ARGUMENTS --add-label "planned"
```

### Step 11: Confirm to User

Output:
> ## Feature Plan Created
>
> **Issue:** #{number} - {title}
>
> **Plan saved to:** `docs/feature-plans/FEATURE-{number}-plan.md`
>
> **Posted to:** GitHub issue as comment
>
> ---
>
> ### Review the plan and when approved, run:
> ```
> @implement-feature {issue_number}
> ```

---

## Guidelines

### Understand Before Planning
- Read the full issue including all comments
- Search for related issues or previous discussions
- Identify any existing similar functionality

### Be Specific
- Always include exact file paths
- Show actual code snippets, not descriptions
- Name specific functions and components

### Follow Existing Patterns
- Match VIPER Metrics coding conventions
- Use existing OTS patterns for server modules
- Reuse components where possible

### Call Out Risks
- Don't hide potential problems
- Rate risks as Low/Medium/High
- Provide mitigation strategies

### Keep Scope Manageable
- If feature is too large, suggest breaking into phases
- Identify MVP vs nice-to-have elements
- Document what's explicitly out of scope

### Database Awareness
- Remember: Database changes require Anvil IDE
- List schema changes clearly for manual implementation
- Include migration scripts where applicable

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Issue not found | "Issue #{n} not found. Check the number and try again." |
| No feature label | "Warning: Issue #{n} doesn't have a 'feature' or 'enhancement' label. Proceeding anyway." |
| Unclear requirements | Ask specific clarifying questions before generating plan |
| Very large feature | Suggest breaking into multiple issues/phases |
| Missing acceptance criteria | List what's missing and suggest criteria based on description |

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `@issue-triage` | **Predecessor** - May suggest features to plan |
| `@implement-feature` | **Next step** - Executes this plan |
| `@create-pr` | **After implementation** - Creates pull request |
| VIPER Metrics Standards | **Reference** - Follow coding conventions |

---

## Example Output

```
## Feature Plan Created

**Issue:** #789 - Add bulk export for inspection reports

**Plan saved to:** `docs/feature-plans/FEATURE-789-plan.md`

**Posted to:** GitHub issue as comment

---

### Review the plan and when approved, run:
```
@implement-feature 789
```
```
