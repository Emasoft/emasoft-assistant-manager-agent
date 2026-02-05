# Blocker Notification Templates

## Contents

- [1. When to notify the user about blockers](#1-when-to-notify-the-user-about-blockers)
- [2. Blocker notification message format](#2-blocker-notification-message-format)
- [3. Handling user response to blockers](#3-handling-user-response-to-blockers)
- [4. Timeout handling when user does not respond](#4-timeout-handling-when-user-does-not-respond)
- [5. Blocker resolution routing](#5-blocker-resolution-routing)

---

## 1. When to notify the user about blockers

### 1.1 Immediate notification required

Notify the user immediately when:
- A critical-path task is blocked and has a deadline within 48 hours
- Multiple tasks are blocked by the same issue (cascade blocker)
- The blocker requires user credentials, access, or authorization
- A RULE 14 requirement conflict is detected (requirement cannot be met as specified)

### 1.2 Batch notification (include in next status report)

Include in the next scheduled status report when:
- A non-critical task is blocked with no near-term deadline
- The blocker is a dependency on external work (another team, service, etc.)
- The blocker has been escalated but resolution is in progress

### 1.3 Do not notify

Do not notify the user when:
- The blocker is purely technical and agents can resolve it (retry, workaround)
- ECOS is handling agent replacement for a blocked agent
- EOA is coordinating between agents to resolve the blocker

---

## 2. Blocker notification message format

### 2.1 Standard blocker notification

When communicating a blocker to the user, use this format:

```
## Blocked Task Alert

**Task**: [Task title] (Issue #[number])
**Blocked Since**: [date/time]
**Severity**: [Critical/High/Medium]

### What's Blocked
[Clear, non-technical description of what cannot proceed]

### Why It's Blocked
[Root cause in user-friendly language]

### What We Need From You
[Specific, actionable request — what exactly the user must provide or decide]

### Options (if applicable)
1. **[Option A]**: [Description, trade-offs, impact]
2. **[Option B]**: [Description, trade-offs, impact]
3. **[Option C]**: [Description, trade-offs, impact]

**Recommended**: Option [N] because [reason]

### Impact if Unresolved
- [What other work is waiting]
- [Deadline at risk, if any]
- [Number of agents waiting]
```

### 2.2 Urgent blocker notification

For blockers with deadlines within 24 hours, prefix with:

```
## URGENT: Blocker Requires Immediate Decision

**Deadline**: [time remaining]
**Impact**: [what will be missed if not resolved]

[Standard blocker format follows]
```

### 2.3 Cascade blocker notification

When multiple tasks are blocked by the same issue:

```
## Cascade Blocker Alert

**Root Cause**: [Single issue causing multiple blocks]
**Tasks Affected**: [count] tasks across [count] agents
**Most Critical**: [Task name] (deadline: [date])

### Affected Tasks
| Task | Agent | Status | Deadline |
|------|-------|--------|----------|
| [task1] | [agent1] | Blocked | [date] |
| [task2] | [agent2] | Blocked | [date] |

### Resolution Needed
[What the user must do to unblock ALL affected tasks]
```

---

## 3. Handling user response to blockers

### 3.1 When user provides a decision

1. Acknowledge the user's response immediately
2. Route the decision to the appropriate agent:
   - If the blocker originated from EOA → Send AI Maestro message to EOA
   - If the blocker originated from ECOS → Send AI Maestro message to ECOS
3. Include the user's exact words in the routing message (do NOT paraphrase requirements — RULE 14)
4. Confirm to the user that the resolution has been routed

### 3.2 AI Maestro message template for routing resolution

```json
{
  "from": "eama-assistant-manager",
  "to": "[original-escalator]",
  "subject": "RESOLUTION: Blocker for task [task-id] resolved by user",
  "priority": "high",
  "content": {
    "type": "blocker-resolution",
    "message": "User has provided the following decision for the blocked task.",
    "task_uuid": "[task-uuid]",
    "issue_number": "[GitHub issue number]",
    "user_decision": "[Exact user response — do not modify per RULE 14]",
    "selected_option": "[If options were presented, which one was chosen]",
    "additional_context": "[Any extra information the user provided]",
    "resolved_at": "[ISO8601 timestamp]"
  }
}
```

### 3.3 When user asks for more information

If the user needs more details before deciding:
1. Route the question to the originating agent (EOA or ECOS) via AI Maestro
2. Await their response
3. Relay the additional information to the user
4. Do NOT make decisions on behalf of the user

---

## 4. Timeout handling when user does not respond

### 4.1 Escalation timeline for user response

| Duration | Action |
|----------|--------|
| 0-4 hours | Wait for user response |
| 4-8 hours | Send a gentle reminder with the original blocker summary |
| 8-24 hours | Send an urgent reminder highlighting deadline impact |
| 24-48 hours | If non-critical: note in status report that task remains blocked |
| 24-48 hours | If critical: escalate urgency, highlight what will be missed |
| >48 hours | Mark task as deferred, notify agents to work on other tasks |

### 4.2 Reminder message format

```
## Reminder: Pending Decision Needed

**Original Request**: [date/time]
**Task**: [Task title] (Issue #[number])
**Time Blocked**: [duration]

A decision is still needed for this blocked task.
[Brief summary of what's needed]

**Impact**: [What's waiting on this decision]
```

---

## 5. Blocker resolution routing

### 5.1 Decision tree for routing user's response

```
User provides blocker resolution
  │
  ├─ Was the blocker escalated by EOA?
  │   └─ YES → Route resolution to EOA via AI Maestro
  │
  ├─ Was the blocker escalated by ECOS?
  │   └─ YES → Route resolution to ECOS via AI Maestro
  │
  └─ Was the blocker detected in status report?
      └─ YES → Route to the relevant role agent via ECOS
```

### 5.2 Confirmation to user

After routing the resolution, confirm to the user:
```
Thank you. I've routed your decision to [agent/team].
The blocked task [Task title] should resume shortly.
I'll include the update in the next status report.
```

---

## See Also

- [ai-maestro-message-templates.md](../../eama-ecos-coordination/references/ai-maestro-message-templates.md) - Inter-agent message templates
- [response-templates.md](response-templates.md) - Standard response templates
