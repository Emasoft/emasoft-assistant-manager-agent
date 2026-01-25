# Handoff Document Template

This template defines the standard format for handoff documents between roles in the 4-plugin architecture.

## Plugin Prefixes

| Plugin | Prefix | Full Name |
|--------|--------|-----------|
| Assistant Manager | `eama-` | Emasoft Assistant Manager Agent |
| Architect | `eaa-` | Emasoft Architect Agent |
| Orchestrator | `eoa-` | Emasoft Orchestrator Agent |
| Integrator | `eia-` | Emasoft Integrator Agent |

## Handoff File Format

```yaml
---
uuid: "handoff-{uuid}"
from_role: "eama" | "eaa" | "eoa" | "eia"
to_role: "eama" | "eaa" | "eoa" | "eia"
created: "ISO-8601 timestamp"
github_issue: "#issue_number"  # Optional
subject: "Brief description"
priority: "urgent" | "high" | "normal" | "low"
requires_ack: true | false
status: "pending" | "acknowledged" | "completed" | "rejected"
---

## Context

[Background information and context for this handoff]

## Requirements / Deliverables

[What needs to be done or what is being delivered]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies

- Depends on: [list of dependencies]
- Blocks: [list of blocked items]

## Notes

[Additional notes or considerations]
```

## Communication Hierarchy

```
USER <-> EAMA (Assistant Manager) <-> EAA (Architect)
                                  <-> EOA (Orchestrator)
                                  <-> EIA (Integrator)
```

**CRITICAL**: Architect (eaa-), Orchestrator (eoa-), and Integrator (eia-) do NOT communicate directly with each other. All communication flows through Assistant Manager (eama-).

## Handoff Types

### 1. User Request -> Role Assignment
- From: eama (assistant-manager)
- To: eaa | eoa | eia
- Purpose: Route user request to appropriate specialist

### 2. Design Complete -> Orchestration
- From: eaa (via eama)
- To: eoa (via eama)
- Purpose: Hand off approved design for implementation

### 3. Implementation Complete -> Integration
- From: eoa (via eama)
- To: eia (via eama)
- Purpose: Signal work ready for quality gates

### 4. Quality Gate Results -> User
- From: eia (via eama)
- To: user
- Purpose: Report integration status and request approvals

## File Naming Convention

```
handoff-{uuid}-{from}-to-{to}.md

Examples:
- handoff-a1b2c3d4-eama-to-eaa.md    # AM assigns to Architect
- handoff-e5f6g7h8-eaa-to-eama.md    # Architect reports to AM
- handoff-i9j0k1l2-eama-to-eoa.md    # AM assigns to Orchestrator
- handoff-m3n4o5p6-eoa-to-eama.md    # Orchestrator reports to AM
- handoff-q7r8s9t0-eama-to-eia.md    # AM assigns to Integrator
- handoff-u1v2w3x4-eia-to-eama.md    # Integrator reports to AM
```

## Storage Location

All handoff files are stored in: `docs_dev/handoffs/`
