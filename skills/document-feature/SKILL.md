---
name: document-feature
description: Create user-facing documentation for a feature. Use when the user wants to document a feature, create feature docs, write documentation for a PR, or says "document feature", "create docs for", "write documentation for PR". Called by /release-production when features are undocumented.
---

# Document Feature

Create user-facing documentation for a feature based on its PR and code changes.

## Usage

```
/document-feature {pr_number}
```

or

```
/document-feature {feature_name}
```

## Workflow

### Step 1: Gather Feature Context

Accept PR number or feature name from `$ARGUMENTS`. If not provided, ask user.

```bash
# If a PR number was provided
gh pr view $ARGUMENTS --json title,body,files,labels,mergedAt,baseRefName

# Get the changed files
gh pr view $ARGUMENTS --json files --jq '.files[].path'

# Get the PR description
gh pr view $ARGUMENTS --json body --jq '.body'

# Get linked issue if exists
gh pr view $ARGUMENTS --json body --jq '.body' | grep -oE '#[0-9]+' | head -1
```

**If PR number provided:**
- Extract feature name from PR title
- Read PR description for context
- Identify key files changed

**If feature name provided:**
- Search for related PRs
- Ask user for additional context

### Step 2: Analyze the Code

Read the key files to understand the feature:

```bash
# Get list of changed files from PR
FILES=$(gh pr view $ARGUMENTS --json files --jq '.files[].path')

# Focus on:
# - Client code (user-facing forms)
# - Server endpoints (new functionality)
# - Any new modules
```

**Analysis goals:**
- What does the feature do?
- How does a user access it?
- What options/settings are available?
- What are common use cases?

### Step 3: Ask Clarifying Questions

If needed, ask user for missing context:

> I'm documenting the **{feature_name}** feature. I need some clarification:
>
> 1. **Target audience**: Who will use this feature?
>    - [ ] All users
>    - [ ] Admins only
>    - [ ] Specific roles
>
> 2. **Access path**: How do users get to this feature?
>    - Example: "Navigate to Assets > Reports > {feature}"
>
> 3. **Key benefits**: What problem does this solve?
>
> 4. **Prerequisites**: Does the user need anything set up first?

### Step 4: Generate Documentation

Create documentation using the template:

```markdown
---
title: "{Feature Name}"
date: {date}
author: {author}
status: published
tags: [feature]
pr: #{pr_number}
---

# {Feature Name}

## Overview

{2-3 sentence description of what this feature does and why it's useful}

## Getting Started

How to access this feature:

1. Navigate to **{menu path}**
2. Click on **{button/link}**
3. You'll see **{what appears}**

## How It Works

### Basic Usage

{Step-by-step instructions for the most common use case}

1. {First step}
2. {Second step}
3. {Third step}

### Options and Settings

| Option | Description | Default |
|--------|-------------|---------|
| {Option 1} | {What it does} | {Default value} |
| {Option 2} | {What it does} | {Default value} |

### Advanced Usage

{Any advanced options or configurations}

## Use Cases

### {Use Case 1}

**Scenario**: {When you would use this}

**Steps**:
1. {Step 1}
2. {Step 2}

### {Use Case 2}

**Scenario**: {Another common scenario}

**Steps**:
1. {Step 1}
2. {Step 2}

## Tips

- {Helpful tip for getting the most out of this feature}
- {Another useful tip}
- {Best practice}

## Permissions

This feature requires the following permissions:
- {Permission 1}
- {Permission 2}

Or: "Available to all users"

## Troubleshooting

### {Common Issue 1}

**Problem**: {Description of what goes wrong}

**Solution**: {How to fix it}

### {Common Issue 2}

**Problem**: {Description of what goes wrong}

**Solution**: {How to fix it}

## Related Features

- [[features/{related-feature}|{Related Feature Name}]]
- [[features/{another-feature}|{Another Feature Name}]]

---

[[features/README|Back to Features]]
```

### Step 5: Review with User

Present the documentation for review:

> ## Documentation Preview
>
> I've generated the following documentation for **{feature_name}**:
>
> {Show full documentation}
>
> **Options:**
> - [Approve and save] - Save to wiki/features/
> - [Edit] - Make changes
> - [Add more detail] - Expand specific sections

**If user wants edits:**
Incorporate feedback and regenerate.

### Step 6: Save Documentation

```bash
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"

# Generate filename from feature name
FEATURE_SLUG=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

# Save to wiki
FEATURE_FILE="$MAIN_REPO/wiki/features/$FEATURE_SLUG.md"
```

Use the Write tool to create the file.

### Step 7: Update Features README

Add the new feature to the features index:

```bash
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"

# Check if features/README.md has a features list
# If so, add the new feature to it
```

### Step 8: Commit Documentation

```bash
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"
cd "$MAIN_REPO"

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# If on master, commit directly
if [[ "$CURRENT_BRANCH" == "master" ]]; then
    git add "wiki/features/$FEATURE_SLUG.md"
    git commit -m "Add documentation for $FEATURE_NAME"
    git push origin master
else
    # If on a feature branch, commit there
    git add "wiki/features/$FEATURE_SLUG.md"
    git commit -m "Add documentation for $FEATURE_NAME"
fi
```

### Step 9: Session Complete

Output:
> ## Feature Documented
>
> **Feature:** {Feature Name}
>
> **Documentation:** `wiki/features/{feature-slug}.md`
>
> **Based on:** PR #{pr_number}
>
> ---
>
> The documentation has been saved and committed. It will be linked in the changelog when the feature is released.
>
> **View documentation:** [wiki/features/{feature-slug}.md]

---

## Documentation Guidelines

### Write for Users, Not Developers

- Focus on "how to use" not "how it works technically"
- Use simple language
- Include screenshots if helpful (describe them for now)
- Provide concrete examples

### Structure for Scanability

- Use clear headings
- Keep paragraphs short
- Use bullet points and tables
- Put the most important info first

### Include Practical Examples

- Show real-world use cases
- Provide step-by-step instructions
- Include tips from actual usage

### Keep It Current

- Update when features change
- Remove outdated information
- Link to related features

---

## Error Handling

| Scenario | Action |
|----------|--------|
| PR not found | "PR #{number} not found. Check the number and try again." |
| PR not merged | "PR #{number} is not merged yet. Document after merge." |
| Can't determine feature | Ask user for feature name and description |
| No code access | Use PR description and ask user for details |
| Feature already documented | "Documentation already exists at wiki/features/{name}.md. Update it?" |

---

## Filename Convention

Feature documentation uses slugified names:

| Feature Name | Filename |
|--------------|----------|
| Bulk Export | `bulk-export.md` |
| Dark Mode Support | `dark-mode-support.md` |
| Service Board Pagination | `service-board-pagination.md` |
| PDF Report Generation | `pdf-report-generation.md` |

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/release-production` | **Caller** - Prompts to run this for undocumented features |
| `/feature-planner` | **Earlier in cycle** - May contain useful context |
| `/implement-feature` | **Earlier in cycle** - Has implementation details |

---

## When to Document

### Always Document

- New user-facing features
- Significant UI changes
- New capabilities or workflows
- Features mentioned in release notes

### Don't Need Full Docs

- Bug fixes (changelog entry sufficient)
- Internal refactoring
- Performance improvements
- Minor UI tweaks

### Update Existing Docs

- When a feature is enhanced
- When behavior changes
- When options are added/removed

---

## Quick Reference

```bash
# Document a merged PR
/document-feature 456

# Document by feature name
/document-feature "Bulk Export"

# Check if feature is documented
ls wiki/features/bulk-export.md
```

---

## Template Sections Explained

| Section | Purpose | Required |
|---------|---------|----------|
| Overview | Quick summary of what/why | Yes |
| Getting Started | How to access the feature | Yes |
| How It Works | Step-by-step usage | Yes |
| Options/Settings | Available configurations | If applicable |
| Use Cases | Real-world scenarios | Recommended |
| Tips | Best practices | Recommended |
| Permissions | Who can use it | If restricted |
| Troubleshooting | Common issues | If known issues exist |
| Related Features | Links to related docs | If applicable |
