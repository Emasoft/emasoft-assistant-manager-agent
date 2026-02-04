---
name: eama-label-taxonomy
description: Use when managing GitHub issue labels for user requests, setting priorities, or reporting status to users. Covers priority and status label taxonomy. Trigger with `/eama-label-taxonomy`.
compatibility: Requires AI Maestro installed.
version: 1.0.0
---

# EAMA Label Taxonomy

## Overview

This skill provides the label taxonomy relevant to the Assistant Manager Agent (EAMA) role. Each role plugin has its own label-taxonomy skill covering the labels that role manages.

## Prerequisites

1. Access to GitHub CLI (`gh`) command
2. Repository with GitHub issue tracking enabled
3. Understanding of EAMA role responsibilities (user communication and role routing)
4. Familiarity with GitHub issue label syntax

## Instructions

Follow these steps to manage labels as EAMA:

1. **Analyze user request** to determine appropriate priority and type labels
2. **Create issue** with initial labels (`status:needs-triage`, `priority:*`, `type:*`)
3. **Monitor status changes** from other agents and translate to user-friendly messages
4. **Update priorities** when user expresses urgency or changes priority
5. **Set hold status** when user requests pause (`status:on-hold`)
6. **Report status** by querying issues with relevant labels
7. **Explain labels** to user in clear, non-technical language

**Checklist for label management**:

Copy this checklist and track your progress:

- [ ] Determine priority from user request context
- [ ] Apply appropriate type label (bug/feature/etc)
- [ ] Set initial status to `needs-triage`
- [ ] Monitor for status changes by other agents
- [ ] Update labels when user changes requirements
- [ ] Generate user-friendly status reports

---

## Labels EAMA Manages

### Priority Labels (`priority:*`)

**EAMA has authority to set and change priorities based on user input.**

| Label | Description | When EAMA Sets It |
|-------|-------------|-------------------|
| `priority:critical` | Must fix immediately | User reports production issue |
| `priority:high` | High priority | User emphasizes importance |
| `priority:normal` | Standard priority | Default for new issues |
| `priority:low` | Nice to have | User indicates low urgency |

**EAMA Priority Responsibilities:**
- Set initial priority based on user request
- Escalate priority when user expresses urgency
- De-escalate when user indicates reduced urgency

### Status Labels EAMA Updates

| Label | When EAMA Sets It |
|-------|------------------|
| `status:needs-triage` | When creating new issue from user request |
| `status:on-hold` | When user requests pause |

---

## Labels EAMA Monitors

### Status Labels (`status:*`)

EAMA reports status to user:
- `status:in-progress` - "Work has started on your request"
- `status:blocked` - "There's a blocker, may need your input"
- `status:needs-review` - "Code is ready for review"
- `status:done` - "Your request is complete"

### Assignment Labels (`assign:*`)

EAMA explains assignments to user:
- `assign:implementer-*` - "An AI agent is working on this"
- `assign:human` - "This needs human attention"
- `assign:orchestrator` - "The orchestrator is handling this"

---

## EAMA Label Commands

### When User Creates Request

```bash
# Create issue with initial labels
gh issue create \
  --title "$USER_REQUEST_TITLE" \
  --body "$USER_REQUEST_BODY" \
  --label "status:needs-triage" \
  --label "priority:$PRIORITY" \
  --label "type:$TYPE"
```

### When User Changes Priority

```bash
# Update priority
gh issue edit $ISSUE_NUMBER --remove-label "priority:normal" --add-label "priority:high"
```

### When User Puts on Hold

```bash
# Mark on hold
gh issue edit $ISSUE_NUMBER --remove-label "status:in-progress" --add-label "status:on-hold"
```

### When Generating Status Report

```bash
# Get all active issues for user
gh issue list --label "status:in-progress" --json number,title,labels

# Get blocked issues needing attention
gh issue list --label "status:blocked" --json number,title,labels

# Get completed issues
gh issue list --label "status:done" --state closed --json number,title
```

---

## User Communication Patterns

### Explaining Labels to User

When user asks "What's happening with my request?":

```markdown
**Issue #42: Add user authentication**

- **Status**: In Progress (`status:in-progress`)
- **Priority**: High (`priority:high`)
- **Assigned to**: Implementation Agent 1 (`assign:implementer-1`)
- **Type**: New Feature (`type:feature`)

The implementation agent is actively working on this task.
```

### Translating User Requests to Labels

| User Says | Labels to Apply |
|-----------|-----------------|
| "This is urgent!" | `priority:critical` |
| "When you get a chance..." | `priority:low` |
| "Something is broken" | `type:bug`, `priority:high` |
| "Can you add..." | `type:feature` |
| "Put this on hold" | `status:on-hold` |
| "Resume this" | Remove `status:on-hold`, add `status:ready` |

---

## Quick Reference

### EAMA Label Responsibilities

| Action | Labels Involved |
|--------|-----------------|
| Create issue | `status:needs-triage`, `priority:*`, `type:*` |
| Change priority | Update `priority:*` |
| Pause work | Add `status:on-hold` |
| Resume work | Remove `status:on-hold` |
| Report to user | Read all labels for status |

### Labels EAMA Never Sets

- `assign:*` - Set by EOA/ECOS
- `review:*` - Managed by EIA
- `effort:*` - Set by EOA during triage
- `component:*` - Set by EOA/EAA

### EAMA's Approval Authority

EAMA can approve:
- Priority changes requested by other agents
- Scope changes that affect user expectations
- Deadline/milestone changes

EAMA must approve:
- Any change to `priority:critical`
- Reassignment to `assign:human`
- Project-level decisions

---

## Output

| Output Type | Format | When Generated |
|-------------|--------|----------------|
| Issue creation | GitHub issue URL with labels | When user creates new request |
| Label update confirmation | "Priority updated to high" | When labels modified |
| Status report | Markdown table of issues and labels | When user requests status |
| Label explanation | Plain text translation of label meaning | When user asks "what's happening?" |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Label not found | Typo or label doesn't exist in repo | Create label or fix typo |
| Permission denied | Insufficient GitHub permissions | Request repo access from user |
| Issue not found | Invalid issue number | Verify issue number with user |
| Conflicting labels | Multiple priority labels applied | Remove old label before adding new |
| API rate limit | Too many GitHub API calls | Wait and retry, batch operations |

## Examples

### Example 1: Creating Issue with Labels

**User request**: "The login page is broken, fix it urgently!"

**EAMA actions**:
```bash
gh issue create \
  --title "Login page broken" \
  --body "User reported urgent login page issue" \
  --label "type:bug" \
  --label "priority:critical" \
  --label "status:needs-triage"
```

**User response**: "Created issue #123 with critical priority. The orchestrator will triage this shortly."

### Example 2: Reporting Status with Labels

**User request**: "What's the status of my authentication work?"

**EAMA actions**:
```bash
gh issue list --label "component:auth" --json number,title,labels
```

**User response**:
```markdown
**Authentication Issues**:

- **#42**: Add OAuth support
  - Status: In Progress (`status:in-progress`)
  - Priority: High (`priority:high`)
  - Assigned to: Implementation Agent 1

- **#45**: Fix password reset
  - Status: Blocked (`status:blocked`)
  - Priority: Normal (`priority:normal`)
  - Blocker: Waiting for email service setup
```

### Example 3: Updating Priority

**User request**: "Actually, make that password reset high priority too."

**EAMA actions**:
```bash
gh issue edit 45 --remove-label "priority:normal" --add-label "priority:high"
```

**User response**: "Priority updated to high for issue #45."

---

## Resources

- **AGENT_OPERATIONS.md** - Core agent operational patterns
- **eama-status-reporting** - User communication patterns
- **eama-user-communication** - Communication style guidelines
- **eama-role-routing** - Role delegation patterns
