# AI Maestro Message Formats for ECOS Communication

## Use-Case TOC

- When formatting an approval request from ECOS -> Section 1
- When formatting an approval response from EAMA -> Section 2
- When formatting an autonomy grant/revoke message -> Section 3
- When formatting a completion notification -> Section 4

## Table of Contents

1. ECOS Approval Request Format
2. EAMA Response Format
3. Autonomy Messages
4. Completion Notification Format

---

## 1. ECOS Approval Request Format

This is the format ECOS uses when sending approval requests to EAMA:

```json
{
  "from": "ecos",
  "to": "eama",
  "subject": "ECOS Approval Request: {operation_summary}",
  "priority": "high|normal",
  "content": {
    "type": "approval-request",
    "request_id": "ecos-req-{uuid}",
    "category": "critical-operation|policy-exception|etc",
    "operation": {
      "type": "deployment|merge|publish|etc",
      "description": "Detailed description of the operation",
      "affected_resources": ["list", "of", "resources"],
      "risk_level": "low|medium|high|critical",
      "reversible": true|false
    },
    "context": {
      "triggered_by": "role or event that initiated",
      "related_issues": ["#123", "#456"],
      "related_handoffs": ["handoff-uuid"]
    },
    "recommendation": "ECOS recommendation: approve|reject|needs-review",
    "requested_at": "ISO-8601"
  }
}
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `request_id` | Unique identifier for tracking |
| `category` | Operation category (see request categories in SKILL.md) |
| `operation.type` | What kind of operation |
| `operation.risk_level` | Risk assessment |
| `operation.reversible` | Can the operation be undone |
| `context.triggered_by` | Which role or event initiated this |
| `recommendation` | ECOS's own recommendation |

---

## 2. EAMA Response Format

See [approval-response-workflow.md](approval-response-workflow.md) for the full response format and workflow.

---

## 3. Autonomy Messages

### Grant Message

```json
{
  "to": "ecos",
  "subject": "EAMA Autonomous Mode Grant",
  "priority": "high",
  "content": {
    "type": "autonomy-grant",
    "operation_types": ["routine-operation", "minor-decision"],
    "expires_at": "ISO-8601",
    "scope_limits": {
      "max_files_per_operation": 50,
      "allowed_branches": ["feature/*"]
    },
    "notification_level": "important"
  }
}
```

### Revoke Message

```json
{
  "to": "ecos",
  "subject": "EAMA Autonomous Mode Revoked",
  "priority": "urgent",
  "content": {
    "type": "autonomy-revoke",
    "reason": "User request|Scope exceeded|Security concern|Timeout",
    "effective_immediately": true,
    "revoked_at": "ISO-8601"
  }
}
```

See [delegation-rules.md](delegation-rules.md) for full details on autonomy configuration.

---

## 4. Completion Notification Format

This is the format ECOS uses when reporting completed operations:

```json
{
  "from": "ecos",
  "to": "eama",
  "subject": "ECOS Operation Complete: {operation_summary}",
  "priority": "normal",
  "content": {
    "type": "operation-complete",
    "request_id": "ecos-req-{uuid}|autonomous-{uuid}",
    "operation": {
      "type": "deployment|merge|publish|etc",
      "description": "What was completed",
      "result": "success|partial|failed",
      "details": "Summary of outcome"
    },
    "autonomous_mode": true|false,
    "completed_at": "ISO-8601"
  }
}
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `request_id` | Matches original request ID or `autonomous-{uuid}` for autonomous ops |
| `operation.result` | Outcome of the operation |
| `operation.details` | Summary of what happened |
| `autonomous_mode` | Whether this was done under autonomous mode |
