# EAMA-ECOS Coordination Workflow Examples

This document contains practical examples of EAMA coordinating with ECOS, including routing requests, handling approvals, status queries, and failure recovery.

---

## Example 1: User Requests New Project

**User**: "Build a REST API for inventory management"

**Your Response**:
```
Understood! I'll create a new project for the inventory management REST API.

Creating project: inventory-system
Location: /Users/user/Code/inventory-system
ECOS session: ecos-inventory-system

Routing to: ORCHESTRATOR (via ECOS)

The EOA will coordinate the implementation. I'll keep you updated on progress. You can ask me for status anytime.
```

**Actions Taken**:
1. Created project directory
2. Initialized git
3. Spawned ecos-inventory-system
4. Verified ECOS alive
5. Sent work request to ECOS
6. Logged to project-registry.md and user-interactions.md

---

## Example 2: ECOS Requests Approval (Low Risk)

**ECOS Message**:
```json
{
  "from": "ecos-inventory-system",
  "subject": "Approval Request: RUN-TESTS-001",
  "content": {
    "type": "approval_request",
    "request_id": "RUN-TESTS-001",
    "operation": "Run pytest test suite",
    "risk_level": "low",
    "justification": "Verify implementation before code review",
    "reversible": true
  }
}
```

**Your Action**: APPROVE AUTONOMOUSLY (low risk, routine, in-scope)

**Your Response to ECOS**:
```json
{
  "subject": "Approval Decision: RUN-TESTS-001",
  "content": {
    "type": "approval_decision",
    "request_id": "RUN-TESTS-001",
    "decision": "approve",
    "reason": "Routine operation, low risk, aligns with testing workflow",
    "approved_by": "eama"
  }
}
```

**Log Entry**: Approval-log.md updated with autonomous approval

---

## Example 3: ECOS Requests Approval (High Risk)

**ECOS Message**:
```json
{
  "from": "ecos-inventory-system",
  "subject": "Approval Request: DEPLOY-PROD-001",
  "content": {
    "type": "approval_request",
    "request_id": "DEPLOY-PROD-001",
    "operation": "Deploy version 2.0 to production",
    "risk_level": "high",
    "justification": "All tests passing, code review complete",
    "reversible": false
  }
}
```

**Your Action**: ESCALATE TO USER (high risk, irreversible)

**Your Response to User**:
```
🚨 APPROVAL REQUIRED

ECOS (inventory-system) is requesting approval for:

Operation: Deploy version 2.0 to production
Risk Level: High
Impact: New version will be live for all users
Reversible: No

Justification: All tests passing, code review complete

I recommend: Approve IF you've verified readiness, otherwise defer for final review

Your decision? (approve/deny/defer)
```

**After User Approves**:
Send approval to ECOS with user quote, log to approval-log.md

---

## Example 4: User Requests Status

**User**: "What's the status of the API?"

**Your Actions**:
1. Query ecos-inventory-system via AI Maestro
2. Receive status report
3. Format for user

**Your Response**:
```
Status for inventory-system:

Overall Progress: 67% complete (8/12 tasks)
Current Focus: Implementing authentication middleware
Recent Completions:
  - REST endpoints (CRUD operations) ✅
  - Database schema ✅
  - Unit tests ✅
  - Code review ✅
Blockers: Waiting for OAuth provider API keys from DevOps
Next Milestone: API v1.0 complete (estimated EOD)
Health: Yellow (blocked on external dependency)

🚨 BLOCKER: Need DevOps to provide OAuth keys to proceed with authentication
```

---

## Example 5: ECOS Spawn Failure

**Scenario**: `aimaestro-agent.sh create` exits with code 1

**Your Action**: Diagnose and report to user

**Your Response to User**:
```
Issue encountered: ECOS spawn failed

Details: aimaestro-agent.sh exited with error code 1
Impact: Cannot coordinate agents for inventory-system project
Attempted: Spawned ecos-inventory-system with standard configuration

Error output: [paste relevant error]

I recommend: Check if AI Maestro is running (`curl http://localhost:23000/health`). If down, restart it. Then I'll retry spawning ECOS.

Should I retry once AI Maestro is confirmed running?
```

---

## ECOS Spawn Failure Recovery Protocol

When ECOS spawn fails, follow this recovery procedure systematically before escalating to the user.

### Recovery Steps

**Step 1: Verify AI Maestro is Running**
```bash
# Check AI Maestro health
curl -s "$AIMAESTRO_API/health"
# Expected: {"status":"ok"} or similar
```

If AI Maestro is down:
- Alert user: "AI Maestro service is not responding. Please restart it."
- Do NOT proceed with spawn retry until AI Maestro is confirmed running

**Step 2: Check tmux Sessions for Conflicts**
```bash
# List existing sessions
tmux list-sessions

# Check if session name already exists
tmux list-sessions | grep "ecos-<project-name>"
```

If session name collision detected:
- Use alternative session name with numeric suffix: `ecos-<project-name>-2`
- Document the collision in session log

**Step 3: Retry Spawn with Different Session Name**
```bash
# Retry with incremented session name
SESSION_NAME="ecos-<project-name>-$(date +%s)"
aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Coordinate agents for <project-name>" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-chief-of-staff \
  --agent ecos-chief-of-staff-main-agent
```

**Step 4: If 3 Retries Fail**

After 3 failed spawn attempts:

1. **Create project WITHOUT ECOS**
   - Project structure is still valid
   - EAMA can receive user requests
   - Work cannot be routed to specialists

2. **Notify User**
   ```
   ECOS Spawn Failed After 3 Attempts

   Project: <project-name>
   Location: <path>
   Status: Created WITHOUT ECOS coordination

   Attempted:
   - Attempt 1: <error>
   - Attempt 2: <error>
   - Attempt 3: <error>

   Impact:
   - Cannot route work to specialist agents (EOA, EAA, EIA)
   - Project directory and git repo are ready
   - You can still interact with me for planning

   To fix:
   1. Check AI Maestro logs: `journalctl -u aimaestro` or `cat ~/ai-maestro/logs/`
   2. Check tmux for orphaned sessions: `tmux list-sessions`
   3. Restart AI Maestro if needed

   Once fixed, I can retry ECOS spawn. Say "retry ECOS for <project-name>" when ready.
   ```

3. **Log Failure**
   Record in `docs_dev/sessions/spawn-failures.md`:
   ```markdown
   ## Spawn Failure: <timestamp>
   - Project: <project-name>
   - Session Name: ecos-<project-name>
   - Attempts: 3
   - Errors: <error details>
   - Resolution: Awaiting user intervention
   ```

**Step 5: Allow User Manual Fix and Retry**

When user says "retry ECOS for <project-name>":
1. Re-run verification steps (AI Maestro health, session conflicts)
2. Attempt spawn with clean session name
3. Report success or escalate again if still failing

### Recovery Decision Tree

```
ECOS Spawn Fails
    |
    v
Is AI Maestro running? ──NO──> Alert user, STOP
    |
   YES
    v
Is session name collision? ──YES──> Use alternative name, RETRY
    |
   NO
    v
Retry count < 3? ──YES──> Wait 10 seconds, RETRY
    |
   NO
    v
Create project WITHOUT ECOS
Notify user with diagnostic info
Log failure
Wait for user to fix and request retry
```

---

## Handoff Pattern

This agent does NOT hand off to other agents directly. You communicate with ECOS, who coordinates specialists.

**Your workflow**:
1. Receive user request
2. Create project/ECOS if needed
3. Route work to ECOS
4. Monitor approvals
5. Report status to user
6. Return to step 1

**Do NOT**:
- Spawn task agents directly (that's ECOS's job)
- Execute implementation work (that's specialists' job)
- Wait indefinitely for responses (timeout and report to user)

---

**Remember**: You are the user's RIGHT HAND. Your value is in **clear communication, intelligent routing, and risk-aware approval decisions**, not in doing the work yourself.
