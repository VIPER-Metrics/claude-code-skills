# Claude Code Skills

A comprehensive set of Claude Code skills, commands, and agents for Anvil.works development workflows.

## Overview

These skills form complete pipelines for both **bug fixing** and **feature development** that integrate with GitHub Issues and Pull Requests:

### Bug Fix Pipeline
```
@issue-triage → @investigate-bug → @fix-planner → @implement-fix → @create-pr
      ↓               ↓                 ↓               ↓               ↓
  Prioritizes     Posts report      Posts plan     Commits code    Opens PR
  open issues     to issue          to issue       to branch       on GitHub
```

### Feature Development Pipeline
```
@create-feature → @feature-planner → @implement-feature → @create-pr
       ↓                ↓                   ↓                 ↓
   Creates          Posts plan        Commits code       Opens PR
   GitHub issue     to issue          to branch          on GitHub
```

## Installation

### For VIPER Team Members

Clone this repo alongside the other VIPER repos and run the setup script:

```bash
cd ~/GitHub  # or wherever your repos are

# Clone if you haven't already
git clone https://github.com/VIPER-Metrics/claude-code-skills.git

# Run setup script to create shared CLAUDE.md symlink
./claude-code-skills/setup.sh
```

This creates a symlink so the shared `CLAUDE.md` is read automatically when working in any VIPER repo.

### For Other Projects

Copy the `.claude` directory to your project root:

```bash
# Clone this repo
git clone https://github.com/VIPER-Metrics/claude-code-skills.git

# Copy to your project
cp -r claude-code-skills/.claude /path/to/your/project/
```

Or manually copy the files:
```
your-project/
└── .claude/
    ├── create-pr.md
    ├── feature-planner.md
    ├── fix-planner.md
    ├── get-session-logs.md
    ├── implement-feature.md
    ├── implement-fix.md
    ├── investigate-bug.md
    ├── commands/
    │   ├── create-bug.md
    │   ├── create-hotfix.md
    │   ├── fix-bug.md
    │   └── investigate-bug.md
    └── skills/
        ├── create-feature/
        │   └── SKILL.md
        └── issue-triage/
            ├── SKILL.md
            └── scripts/
                └── generate_report.py
```

## Skills

### `/create-feature {description}` (optional)

Transform a rough feature idea into a well-structured GitHub issue through guided discovery.

**What it does:**
- Takes your initial feature idea (even vague descriptions work)
- Investigates the codebase to find related code and patterns
- Asks clarifying questions about users, scope, and edge cases
- Creates a comprehensive GitHub issue with acceptance criteria

**Output:** GitHub issue with user story, acceptance criteria, use cases, and technical context

---

### `/issue-triage`

Fetch, rank, and display open GitHub issues by priority.

**What it does:**
- Fetches all open issues from current repository
- Ranks by priority: 🔴 Critical → 🟠 High → 🟡 Aging Bugs → ⚪ Standard
- Displays as scannable markdown table with excerpts
- Prompts user to select an issue for investigation

**Priority Logic:**
- **Critical/P0**: Labels containing `critical`, `p0`
- **High/P1**: Labels containing `high-priority`, `p1`
- **Aging bugs**: `bug` label AND > 7 days old
- **Standard**: Everything else

**Output:** Prioritized issue table with links

### 1. `/investigate-bug {issue_number}`

Deep investigation of a GitHub issue to identify root cause, affected files, and scope boundaries.

**What it does:**
- Fetches issue details from GitHub
- Searches codebase for error locations
- Traces code paths and identifies root cause
- Defines what WILL and WON'T be modified
- Creates investigation report and posts to GitHub issue
- Adds "investigated" label

**Output:** Investigation report posted as GitHub issue comment

### 2. `/fix-planner {issue_number}`

Generates an actionable implementation plan from an investigation report.

**Prerequisite:** Must run `/investigate-bug` first

**What it does:**
- Extracts context from investigation report
- Creates detailed implementation steps with code snippets
- Defines testing strategy (unit, integration, manual)
- Includes data remediation scripts if needed
- Saves plan to `docs/fix-plans/FIX-{number}-plan.md`
- Posts plan to GitHub issue
- Adds "ready-to-implement" label

**Output:** Implementation plan posted as GitHub issue comment

### 2b. `/feature-planner {issue_number}`

Generates an actionable implementation plan from a feature request issue.

**What it does:**
- Extracts requirements from feature issue (acceptance criteria, use cases)
- Analyzes codebase for integration points and patterns
- Designs architecture (data model, server functions, UI components)
- Creates phased implementation steps with code snippets
- Defines testing strategy (unit, integration, manual)
- Saves plan to `docs/feature-plans/FEATURE-{number}-plan.md`
- Posts plan to GitHub issue
- Adds "planned" label

**Output:** Implementation plan posted as GitHub issue comment

### 3. `/implement-fix {issue_number}`

Executes code changes based on an approved fix plan.

**Prerequisite:** Must run `/fix-planner` first

**What it does:**
- Loads fix plan from docs or GitHub
- Creates isolated worktree: `~/GitHub/viper-metrics-worktrees/{number}-{name}`
- Creates branch: `fix-{number}-{description}`
- Implements each change from the plan
- Writes/updates tests as specified
- Runs test suite
- Creates data remediation scripts (but doesn't run them)
- Commits with structured message

**Output:** Committed changes in worktree, ready for PR

### 3b. `/implement-feature {issue_number}`

Executes code changes based on an approved feature plan.

**Prerequisite:** Must run `/feature-planner` first

**What it does:**
- Loads feature plan from docs or GitHub
- Confirms database changes were made in Anvil IDE (if required)
- Creates isolated worktree: `~/GitHub/viper-metrics-worktrees/{number}-{name}`
- Creates branch: `feature-{number}-{description}`
- Implements in phases: Data Layer → Server Layer → Client Layer → Integration
- Writes tests as specified
- Includes manual testing checkpoint
- Commits with structured message

**Output:** Committed changes in worktree, ready for PR

### 4. `/create-pr {issue_number}`

Creates a GitHub Pull Request from a completed implementation.

**Prerequisite:** Must run `/implement-fix` or `/implement-feature` first

**What it does:**
- Validates branch state (on fix branch, no uncommitted changes)
- Gathers context from issue and fix plan
- Generates comprehensive PR description
- Pushes branch and creates PR via `gh pr create`
- Links PR to original issue
- Updates issue labels

**Output:** Pull request URL

---

### `/get-session-logs {issue_number}`

Fetch and analyze Anvil session logs for a bug report that contains a session link.

**Prerequisites:** `ANVIL_AUTH_COOKIES` environment variable set

**What it does:**
- Extracts session ID from the GitHub issue body
- Fetches session logs from Anvil
- Analyzes user journey leading up to the error
- Displays forms visited, data accessed, and timing

**Output:** Formatted session analysis with user journey and raw logs

---

## Commands

Quick commands in `.claude/commands/` for common workflows:

### `/fix-bug {issue_number}`
Full workflow that handles investigation through PR creation in one session.
- Creates worktree immediately for complete isolation
- Triages bug complexity (trivial vs standard vs complex)
- Includes human review checkpoint before implementation

### `/investigate-bug {issue_number}` (command version)
Streamlined investigation that prepares everything for `/fix-bug`.

### `/create-bug`
Guided workflow to create a well-structured bug report issue.
- Gathers reproduction steps and expected behavior
- Investigates codebase for related code
- Creates comprehensive GitHub issue

### `/create-hotfix`
Create an urgent hotfix issue for critical production bugs.
- Streamlined for speed when production is down
- Marks issues with appropriate priority labels

## Workflow Examples

### Standard Bug Fix (Recommended)

```bash
# Step 0: See what needs attention
/issue-triage

# Step 1: Investigate the bug
/investigate-bug 142

# Step 2: Review investigation, then create plan
/fix-planner 142

# Step 3: Review plan, then implement
/implement-fix 142

# Step 4: Create PR
/create-pr 142
```

### Quick Bug Fix

```bash
# For simpler bugs, use the combined workflow
/fix-bug 142
```

### Feature Development

```bash
# Step 0: Create a well-structured feature issue (optional - skip if issue exists)
/create-feature "add bulk export for assets"

# Step 1: Create implementation plan for feature issue
/feature-planner 789

# Step 2: Review plan, complete any database changes in Anvil IDE, then implement
/implement-feature 789

# Step 3: Create PR
/create-pr 789
```

## Git Worktree Workflow

These skills use **git worktrees** for branch isolation, allowing you to work on multiple issues simultaneously without switching branches or stashing changes.

### Directory Structure

```
~/GitHub/viper-metrics-v2-0/                    # Main repo - stays on `published`
~/GitHub/viper-metrics-worktrees/
├── 657-switch-inspection-asset/                # Issue #657 worktree
├── 667-defect-pagination/                      # Issue #667 worktree
└── {issue-number}-{short-name}/                # New worktrees follow this pattern
```

### Common Worktree Commands

```bash
# List all worktrees
git worktree list

# Create new worktree for an issue (done automatically by skills)
git worktree add ~/GitHub/viper-metrics-worktrees/{issue}-{name} -b fix-{issue}-{name} origin/published

# Remove a worktree (after merging PR)
git worktree remove ~/GitHub/viper-metrics-worktrees/{issue}-{name}

# Prune stale worktree references
git worktree prune
```

### Why Worktrees?

- **Parallel development**: Work on multiple issues without context switching
- **Clean isolation**: Each issue has its own working directory
- **No stashing**: Leave work-in-progress in one worktree, switch to another
- **Shared git data**: All worktrees share the same `.git` objects and refs

## GitHub Integration

These skills require the GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Install GitHub CLI
brew install gh

# Authenticate
gh auth login
```

## Customization

Each skill can be customized for your project:

1. **Branch naming**: Edit `implement-fix.md` to change branch prefix
2. **PR template**: Edit `create-pr.md` to modify PR structure
3. **Labels**: Edit skills to use your project's label names
4. **Test commands**: Update test commands for your framework

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- Git repository with GitHub remote
- Python projects: `pytest` for test execution

## License

MIT - Feel free to use and modify for your projects.
