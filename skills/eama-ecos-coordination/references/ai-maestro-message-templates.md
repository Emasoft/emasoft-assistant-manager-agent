# AI Maestro Message Templates for EAMA

**Reference for**: `eama-ecos-coordination` skill

This document provides all curl command templates and message formats for AI Maestro inter-agent communication between EAMA and other agents (ECOS, EAA, EOA, EIA).

---

## Contents

- [1. Receiving Messages](#1-receiving-messages)
  - [1.1 Receiving approval requests from ECOS](#11-receiving-approval-requests-from-ecos)
  - [1.2 Receiving status reports from ECOS](#12-receiving-status-reports-from-ecos)
  - [1.3 Receiving health check responses (pong)](#13-receiving-health-check-responses-pong)
- [2. Sending Approval-Related Messages](#2-sending-approval-related-messages)
  - [2.1 Sending approval decisions to ECOS (approve/deny/defer)](#21-sending-approval-decisions-to-ecos-approvedenydefer)
  - [2.2 Notifying ECOS of user decisions after escalation](#22-notifying-ecos-of-user-decisions-after-escalation)
- [3. Requesting Information from ECOS](#3-requesting-information-from-ecos)
  - [3.1 Requesting status from ECOS](#31-requesting-status-from-ecos)
  - [3.2 Sending health check pings to verify ECOS is alive](#32-sending-health-check-pings-to-verify-ecos-is-alive)
- [4. Delegating Work to ECOS](#4-delegating-work-to-ecos)
  - [4.1 Routing user work requests to ECOS for specialist delegation](#41-routing-user-work-requests-to-ecos-for-specialist-delegation)
  - [4.2 Routing design work to EAA via ECOS](#42-routing-design-work-to-eaa-via-ecos)
  - [4.3 Routing implementation work to EOA via ECOS](#43-routing-implementation-work-to-eoa-via-ecos)
  - [4.4 Routing review/integration work to EIA via ECOS](#44-routing-reviewintegration-work-to-eia-via-ecos)
- [5. Standard AI Maestro API Patterns](#5-standard-ai-maestro-api-patterns)
  - [5.1 Base API format and authentication](#51-base-api-format-and-authentication)
  - [5.2 Message content structure requirements](#52-message-content-structure-requirements)
  - [5.3 Priority levels and when to use them](#53-priority-levels-and-when-to-use-them)

---

## 1. Receiving Messages

### 1.1 Receiving approval requests from ECOS

**Use this when**: ECOS requests permission for a critical operation

**Incoming message format** (what you receive from ECOS):
```json
{
  "from": "ecos-<project-name>",
  "to": "eama-assistant-manager",
  "subject": "Approval Request: <REQUEST-ID>",
  "priority": "high",
  "content": {
    "type": "approval_request",
    "request_id": "<unique-id>",
    "operation": "<description of operation>",
    "risk_level": "low|medium|high",
    "justification": "<why ECOS needs this>",
    "impact": "<what will happen>",
    "reversible": true|false
  }
}
```

**How to read it**:
```bash
curl "$AIMAESTRO_API/api/messages?agent=eama-assistant-manager&action=list&status=unread" | jq '.[] | select(.content.type == "approval_request")'
```

**Response actions**:
- Assess risk level
- Make approval decision (approve/deny/defer)
- See section 2.1 for sending approval decision back to ECOS

---

### 1.2 Receiving status reports from ECOS

**Use this when**: You requested status and ECOS responds

**Incoming message format** (what you receive):
```json
{
  "from": "ecos-<project-name>",
  "to": "eama-assistant-manager",
  "subject": "Status Report",
  "priority": "normal",
  "content": {
    "type": "status_report",
    "overall_progress": "67%",
    "active_tasks": [
      {"specialist": "EOA", "task": "Implement REST API", "status": "in_progress"},
      {"specialist": "EIA", "task": "Code review", "status": "completed"}
    ],
    "blockers": [
      {"description": "Waiting for OAuth keys", "assigned_to": "DevOps"}
    ],
    "next_milestone": "API v1.0 complete",
    "health": "green|yellow|red"
  }
}
```

**How to read it**:
```bash
curl "$AIMAESTRO_API/api/messages?agent=eama-assistant-manager&action=list&status=unread" | jq '.[] | select(.content.type == "status_report")'
```

**Response actions**:
- Parse status information
- Format for user presentation
- Present to user with clear progress indicators

---

### 1.3 Receiving health check responses (pong)

**Use this when**: You sent a health check ping and ECOS responds

**Expected response format**:
```json
{
  "from": "ecos-<project-name>",
  "to": "eama-assistant-manager",
  "subject": "Re: Health Check",
  "content": {
    "type": "pong",
    "status": "alive",
    "uptime": "<seconds since spawn>",
    "active_specialists": ["EOA", "EIA"]
  }
}
```

**How to read it**:
```bash
curl "$AIMAESTRO_API/api/messages?agent=eama-assistant-manager&action=list&status=unread" | jq '.[] | select(.content.type == "pong")'
```

**Response actions**:
- Verify "status": "alive"
- Update session health status in logs
- If no response within 30 seconds, retry once, then report to user

---

## 2. Sending Approval-Related Messages

### 2.1 Sending approval decisions to ECOS (approve/deny/defer)

**Use this when**: Responding to ECOS approval request

**Outgoing message format** (your response to ECOS):
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "Approval Decision: <REQUEST-ID>",
    "priority": "high",
    "content": {
      "type": "approval_decision",
      "request_id": "<same-id-from-request>",
      "decision": "approve|deny|defer",
      "reason": "<explanation of decision>",
      "conditions": "<any conditions for approval, if applicable>",
      "approved_by": "eama|user",
      "user_quote": "<exact user statement if user approved>"
    }
  }'
```

**Decision values**:
- `approve`: Operation authorized, proceed
- `deny`: Operation rejected, do not proceed
- `defer`: Need more information, request clarification

**Example (autonomous approval)**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "Approval Decision: RUN-TESTS-001",
    "priority": "high",
    "content": {
      "type": "approval_decision",
      "request_id": "RUN-TESTS-001",
      "decision": "approve",
      "reason": "Routine operation, low risk, aligns with testing workflow",
      "approved_by": "eama"
    }
  }'
```

**Example (user-escalated denial)**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "Approval Decision: DELETE-DATA-002",
    "priority": "high",
    "content": {
      "type": "approval_decision",
      "request_id": "DELETE-DATA-002",
      "decision": "deny",
      "reason": "User denied: operation is destructive and irreversible",
      "approved_by": "user",
      "user_quote": "No, do not delete. Archive instead."
    }
  }'
```

---

### 2.2 Notifying ECOS of user decisions after escalation

**Use this when**: You escalated a request to the user and got their decision

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "User Decision: <REQUEST-ID>",
    "priority": "urgent",
    "content": {
      "type": "user_decision",
      "request_id": "<REQUEST-ID>",
      "decision": "approve|deny",
      "user_statement": "<exact quote from user>",
      "timestamp": "<ISO-8601 timestamp>",
      "context": "<any additional context from user>"
    }
  }'
```

**Example**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "User Decision: DEPLOY-PROD-001",
    "priority": "urgent",
    "content": {
      "type": "user_decision",
      "request_id": "DEPLOY-PROD-001",
      "decision": "approve",
      "user_statement": "Yes, deploy to production",
      "timestamp": "2026-02-05T14:30:00Z",
      "context": "User verified all tests passing and code review complete"
    }
  }'
```

---

## 3. Requesting Information from ECOS

### 3.1 Requesting status from ECOS

**Use this when**: User asks for project status

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "Status Query",
    "priority": "normal",
    "content": {
      "type": "status_query",
      "scope": "full|milestone|task",
      "details": "<what user asked for>",
      "format": "summary|detailed",
      "timeout": 30
    }
  }'
```

**Example**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "Status Query",
    "priority": "normal",
    "content": {
      "type": "status_query",
      "scope": "full",
      "details": "User asked: What is the status of the API implementation?",
      "format": "summary",
      "timeout": 30
    }
  }'
```

**Expected response**: See section 1.2 (Receiving status reports from ECOS)

---

### 3.2 Sending health check pings to verify ECOS is alive

**Use this when**: Verifying ECOS is responsive (after spawn, periodically, before delegating work)

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "Health Check",
    "priority": "normal",
    "content": {
      "type": "ping",
      "message": "Verify ECOS alive",
      "expect_reply": true,
      "timeout": 10
    }
  }'
```

**Example**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "Health Check",
    "priority": "normal",
    "content": {
      "type": "ping",
      "message": "Verify ECOS alive",
      "expect_reply": true,
      "timeout": 10
    }
  }'
```

**Expected response**: See section 1.3 (Receiving health check responses)

---

## 4. Delegating Work to ECOS

### 4.1 Routing user work requests to ECOS for specialist delegation

**Use this when**: User gives a work request that should be handled by a specialist (EOA, EAA, EIA) via ECOS

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "User Request: <brief summary>",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EOA|EAA|EIA",
      "task": "<detailed task description>",
      "user_context": "<relevant background>",
      "priority": "high|normal|low",
      "deadline": "<if specified>",
      "success_criteria": "<user expectations>"
    }
  }'
```

**Example**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "User Request: Implement REST API",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EOA",
      "task": "Build a REST API for inventory management with CRUD operations",
      "user_context": "User wants full inventory tracking system with authentication",
      "priority": "high",
      "success_criteria": "REST API with all CRUD endpoints, authentication, tests passing"
    }
  }'
```

---

### 4.2 Routing design work to EAA via ECOS

**Use this when**: User requests architecture/design work

**Specialist routing**: `"specialist": "EAA"` (Architect)

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "User Request: <design task summary>",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EAA",
      "task": "<architecture/design task>",
      "user_context": "<relevant requirements>",
      "priority": "normal",
      "success_criteria": "<design deliverables expected>"
    }
  }'
```

**Example**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-data-pipeline",
    "subject": "User Request: Design data pipeline architecture",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EAA",
      "task": "Design architecture for real-time data pipeline processing 1M events/day",
      "user_context": "Need to process IoT sensor data from 10k devices, store in time-series DB, expose via API",
      "priority": "high",
      "success_criteria": "Architecture document with component diagrams, data flow, scalability plan"
    }
  }'
```

---

### 4.3 Routing implementation work to EOA via ECOS

**Use this when**: User requests building/implementing features

**Specialist routing**: `"specialist": "EOA"` (Orchestrator)

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "User Request: <implementation task summary>",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EOA",
      "task": "<implementation task>",
      "user_context": "<relevant requirements>",
      "priority": "high",
      "success_criteria": "<working implementation expected>"
    }
  }'
```

**Example**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "User Request: Build REST API",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EOA",
      "task": "Implement REST API with CRUD operations for inventory items",
      "user_context": "Database schema already designed. Need endpoints for: create item, update item, delete item, list items, search items.",
      "priority": "high",
      "success_criteria": "All endpoints working, tests passing, documented with OpenAPI spec"
    }
  }'
```

---

### 4.4 Routing review/integration work to EIA via ECOS

**Use this when**: User requests code review, testing, merging, or release

**Specialist routing**: `"specialist": "EIA"` (Integrator)

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-<project-name>",
    "subject": "User Request: <review/integration task summary>",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EIA",
      "task": "<review/integration task>",
      "user_context": "<relevant context>",
      "priority": "normal",
      "success_criteria": "<review complete, merged, released>"
    }
  }'
```

**Example (code review)**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "User Request: Review API implementation",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EIA",
      "task": "Review REST API implementation for code quality, security, performance",
      "user_context": "EOA completed implementation. User wants thorough review before merging to main.",
      "priority": "high",
      "success_criteria": "Code review complete, all issues addressed, PR approved and merged"
    }
  }'
```

**Example (release)**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "ecos-inventory-system",
    "subject": "User Request: Release version 2.0",
    "priority": "normal",
    "content": {
      "type": "work_request",
      "specialist": "EIA",
      "task": "Create release 2.0 with all new features, update changelog, tag release",
      "user_context": "All features complete, tests passing. User ready to release.",
      "priority": "normal",
      "success_criteria": "Release 2.0 tagged, changelog updated, release notes published"
    }
  }'
```

---

## 5. Standard AI Maestro API Patterns

### 5.1 Base API format and authentication

**Base URL**: `$AIMAESTRO_API` (default: `http://localhost:23000`)

**Standard curl format**:
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{<message JSON>}'
```

**API environment variables**:
- `AIMAESTRO_API`: API base URL (default: `http://localhost:23000`)
- `AIMAESTRO_AGENT`: Agent identifier override
- `AIMAESTRO_POLL_INTERVAL`: Poll interval in seconds (default: 10)

**No authentication required** for local development (localhost).

---

### 5.2 Message content structure requirements

**CRITICAL**: The `content` field **MUST be an object**, NOT a string!

**CORRECT**:
```json
{
  "content": {
    "type": "work_request",
    "message": "Task description here"
  }
}
```

**WRONG** (will fail):
```json
{
  "content": "Task description here"
}
```

**Standard content fields**:
- `type`: Message type (required: `approval_request`, `approval_decision`, `status_query`, `status_report`, `work_request`, `ping`, `pong`, `user_decision`)
- `message`: Human-readable message (optional but recommended)
- Additional fields specific to message type (see sections above)

---

### 5.3 Priority levels and when to use them

| Priority | When to Use |
|----------|-------------|
| `urgent` | User decisions on high-risk operations, critical blockers |
| `high` | Approval requests, approval decisions, time-sensitive work |
| `normal` | Routine work requests, status queries, health checks |
| `low` | Informational messages, background tasks |

**Examples**:
- **urgent**: User approved production deployment (needs immediate action)
- **high**: ECOS requests approval for destructive operation (needs quick decision)
- **normal**: User asks for status update (no urgency)
- **low**: Logging operational metrics (no action required)

**Default**: Use `"normal"` unless there's a clear reason for higher priority.

---

## Quick Reference Table

| Use Case | Message Type | Priority | Section |
|----------|--------------|----------|---------|
| Receive approval request | `approval_request` | high | 1.1 |
| Send approval decision | `approval_decision` | high | 2.1 |
| Receive status report | `status_report` | normal | 1.2 |
| Request status | `status_query` | normal | 3.1 |
| Health check ping | `ping` | normal | 3.2 |
| Health check response | `pong` | normal | 1.3 |
| User decision notification | `user_decision` | urgent | 2.2 |
| Route work to specialist | `work_request` | normal/high | 4.1-4.4 |

---

**See also**:
- [eama-ecos-coordination/SKILL.md](../SKILL.md) - Main coordination workflow
- [eama-approval-workflows/SKILL.md](../../eama-approval-workflows/SKILL.md) - Approval decision criteria
- [eama-role-routing/SKILL.md](../../eama-role-routing/SKILL.md) - Specialist routing logic
