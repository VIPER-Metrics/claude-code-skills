# Claude Code Skills

A comprehensive set of Claude Code skills, commands, and agents for Anvil.works development and bug fixing workflows.

## Overview

These skills form a complete bug-fixing pipeline that integrates with GitHub Issues and Pull Requests:

```
@issue-triage → @investigate-bug → @fix-planner → @implement-fix → @create-pr
      ↓               ↓                 ↓               ↓               ↓
  Prioritizes     Posts report      Posts plan     Commits code    Opens PR
  open issues     to issue          to issue       to branch       on GitHub
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
    ├── fix-planner.md
    ├── implement-fix.md
    ├── investigate-bug.md
    ├── agents/
    │   ├── anvil-backend-specialist.md
    │   ├── anvil-client-yaml-specialist.md
    │   ├── code-reviewer.md
    │   ├── data-table-documenter.md
    │   ├── documentation-writer.md
    │   ├── maintenance-planner.md
    │   └── mixpanel-analytics-optimizer.md
    ├── commands/
    │   ├── anvil-reference.md
    │   ├── fix-bug.md
    │   └── investigate-bug.md
    └── skills/
        └── issue-triage/
            ├── SKILL.md
            └── scripts/
                └── generate_report.py
```

## Skills

### 0. `/issue-triage`

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

### 3. `/implement-fix {issue_number}`

Executes code changes based on an approved fix plan.

**Prerequisite:** Must run `/fix-planner` first

**What it does:**
- Loads fix plan from docs or GitHub
- Creates feature branch: `fix/issue-{number}-{description}`
- Implements each change from the plan
- Writes/updates tests as specified
- Runs test suite
- Creates data remediation scripts (but doesn't run them)
- Commits with structured message

**Output:** Committed changes on feature branch

### 4. `/create-pr {issue_number}`

Creates a GitHub Pull Request from a completed fix implementation.

**Prerequisite:** Must run `/implement-fix` first

**What it does:**
- Validates branch state (on fix branch, no uncommitted changes)
- Gathers context from issue and fix plan
- Generates comprehensive PR description
- Pushes branch and creates PR via `gh pr create`
- Links PR to original issue
- Updates issue labels

**Output:** Pull request URL

## Agents

Specialized agents in `.claude/agents/` handle domain-specific tasks:

| Agent | Purpose |
|-------|---------|
| `anvil-backend-specialist` | Server modules, database queries, security controls, `q.fetch_only()` optimization |
| `anvil-client-yaml-specialist` | Form YAML modifications, UI components, data bindings, event handlers |
| `code-reviewer` | Security review, formatting checks, breaking change detection |
| `data-table-documenter` | Database schema documentation after changes |
| `documentation-writer` | Feature documentation, What's New content |
| `maintenance-planner` | Heavy equipment maintenance workflow design |
| `mixpanel-analytics-optimizer` | Analytics tracking via Segment/Mixpanel |

**Usage**: Agents are invoked automatically by Claude Code when appropriate, or can be triggered via the Task tool.

## Quick Commands

For simpler workflows, these commands in `.claude/commands/` combine multiple steps:

### `/fix-bug {issue_number}`
Full workflow agent that handles investigation through PR creation in one session.
- Creates branch immediately for isolation
- Triages bug complexity (trivial vs standard vs complex)
- Includes human review checkpoint before implementation
- Runs specialist agent reviews when appropriate

### `/investigate-bug {issue_number}` (command version)
Streamlined investigation that prepares everything for `/fix-bug`.

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
