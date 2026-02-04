# ECOS Coordination Examples

## Use-Case TOC

- When handling a deployment approval request -> Example 1
- When granting autonomous mode for development -> Example 2
- When processing a completion notification -> Example 3

## Table of Contents

1. Example 1: ECOS Requests Approval for Deployment
2. Example 2: Granting Autonomous Mode for Development Tasks
3. Example 3: ECOS Reports Completion

---

## Example 1: ECOS Requests Approval for Deployment

This example shows the complete flow of ECOS requesting approval for a staging deployment.

### ECOS sends approval request

```json
{
  "from": "ecos",
  "to": "eama",
  "subject": "ECOS Approval Request: Deploy v2.1.0 to staging",
  "priority": "high",
  "content": {
    "type": "approval-request",
    "request_id": "ecos-req-a1b2c3d4",
    "category": "routine-operation",
    "operation": {
      "type": "deployment",
      "description": "Deploy version 2.1.0 to staging environment",
      "affected_resources": ["staging-server", "staging-db"],
      "risk_level": "medium",
      "reversible": true
    },
    "context": {
      "triggered_by": "eoa",
      "related_issues": ["#89", "#92"]
    },
    "recommendation": "approve",
    "requested_at": "2025-02-02T14:30:00Z"
  }
}
```

### EAMA evaluates the request

EAMA checks:
- Category: `routine-operation` - delegatable but not currently delegated
- Risk: `medium` - acceptable for staging
- Reversible: `true` - can rollback if needed
- ECOS recommendation: `approve`

### EAMA responds with approval

```json
{
  "to": "ecos",
  "subject": "EAMA Approval Response: ecos-req-a1b2c3d4",
  "priority": "high",
  "content": {
    "type": "approval-response",
    "request_id": "ecos-req-a1b2c3d4",
    "decision": "approved",
    "comment": "Proceed with staging deployment",
    "responded_at": "2025-02-02T14:32:00Z"
  }
}
```

---

## Example 2: Granting Autonomous Mode for Development Tasks

This example shows how to grant ECOS autonomous mode for a 4-hour development session.

### User request

User tells EAMA: "Let ECOS handle routine development tasks for the next 4 hours"

### EAMA sends autonomy grant

```json
{
  "to": "ecos",
  "subject": "EAMA Autonomous Mode Grant",
  "priority": "high",
  "content": {
    "type": "autonomy-grant",
    "operation_types": ["routine-operation", "minor-decision"],
    "expires_at": "2025-02-02T22:00:00Z",
    "scope_limits": {
      "max_files_per_operation": 100,
      "allowed_branches": ["feature/*", "fix/*"]
    },
    "notification_level": "important"
  }
}
```

### What ECOS can now do autonomously

- Implement features on feature/* branches
- Fix bugs on fix/* branches
- Make minor decisions without asking
- Modify up to 100 files per operation

### What ECOS still needs approval for

- Production deployments
- Security changes
- Data deletion
- External communications
- Any operation not in `routine-operation` or `minor-decision` categories

---

## Example 3: ECOS Reports Completion

This example shows an autonomous operation completion notification.

### ECOS sends completion notification

```json
{
  "from": "ecos",
  "to": "eama",
  "subject": "ECOS Operation Complete: Feature implementation",
  "priority": "normal",
  "content": {
    "type": "operation-complete",
    "request_id": "autonomous-x1y2z3",
    "operation": {
      "type": "implementation",
      "description": "Implemented user profile page components",
      "result": "success",
      "details": "Created 5 components, 12 tests passing"
    },
    "autonomous_mode": true,
    "completed_at": "2025-02-02T16:45:00Z"
  }
}
```

### EAMA processes the notification

1. **Verify scope**: Implementation was within granted `routine-operation` scope
2. **Log for audit**: Record in `ecos_audit_log`
3. **User notification**: Since `notification_level` is `important` and this is a success, aggregate for status report rather than immediate notification

### State update

```yaml
ecos_audit_log:
  - timestamp: "2025-02-02T16:45:00Z"
    event_type: "complete"
    request_id: "autonomous-x1y2z3"
    details: "Autonomous implementation: user profile page components - success"
    user_involved: false
```
