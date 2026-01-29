---
description: Status report generation for cross-role coordination
context: fork
agent: eama-report-generator
user-invocable: true
triggers:
  - when user asks for status
  - when generating progress reports
  - when summarizing work across roles
---

# Status Reporting Skill

## Purpose

Generate comprehensive status reports showing progress across all roles (Architect, Orchestrator, Integrator).

## Report Types

| Type | Frequency | Content |
|------|-----------|---------|
| Quick Status | On demand | Current state summary |
| Progress Report | Daily/Weekly | Work completed, in progress, blocked |
| Handoff Summary | On transition | What was handed to whom |
| Blocker Report | As needed | What's blocking progress |

## Report Generation Workflow

1. Query each role via AI Maestro for current status
2. Query GitHub for issue/PR status
3. Read session memory files
4. Compile into unified report
5. Format for user consumption

## Report Sections

### Quick Status Format
- Current active task
- % complete estimate
- Next milestone
- Blockers (if any)

### Progress Report Format
- Period covered
- Tasks completed (with evidence)
- Tasks in progress (with estimates)
- Tasks blocked (with reasons)
- Tasks added (new scope)
- Risks identified

## Output Location

Reports saved to: `docs_dev/reports/status-{date}.md`

## Related Skills

- eama-role-routing (role status queries)
- eama-approval-workflows (approval status)
- eama-shared (session memory access)
