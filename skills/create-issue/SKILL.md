---
name: create-issue
description: Create a well-documented GitHub issue through interactive questions. Use when the user wants to create a new bug report, feature request, improvement, or any GitHub issue. Guides through gathering context, reading related code, and creating a properly labeled issue.
---

# Create GitHub Issue

Guide users through creating a comprehensive GitHub issue by asking structured questions and gathering context from the codebase.

## Usage

```
/create-issue
```

## Workflow

### Step 1: Determine Issue Type

Ask: "What type of issue is this?"

| Type | Label | Description |
|------|-------|-------------|
| Bug | `bug` | Something isn't working |
| Feature | `enhancement` | New functionality |
| Improvement | `enhancement` | Enhance existing functionality |
| Documentation | `documentation` | Documentation updates |
| Business Logic | `business-logic` | Business rules or calculations |
| Question | `question` | Needs clarification |

### Step 2: Identify Component

Ask: "Which component, form, or module is this related to?"

Examples:
- CalcEOM form
- ServiceBoard module
- Sync endpoints
- Asset management
- Defects system

### Step 3: Gather Detailed Context

Ask type-specific questions:

#### For Bugs:
1. What is the current (incorrect) behavior?
2. What is the expected (correct) behavior?
3. Are there any error messages or logs?
4. What are the steps to reproduce?
5. Does this happen consistently or intermittently?
6. Which users/companies are affected?

#### For Features:
1. What functionality should be added?
2. Why is this needed? What problem does it solve?
3. Who will use this feature?
4. Any specific requirements or constraints?
5. Any design/implementation ideas?

#### For Improvements:
1. What currently exists that needs improving?
2. What would the improvement look like?
3. What are the benefits?
4. Any performance or UX concerns?

#### For Business Logic:
1. What business rule or calculation needs to be addressed?
2. What is the current business logic (if it exists)?
3. What should the correct business logic be?
4. Are there specific data validation rules required?
5. What are the business conditions/triggers?
6. Are there any regulatory or compliance requirements?
7. What data sources or tables are involved?
8. What should happen in edge cases?

#### For All Types:
1. Related file paths?
2. Priority? (Low/Medium/High/Critical)
3. Any screenshots or additional context?

### Step 4: Gather Code Context

After collecting answers:

1. **Read mentioned files** to understand the code:
```bash
# Read files mentioned by user
cat {file_path}
```

2. **Search for related patterns**:
```bash
# Find related code
grep -rn "{keyword}" --include="*.py"
```

3. **Note relevant details**:
   - File paths and line numbers
   - Related functions or classes
   - Similar existing implementations
   - Potential impact areas

### Step 5: Create the Issue

Format the issue using this structure:

```markdown
## Type
{Bug/Feature/Improvement/Documentation/Business Logic/Question}

## Component
{Name and file paths}

## Description
{Clear, concise description of the issue}

## Current Behavior
{For bugs: what happens now}
{For business logic: current rule/calculation}
{For improvements: current state}

## Expected Behavior
{For bugs: what should happen}
{For features: what it should do}
{For business logic: correct rule/calculation}
{For improvements: desired state}

## Business Rules
{For business logic issues only:}
- **Validation rules:** {list}
- **Conditions/triggers:** {list}
- **Data sources:** {tables/APIs}
- **Edge cases:** {list}
- **Regulatory requirements:** {if any}

## Steps to Reproduce
{For bugs only:}
1. {step 1}
2. {step 2}
3. {step 3}

## Error Messages/Logs
{If applicable - include stack traces, console output}

## Related Files
- `{path/to/file.py}:{line}` - {description}
- `{path/to/file.py}:{line}` - {description}

## Additional Context
{Screenshots, related issues, background info}

## Priority
{Low/Medium/High/Critical}

## Implementation Notes
{Ideas, constraints, or considerations}

---
*Created via /create-issue*
```

### Step 6: Create Issue with GitHub CLI

```bash
# Create the issue with appropriate labels
gh issue create \
  --title "{concise title}" \
  --body-file /tmp/issue-body.md \
  --label "{primary-label}" \
  --label "{secondary-label}"
```

**Label mapping:**
| Issue Type | Primary Label | Secondary Labels |
|------------|---------------|------------------|
| Bug | `bug` | priority, component |
| Feature | `enhancement` | priority |
| Improvement | `enhancement` | priority |
| Documentation | `documentation` | - |
| Business Logic | `business-logic` | priority |
| Question | `question` | - |

**Priority labels:**
- `priority: critical` (P0)
- `priority: high` (P1)
- `priority: medium` (P2)
- `priority: low` (P3)

### Step 7: Confirm Creation

After creating:
```bash
# Get the issue URL
gh issue view {issue_number} --json url --jq '.url'
```

Output:
> ## Issue Created
>
> **Issue:** #{number} - {title}
>
> **URL:** {github_url}
>
> **Labels:** {list of labels}
>
> ---
>
> Would you like me to:
> - Open the issue in your browser?
> - Start investigating this bug? (`/investigate-bug {number}`)
> - Start planning this feature? (`/feature-planner {number}`)

---

## Guidelines

### Write Clear Titles
- Start with action verb for features: "Add...", "Enable...", "Support..."
- Start with problem for bugs: "Fix...", "Error when...", "Cannot..."
- Be specific but concise (under 70 characters)

### Gather Enough Context
- Always read related files before creating
- Include relevant code snippets in the issue
- Reference specific line numbers
- Note any patterns or similar code

### Use Appropriate Labels
- Always include the type label (bug, enhancement, etc.)
- Add priority if known
- Add component labels if available

### Link Related Issues
- Search for similar existing issues
- Reference related issues with `#number`
- Note if this blocks or is blocked by other issues

---

## Error Handling

| Scenario | Action |
|----------|--------|
| File not found | Note that file doesn't exist, ask for correct path |
| Unclear requirements | Ask clarifying questions |
| Duplicate issue | Search first, suggest linking to existing issue |
| Missing context | Prompt for more details before creating |

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/investigate-bug` | **Next step** for bugs |
| `/feature-planner` | **Next step** for features |
| `/issue-triage` | Can trigger issue creation |

---

## Example Session

```
> /create-issue

What type of issue is this?
1. 🐛 Bug
2. ✨ Feature
3. 🔧 Improvement
4. 📝 Documentation
5. 📊 Business Logic
6. ❓ Question

> 1

Which component, form, or module is this related to?

> ServiceBoard module, the scheduling calendar

What is the current (incorrect) behavior?

> When I drag an event to a new date, it doesn't save

What is the expected behavior?

> The event should update to the new date

Are there any error messages?

> Console shows "TypeError: Cannot read property 'date' of undefined"

What are the steps to reproduce?

> 1. Open service board
> 2. Drag any event to a different date
> 3. Release - event snaps back

Related file paths?

> Not sure, probably in client_code/Maintenance/ServiceBoard somewhere

Priority?

> High - blocking daily operations

---

Let me read the ServiceBoard code to understand the issue...

[Reads client_code/Maintenance/ServiceBoard/__init__.py]
[Searches for drag event handlers]

Found relevant code at:
- `client_code/Maintenance/ServiceBoard/__init__.py:245` - drag handler
- `server_code/MaintenanceOTS/ServiceBoard.py:89` - update function

## Issue Created

**Issue:** #742 - Fix event drag-and-drop not saving on ServiceBoard

**URL:** https://github.com/VIPER-Metrics/viper-metrics-v2-0/issues/742

**Labels:** bug, priority: high

---

Would you like me to start investigating this bug?
```
