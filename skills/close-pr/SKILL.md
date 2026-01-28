---
name: close-pr
description: Close out a completed PR after testing. Use when the user wants to close a PR, confirm a fix is working, finalize an issue, or says "close PR", "close issue", "fix is working", "tested and working". Can merge PR if not already merged, verifies testing complete, closes issue, archives wiki docs, cleans up worktree, and notifies the issue owner.
---

# Close PR

Finalize a completed pull request after testing is confirmed.

## Usage

```
/close-pr {issue_number}
```

## Workflow

### Step 1: Get Issue and PR Details

Accept issue number from `$ARGUMENTS`. If not provided, ask user.

```bash
# Get issue details
gh issue view $ARGUMENTS --json title,author,state,labels,assignees

# Find associated PR - check both merged and open states
gh pr list --search "$ARGUMENTS" --state merged --json number,title,mergedAt,baseRefName,url
gh pr list --search "$ARGUMENTS" --state open --json number,title,state,baseRefName,url
```

### Step 2: Check PR Status and Handle Accordingly

Search for the PR using multiple patterns:

```bash
# First try to find a merged PR
PR_INFO=$(gh pr list --search "closes #$ARGUMENTS OR fixes #$ARGUMENTS" --state merged --json number,baseRefName,mergedAt,url --jq '.[0]')

if [[ -z "$PR_INFO" ]]; then
    # Try searching by branch name for merged PRs
    PR_INFO=$(gh pr list --search "fix-$ARGUMENTS OR feature-$ARGUMENTS" --state merged --json number,baseRefName,mergedAt,url --jq '.[0]')
fi

if [[ -z "$PR_INFO" ]]; then
    # Check for open (unmerged) PRs
    PR_INFO=$(gh pr list --search "$ARGUMENTS" --state open --json number,baseRefName,state,url --jq '.[0]')
    # Also try by branch name
    if [[ -z "$PR_INFO" ]]; then
        PR_INFO=$(gh pr list --head "fix-$ARGUMENTS" --state open --json number,baseRefName,state,url --jq '.[0]')
    fi
fi
```

**Three possible states:**

1. **PR is merged**: Continue to Step 3
2. **PR is open (not merged)**: Inform user and proceed to Step 2a
3. **No PR found**: Stop - "No PR found for issue #$ARGUMENTS. Is there an associated PR?"

### Step 2a: Handle Unmerged PR

If the PR exists but is not merged:

1. Show the PR details to the user
2. Check if user has already confirmed testing (see Step 3 for confirmation patterns)
3. If testing confirmed, offer to merge the PR:

```bash
# Check PR is mergeable
gh pr view {pr_number} --json state,mergeable,mergeStateStatus

# If mergeable, merge it
gh pr merge {pr_number} --merge --delete-branch
```

**Note:** The `--delete-branch` may fail if a worktree is using the branch. This is expected - the branch will be cleaned up in Step 8.

After merging, continue with the closing workflow.

### Step 3: Confirm Testing Complete

**Accept informal confirmation:** If the user has already indicated testing is complete in their message (e.g., "i have reviewed and tested it", "tested and working", "fix is verified"), treat this as confirmation and proceed.

**Common confirmation phrases to accept:**
- "tested it" / "i tested it"
- "reviewed and tested"
- "verified working"
- "fix works"
- "confirmed working"
- Any message indicating they've validated the fix

**If no prior confirmation**, ask the user:

```
Before closing issue #$ARGUMENTS, please confirm:

1. Have you tested the fix/feature in staging?
2. Is the fix working as expected?

Options:
- [Yes, tested and working] - Close the issue
- [No, issues found] - Keep open and document problems
- [Skip to production] - For hotfixes already in production
```

**If "No, issues found":**
> What issues were found during testing?
>
> I'll add a comment to the issue documenting the problems.

Then add comment to issue and stop (don't close).

**If "Skip to production":**
Verify PR was merged to `published` and continue with closing.

### Step 3a: Validate Target Branch

After confirming the PR is merged (or after merging it):

```bash
BASE_BRANCH=$(gh pr view {pr_number} --json baseRefName --jq '.baseRefName')
```

**Validation:**
- If merged to `master`: Continue (normal flow)
- If merged to `published`: Warn user - "This PR was merged directly to production. Confirm this was intentional before closing."

### Step 4: Get Issue Owner

Determine who opened the issue:

```bash
# Get issue author
ISSUE_AUTHOR=$(gh issue view $ARGUMENTS --json author --jq '.author.login')
CURRENT_USER=$(gh api user --jq '.login')

echo "Issue opened by: $ISSUE_AUTHOR"
echo "Current user: $CURRENT_USER"
```

### Step 5: Post Closing Comment

Create a closing comment based on who owns the issue:

**If issue owner is current user (Jarred):**
```markdown
## Issue Resolved

**Status:** Tested and working in staging

**PR:** {pr_url}
**Merged:** {merged_at}
**Branch:** `{base_branch}`

### Testing Confirmation
- [x] Fix deployed to staging
- [x] Manual testing completed
- [x] Fix verified working

Closing this issue.
```

**If issue owner is someone else:**
```markdown
## Issue Resolved

**Status:** Tested and working in staging

**PR:** {pr_url}
**Merged:** {merged_at}
**Branch:** `{base_branch}`

### Testing Confirmation
- [x] Fix deployed to staging
- [x] Manual testing completed
- [x] Fix verified working

@{issue_author} - This fix has been tested and is working. The changes will be included in the next production release.

Closing this issue.
```

Post the comment:
```bash
gh issue comment $ARGUMENTS --body-file /tmp/closing-comment.md
```

### Step 6: Close the Issue

```bash
# Close the issue
gh issue close $ARGUMENTS --reason completed

# Update labels
gh issue edit $ARGUMENTS --add-label "verified" 2>/dev/null || true
gh issue edit $ARGUMENTS --remove-label "pr-submitted" 2>/dev/null || true
gh issue edit $ARGUMENTS --remove-label "bug" 2>/dev/null || true
```

### Step 7: Archive Wiki Documentation

Move the issue's wiki folder to the closed issues archive:

```bash
# Define paths
MAIN_REPO="$HOME/Development/VIPER/CoreApps/viper-metrics-v2-0"
SOURCE_PATH="$MAIN_REPO/wiki/issues/$ARGUMENTS"
ARCHIVE_PATH="$MAIN_REPO/wiki/issues/closed/$ARGUMENTS"

# Create closed issues folder if it doesn't exist
mkdir -p "$MAIN_REPO/wiki/issues/closed"

# Move the issue folder to closed
if [[ -d "$SOURCE_PATH" ]]; then
    mv "$SOURCE_PATH" "$ARCHIVE_PATH"
    echo "Moved wiki/issues/$ARGUMENTS → wiki/issues/closed/$ARGUMENTS"
else
    echo "No wiki folder found for issue #$ARGUMENTS"
fi
```

**Wiki structure after archiving:**
```
wiki/issues/
├── closed/
│   └── 737/
│       ├── investigation.md
│       ├── fix-plan.md
│       └── test-plan.md
├── 738/                      # Still open
│   └── ...
└── 739/                      # Still open
    └── ...
```

This keeps documentation accessible for reference while decluttering the active issues folder.

### Step 8: Cleanup Worktree

Check if a worktree exists for this issue and offer to remove it:

```bash
# Check for worktree
WORKTREE_PATH=$(git worktree list | grep "$ARGUMENTS" | awk '{print $1}')

if [[ -n "$WORKTREE_PATH" ]]; then
    echo "Worktree found: $WORKTREE_PATH"
    # Offer to remove
fi
```

**Ask user:**
> A worktree exists for this issue at `{worktree_path}`.
>
> Would you like to remove it?
> - [Yes, remove worktree]
> - [No, keep it]

If yes:
```bash
git worktree remove "$WORKTREE_PATH"
git branch -d "fix-$ARGUMENTS-*" 2>/dev/null || true
git branch -d "feature-$ARGUMENTS-*" 2>/dev/null || true
```

### Step 9: Session Complete

Output:
> ## Issue Closed
>
> **Issue:** #{number} - {title}
>
> **Status:** Closed (verified working)
>
> **PR:** {pr_url}
>
> **Merged to:** `{base_branch}`
>
> **Owner notified:** {Yes/No - @username}
>
> **Wiki archived:** `wiki/issues/closed/{number}/`
>
> **Worktree removed:** {Yes/No}
>
> ---
>
> ### Production Release
> {If merged to master:}
> This fix is now in staging. It will be included in the next production release to `published`.
>
> {If merged to published:}
> This fix is now live in production.

---

## Issue Owner Notification

The skill automatically tags the issue owner when closing if they're not the current user:

| Issue Owner | Action |
|-------------|--------|
| Current user (Jarred) | No tag needed |
| Other team member | Tag with @username |
| External user | Tag with @username |
| Bot/automation | No tag |

**Notification message:**
> @{username} - This fix has been tested and is working. The changes will be included in the next production release.

---

## Validation Rules

### PR Must Be Merged
- If PR is open and user has confirmed testing, offer to merge it
- Cannot close issue if PR was closed without merging
- Cannot close issue if no associated PR exists

### Merged to Correct Branch
- Bug fixes should go to `master` first (staging)
- Hotfixes may go directly to `published` (with warning)
- Features should go to `master`

### Testing Confirmed
- Accept informal confirmation from user messages (e.g., "tested it", "reviewed and tested", "verified working")
- Only prompt for formal confirmation if no prior indication of testing
- If issues found, document and keep open

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No PR found | "No PR found for issue #{number}. Is there an associated PR?" |
| PR open, not merged | If user confirmed testing, offer to merge. Otherwise ask for testing confirmation first. |
| PR merge fails | Show error details. Common issues: merge conflicts, failed checks. |
| Branch delete fails after merge | Expected if worktree exists. Continue - branch cleaned up in Step 8. |
| Issue already closed | "Issue #{number} is already closed." |
| Testing failed | Document issues in comment, keep issue open |
| Wiki folder not found | Warn but continue - "No wiki folder found for issue #{number}" |
| Wiki archive fails | Warn but continue - "Could not archive wiki folder. Move manually." |
| Worktree removal fails | Warn but continue - "Could not remove worktree. Remove manually with: `git worktree remove {path}`" |

---

## Labels Management

**Add on close:**
- `verified` - Confirms testing passed

**Remove on close:**
- `pr-submitted` - No longer pending
- `ready-to-implement` - Implementation complete
- `in-progress` - Work complete

**Keep:**
- `bug` or `enhancement` - For historical tracking

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/create-pr` | **Predecessor** - PR must exist |
| `/investigate-bug` | **Start of cycle** - For bug workflow |
| `/feature-planner` | **Start of cycle** - For feature workflow |

---

## Complete Bug Fix Workflow

```
/investigate-bug 142
    ↓
/fix-planner 142
    ↓
/implement-fix 142
    ↓
/create-pr 142
    ↓
[Code Review]
    ↓
[Test in staging]
    ↓
/close-pr 142    ← Merges PR if not already merged, then closes issue
    ↓
[Production release]
```

---

## Guidelines

### Always Confirm Testing
- Accept informal confirmation from user (e.g., "tested it", "reviewed and tested")
- Only prompt formally if no prior indication of testing
- Document any issues found during testing
- Keep issue open if problems persist

### Notify Stakeholders
- Always tag issue owner if not current user
- Provide clear status update
- Mention next steps (production release)

### Clean Up
- Archive wiki documentation to `wiki/issues/closed/`
- Remove worktrees after closing
- Update labels appropriately
- Documentation remains accessible in archive for future reference
