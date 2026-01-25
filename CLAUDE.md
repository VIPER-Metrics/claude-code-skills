# VIPER Ecosystem - Shared Context

This file provides cross-repository context for all VIPER applications. It is read automatically when working in any VIPER repo.

---

## Critical Rules

### Database Schema
- **NEVER modify data table schemas directly** - Always use the Anvil IDE
- Direct schema modifications can cause sync issues and data corruption
- To understand the database structure, read `viper-metrics-v2-0/anvil.yaml` under the `db_schema` section (160 tables)

### YAML Modifications
- Anvil.works has specific requirements for YAML structure
- **Always use the `/anvil-reference` command** before modifying form YAML files
- Never manually edit component `grid_position` values - let Anvil generate these

### Testing
- VS Code cannot run Anvil applications directly
- All testing must be done through the **Anvil IDE**
- Use the Anvil IDE's built-in debugger and console for troubleshooting

### Agent Usage
- **Use agents wherever possible** to preserve the main context window
- The main conversation should manage and coordinate sub-agents
- Available agents: `anvil-backend-specialist`, `anvil-client-yaml-specialist`, `code-reviewer`, `data-table-documenter`, `documentation-writer`, `maintenance-planner`, `mixpanel-analytics-optimizer`
- Delegate specialized tasks to appropriate agents rather than handling everything in the main context

### GitHub Issues
- **Always clarify which repo** when working on GitHub issues
- This workspace contains 4 repos with separate issue trackers:
  - `viper-metrics-v2-0` - Main web app issues
  - `viper-operator` - Operator app issues
  - `viper-inspect` - Inspect app issues
  - `claude-code-skills` - Shared tooling issues
- Ask: "Which repo is this issue in?" before running `gh issue view`

### Git Workflow
- **NEVER modify the `published` branch directly** - always create a feature branch
- **Always branch from `published`** - this is the main branch for all VIPER apps
- **Always pull before pushing** - changes may have been made in Anvil IDE
- **Branch naming**: Use simple names like `fix-bug-name` or `new-feature`
- **NEVER use slashes in branch names** - no `/` or `\` (e.g., `feat/new-feature` is NOT allowed)
  - Bad: `feat/new-feature`, `fix/bug-123`, `feature\update`
  - Good: `new-feature`, `fix-bug-123`, `feature-update`
- Anvil has strict requirements for branch names - slashes cause sync issues

---

## VIPER Ecosystem Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SHARED DATABASE                          │
│                    (Anvil Data Tables)                          │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ VIPER Metrics │◄───│VIPER Operator │    │ VIPER Inspect │
│   (Main App)  │    │ (Legacy App)  │    │  (New App)    │
│               │◄───┼───────────────┼────┤               │
│  - Web UI     │    │  - Offline    │    │  - Offline    │
│  - All CRUD   │    │  - Inspections│    │  - 2-way Sync │
│  - Sync APIs  │    │  - One-way    │    │  - Inspections│
│  - Reports    │    │    sync       │    │               │
└───────────────┘    └───────────────┘    └───────────────┘
     SERVER              CLIENT               CLIENT
```

### Repository Purposes

| Repo | Common Name | Purpose | Relationship |
|------|-------------|---------|--------------|
| `viper-metrics-v2-0` | **VIPER Metrics** | Main web application. All data management, reporting, and sync endpoints. The "server" for the ecosystem. | **Primary app** - all others depend on this |
| `viper-operator` | **VIPER Operator** | Offline-capable inspection app (legacy). Sends data TO Metrics endpoints. | Client → hits Metrics endpoints |
| `viper-inspect` | **VIPER Inspect** | Newer offline-capable inspection app with two-way sync. Better sync than Operator. | Client → hits Metrics endpoints |
| `claude-code-skills` | **Shared Config** | Claude Code skills, commands, and agents for sharing across projects. | Tooling only - not a VIPER app |

### Data Flow

1. **All three apps share the same database** (Anvil Data Tables)
2. **VIPER Metrics does the heavy lifting** - most data saving/manipulation happens on its server
3. **Operator & Inspect are clients** - they call endpoints on VIPER Metrics
4. **Sync endpoints** are defined in `viper-metrics-v2-0/server_code/InspectionsOTS/Sync_Endpoints.py`

### Key Sync Endpoints (on VIPER Metrics)

| Endpoint | Method | Used By |
|----------|--------|---------|
| `/new/sync-inspections` | POST | Operator, Inspect |
| `/new/sync-sections` | POST | Operator, Inspect |
| `/new/sync-defects` | POST | Operator, Inspect |
| `/new/upload-inspection-images` | POST | Operator, Inspect |
| `/new/upload-defect-images` | POST | Operator, Inspect |
| `/new/check-lookup-updates` | POST | Operator, Inspect |

---

## Cross-Repo Development Guidelines

### When Modifying Sync Endpoints (in Metrics)
1. Check both Operator and Inspect for compatibility
2. Sync endpoints must maintain backward compatibility
3. Test with both client apps before deploying

### When Modifying Client Apps (Operator/Inspect)
1. Verify the endpoint exists in VIPER Metrics
2. Check the expected request/response format
3. Handle offline scenarios gracefully

### When Adding New Features
1. Determine which app owns the feature
2. If it requires server logic → implement in VIPER Metrics
3. If it's client-only → implement in Operator or Inspect
4. If it needs sync → coordinate between repos

---

## Quick Reference

### Schema Location
```
viper-metrics-v2-0/anvil.yaml → db_schema section
```

### Anvil YAML Reference
```
/anvil-reference
```

### Bug Fixing Workflow
```
/investigate-bug {issue_number}
/fix-bug {issue_number}
```

---

## Tech Stack (All Apps)

- **Framework**: Anvil.works (Python full-stack)
- **Database**: Anvil Data Tables (shared across all apps)
- **Auth**: Microsoft, Google, Anvil users
- **UI Library**: anvil_extras (routing, authorization)
- **Offline**: Service workers (Operator, Inspect)

---

## Maintaining This Documentation

When updating this shared CLAUDE.md:
1. **Also update the individual repo CLAUDE.md files** if the change affects them
2. Repos to update: `viper-metrics-v2-0`, `viper-operator`, `viper-inspect`
3. Keep the shared context here, repo-specific details in each repo's CLAUDE.md

---

*This shared context applies to all VIPER repositories. Each repo has its own CLAUDE.md with repo-specific details.*
