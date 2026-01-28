---
name: release-production
description: Merge master (staging) into published (production) with changelog creation. Use when the user wants to release to production, deploy to production, merge to published, or says "release to production", "deploy production", "merge master to published". Ensures all features are documented before release.
---

# Release Production

Merge master (staging) into published (production) with proper changelog documentation.

## Usage

```
/release-production
```

## Workflow

### Step 1: Pre-Flight Checks

Verify we're ready to release:

```bash
# Ensure we're in the main repo (not a worktree)
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"
cd "$MAIN_REPO"

# Fetch latest from remote
git fetch origin

# Check current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Verify master and published are up to date
git log origin/master..master --oneline
git log origin/published..published --oneline
```

**Validations:**
- Must be in the main repo (not a worktree)
- No uncommitted changes
- Local branches in sync with remote

### Step 2: Identify Changes for Release

Get all changes that will be released:

```bash
# Get commits on master that aren't in published
git log origin/published..origin/master --oneline

# Get the list of merged PRs
git log origin/published..origin/master --merges --oneline

# Get detailed info on PRs included
gh pr list --state merged --base master --json number,title,mergedAt,labels,author --jq '.[] | select(.mergedAt > "LAST_RELEASE_DATE")'
```

Create a summary of what's being released:

```bash
# Find all PRs merged since last release
# Look at the published branch's last commit date
LAST_RELEASE=$(git log origin/published -1 --format="%cI")

# Get PRs merged to master after that date
gh pr list --state merged --base master --json number,title,mergedAt,labels --jq "[.[] | select(.mergedAt > \"$LAST_RELEASE\")]"
```

**Output a summary:**
> ## Changes Ready for Release
>
> **Commits:** {count} commits
>
> **PRs included:**
> | PR | Title | Type |
> |----|-------|------|
> | #123 | Fix login error | Bug Fix |
> | #456 | Add bulk export | Feature |

### Step 3: Check Documentation Status

For each PR being released, check if it needs documentation:

```bash
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"

# For each PR in the release
for PR in $PR_LIST; do
    # Get PR labels
    LABELS=$(gh pr view $PR --json labels --jq '.labels[].name')

    # Features (enhancement label) need documentation
    if echo "$LABELS" | grep -q "enhancement"; then
        # Check if documentation exists
        FEATURE_NAME=$(gh pr view $PR --json title --jq '.title' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

        if [[ ! -f "$MAIN_REPO/wiki/features/$FEATURE_NAME.md" ]]; then
            echo "UNDOCUMENTED: PR #$PR needs documentation"
        fi
    fi
done
```

**Three scenarios:**

1. **All features documented** → Continue to Step 4
2. **Features need documentation** → Stop and prompt user
3. **Bug fixes only** → Continue (bugs don't need feature docs)

**If undocumented features exist:**

> ## Documentation Required
>
> The following features need documentation before release:
>
> | PR | Title | Status |
> |----|-------|--------|
> | #456 | Add bulk export | Needs documentation |
> | #789 | Dark mode support | Needs documentation |
>
> **Options:**
> - Run `/document-feature {pr_number}` for each feature
> - Or provide documentation manually
>
> Re-run `/release-production` after documentation is complete.

**Stop here if documentation is missing.**

### Step 4: Generate Changelog Entry

Create the changelog file:

```bash
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"
TODAY=$(date +%Y-%m-%d)
MONTH_YEAR=$(date +"%B %Y")

# Create changelog file
CHANGELOG_FILE="$MAIN_REPO/wiki/changelog/$TODAY-release.md"
```

**Changelog content structure:**

```markdown
---
title: {Month Year} Release
date: {YYYY-MM-DD}
author: Jarred
status: published
tags:
  - changelog
---

# {Month Year} Release

**Release Date**: {Full Date}

## Summary

{2-3 sentence overview of what's in this release}

## New Features

- **Feature Name** ([#{pr_number}]({pr_url})): Description of the new feature and how to use it. See [[features/{feature-name}|documentation]].

## Improvements

- **Area improved** ([#{pr_number}]({pr_url})): What was improved and why it matters.

## Bug Fixes

| Issue | PR | Description |
|-------|-----|-------------|
| [#{issue}]({issue_url}) | [#{pr}]({pr_url}) | Brief description of what was fixed |

## Breaking Changes

{List any breaking changes, or "None" if none}

## Migration Notes

{Any steps users need to take, or "No user action required."}

---

[[changelog/README|Back to Changelog]]
```

**Guidelines for changelog:**
- Group PRs by type (Feature, Improvement, Bug Fix)
- Link to feature documentation for new features
- Include both issue and PR links for bug fixes
- Note any breaking changes prominently

### Step 5: Review Changelog

Present the generated changelog to the user:

> ## Changelog Preview
>
> I've generated the following changelog for this release:
>
> {Show full changelog content}
>
> **Options:**
> - [Approve and continue] - Save changelog and proceed with merge
> - [Edit changelog] - Make changes before saving
> - [Cancel] - Don't release yet

**If "Edit changelog":**
Allow user to provide edits, then regenerate.

### Step 6: Save Changelog and Commit

```bash
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"
cd "$MAIN_REPO"

# Checkout master
git checkout master
git pull origin master

# Write changelog file
# (Use Write tool to create the file)

# Commit changelog
git add "wiki/changelog/$TODAY-release.md"
git commit -m "Add changelog for $TODAY release"
git push origin master
```

### Step 7: Merge Master into Published

Perform the production merge:

```bash
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"
cd "$MAIN_REPO"

# Checkout published
git checkout published
git pull origin published

# Merge master into published
git merge origin/master --no-edit

# Push to remote
git push origin published
```

**If merge conflicts:**
> ## Merge Conflict
>
> There are conflicts between master and published:
>
> ```
> {list of conflicting files}
> ```
>
> This usually shouldn't happen. Please resolve manually or investigate why the branches diverged.

### Step 8: Tag the Release (Optional)

Ask user if they want to create a release tag:

> Would you like to create a Git tag for this release?
>
> - [Yes, create tag] - Create tag `release-{date}`
> - [No, skip tag] - Continue without tagging

If yes:
```bash
TAG_NAME="release-$(date +%Y-%m-%d)"
git tag -a "$TAG_NAME" -m "Production release $(date +%Y-%m-%d)"
git push origin "$TAG_NAME"
```

### Step 9: Session Complete

Output:
> ## Production Release Complete
>
> **Release Date:** {date}
>
> **Changes Released:**
> - {X} commits
> - {Y} bug fixes
> - {Z} features
>
> **Changelog:** `wiki/changelog/{date}-release.md`
>
> **Branches:**
> - `master` (staging) merged into `published` (production)
>
> **Tag:** `release-{date}` (if created)
>
> ---
>
> ### What's Next
>
> 1. Verify production deployment in Anvil
> 2. Smoke test critical features
> 3. Monitor for errors
>
> ### Release Notes URL
> {If you publish changelogs externally, include link}

---

## Documentation Check Logic

Features require documentation; bug fixes don't:

| PR Label | Documentation Required |
|----------|----------------------|
| `enhancement` | Yes - must have wiki/features/{name}.md |
| `feature` | Yes - must have wiki/features/{name}.md |
| `bug` | No - changelog entry sufficient |
| `fix` | No - changelog entry sufficient |
| Other | Evaluate based on PR title/content |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Uncommitted changes | "Commit or stash changes before releasing" |
| Master behind remote | "Pull latest master first: `git pull origin master`" |
| Published behind remote | "Pull latest published first" |
| Undocumented features | List them and stop - require /document-feature first |
| Merge conflicts | Show conflicts and stop - require manual resolution |
| No changes to release | "No new changes on master since last release" |
| Push fails | "Push failed. Check permissions and try manually" |

---

## Changelog Naming Convention

Files are named by release date:
```
wiki/changelog/
├── 2026-01-28-release.md
├── 2026-02-15-release.md
├── 2026-03-01-release.md
└── README.md
```

For multiple releases on the same day (rare):
```
wiki/changelog/
├── 2026-01-28-release.md
├── 2026-01-28-release-2.md  # Hotfix same day
```

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/document-feature` | **Prerequisite** - Must run for undocumented features |
| `/close-pr` | **Predecessor** - Issues should be closed before release |
| `/create-pr` | **Earlier in cycle** - PRs merged to master |

---

## Complete Release Workflow

```
[PRs merged to master]
    ↓
[Test in staging]
    ↓
/close-pr {numbers}        ← Close all issues for this release
    ↓
/release-production        ← This skill
    ↓
    ├── Check documentation status
    │   ├── If undocumented → /document-feature {pr}
    │   └── If documented → Continue
    ↓
    ├── Generate changelog
    ├── Merge master → published
    └── Push to production
    ↓
[Verify production deployment]
```

---

## Guidelines

### Always Document Features
- Features without documentation create confusion
- Documentation helps users understand new capabilities
- Changelog can reference feature docs for details

### Write Clear Changelogs
- Summarize the "why" not just the "what"
- Group related changes together
- Highlight breaking changes prominently

### Test Before Release
- All changes should be tested in staging
- Issues should be closed (verified working) before release
- Don't release untested changes

### Keep Changelog History
- Never delete old changelog entries
- They serve as historical record
- Useful for tracking when changes were deployed
