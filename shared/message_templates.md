# AI Maestro Message Templates

Standard message formats for inter-role communication via AI Maestro.

## Message Types

### 1. Task Assignment

```json
{
  "to": "{target-agent-session}",
  "subject": "[TASK] {brief_description}",
  "priority": "high",
  "content": {
    "type": "task_assignment",
    "message": "{detailed_instructions}",
    "handoff_file": "docs_dev/handoffs/handoff-{uuid}-eama-to-{role}.md",
    "github_issue": "#{issue_number}",
    "deadline": "{ISO-8601 timestamp or null}"
  }
}
```

### 2. Status Request

```json
{
  "to": "{target-agent-session}",
  "subject": "[STATUS] Request for {project/task}",
  "priority": "normal",
  "content": {
    "type": "status_request",
    "message": "Please provide status update on {task_description}",
    "fields_requested": ["progress_percent", "blockers", "eta", "next_steps"]
  }
}
```

### 3. Status Update

```json
{
  "to": "eama-session",
  "subject": "[UPDATE] {task_name} - {status}",
  "priority": "normal",
  "content": {
    "type": "status_update",
    "message": "{summary}",
    "progress_percent": 75,
    "blockers": ["blocker1", "blocker2"],
    "completed_items": ["item1", "item2"],
    "next_steps": ["step1", "step2"],
    "eta": "{ISO-8601 timestamp}"
  }
}
```

### 4. Completion Signal

```json
{
  "to": "eama-session",
  "subject": "[COMPLETE] {task_name}",
  "priority": "high",
  "content": {
    "type": "completion",
    "message": "{summary_of_deliverables}",
    "handoff_file": "docs_dev/handoffs/handoff-{uuid}-{role}-to-eama.md",
    "github_issue": "#{issue_number}",
    "artifacts": ["path/to/artifact1", "path/to/artifact2"],
    "verification_status": "passed" | "failed" | "partial"
  }
}
```

### 5. Approval Request

```json
{
  "to": "eama-session",
  "subject": "[APPROVAL] {approval_type} for {item}",
  "priority": "high",
  "content": {
    "type": "approval_request",
    "message": "{description_of_what_needs_approval}",
    "approval_type": "push" | "merge" | "publish" | "security" | "release",
    "affected_items": ["item1", "item2"],
    "risk_assessment": "low" | "medium" | "high",
    "rollback_plan": "{description}"
  }
}
```

### 6. Approval Response

```json
{
  "to": "{requesting-agent-session}",
  "subject": "[APPROVED/REJECTED] {approval_type} for {item}",
  "priority": "high",
  "content": {
    "type": "approval_response",
    "message": "{user_feedback_if_any}",
    "decision": "approved" | "rejected" | "needs_revision",
    "conditions": ["condition1", "condition2"],
    "user_comment": "{optional_user_comment}"
  }
}
```

### 7. Question / Clarification

```json
{
  "to": "eama-session",
  "subject": "[QUESTION] {brief_topic}",
  "priority": "normal",
  "content": {
    "type": "question",
    "message": "{detailed_question}",
    "context": "{relevant_context}",
    "options": ["option1", "option2"],
    "blocking": true | false
  }
}
```

### 8. Error / Issue Report

```json
{
  "to": "eama-session",
  "subject": "[ERROR] {error_type} in {component}",
  "priority": "urgent",
  "content": {
    "type": "error_report",
    "message": "{error_description}",
    "error_type": "build_failure" | "test_failure" | "integration_issue" | "blocker",
    "affected_components": ["component1", "component2"],
    "attempted_solutions": ["solution1", "solution2"],
    "needs_user_input": true | false
  }
}
```

## Session Name Convention

| Role | Prefix | Session Name Pattern |
|------|--------|---------------------|
| Assistant Manager | `eama-` | `eama-{project}-session` |
| Architect | `eaa-` | `eaa-{project}-session` |
| Orchestrator | `eoa-` | `eoa-{project}-session` |
| Integrator | `eia-` | `eia-{project}-session` |

**Prefix Legend:**
- `e` = Emasoft (author identifier)
- `ama` = Assistant Manager Agent
- `aa` = Architect Agent
- `oa` = Orchestrator Agent
- `ia` = Integrator Agent

## Priority Levels

| Priority | Use Case |
|----------|----------|
| `urgent` | Blocking issues, critical errors, security issues |
| `high` | Completion signals, approval requests, important updates |
| `normal` | Status updates, questions, routine communication |
| `low` | Non-blocking information, FYI messages |
