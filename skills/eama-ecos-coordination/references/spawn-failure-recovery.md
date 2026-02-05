# Spawn Failure Recovery Procedures

## Overview

This document provides recovery procedures for handling failures in ECOS creation, agent spawning, and inter-agent communication within the EAMA system.

---

## 1. ECOS Spawn Failure Recovery Protocol

When ECOS spawn fails, follow this recovery procedure systematically before escalating to the user.

### Recovery Steps

#### Step 1: Verify AI Maestro is Running

```bash
# Check AI Maestro health
curl -s "$AIMAESTRO_API/health"
# Expected: {"status":"ok"} or similar
```

If AI Maestro is down:
- Alert user: "AI Maestro service is not responding. Please restart it."
- Do NOT proceed with spawn retry until AI Maestro is confirmed running

#### Step 2: Check tmux Sessions for Conflicts

```bash
# List existing sessions
tmux list-sessions

# Check if session name already exists
tmux list-sessions | grep "ecos-<project-name>"
```

If session name collision detected:
- Use alternative session name with numeric suffix: `ecos-<project-name>-2`
- Document the collision in session log

#### Step 3: Retry Spawn with Different Session Name

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

#### Step 4: If 3 Retries Fail

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

#### Step 5: Allow User Manual Fix and Retry

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

## 2. Communication Breakdown Recovery

When ECOS or other agents fail to respond to messages.

### When ECOS Doesn't Respond

**Symptoms:**
- No response to health ping
- No acknowledgment of routing request
- Messages sent via AI Maestro but no reply received

**Recovery Procedure:**

1. **Wait 30 seconds**
   - Allow time for ECOS to process message
   - ECOS may be busy with approval workflow

2. **Retry health ping once**
   ```bash
   curl -X POST "$AIMAESTRO_API/messages" \
     -H "Content-Type: application/json" \
     -d '{
       "from": "eama-assistant-manager",
       "to": "ecos-<project-name>",
       "subject": "Health Check",
       "priority": "normal",
       "content": {"type": "health_check", "message": "Are you alive?"}
     }'
   ```

3. **If still no response, report to user**
   ```
   Communication Issue: ECOS Not Responding

   Project: <project-name>
   Session: ecos-<project-name>
   Issue: No response to messages after 30s + 1 retry

   Checked:
   - AI Maestro API: Running
   - Message sent successfully: Yes
   - Response received: No

   Possible causes:
   1. ECOS session crashed
   2. ECOS overloaded or stuck
   3. AI Maestro routing issue

   Actions you can take:
   1. Check ECOS session: `tmux attach -t ecos-<project-name>`
   2. Check ECOS logs (if available)
   3. Restart ECOS if needed

   I can retry routing once ECOS is confirmed working.
   ```

4. **Log the communication failure**
   Record in `docs_dev/sessions/communication-failures.md`:
   ```markdown
   ## Communication Failure: <timestamp>
   - From: EAMA
   - To: ecos-<project-name>
   - Message: <subject>
   - Attempts: 2 (initial + 1 retry)
   - Timeout: 30s + 30s
   - Status: No response
   - Resolution: Escalated to user
   ```

---

## 3. Approval Request Handling Failures

When approval workflow encounters errors.

### When Approval Request Unclear

**Symptoms:**
- ECOS approval request lacks required fields
- Risk level ambiguous or missing
- Proposed action description incomplete

**Recovery Procedure:**

1. **Do NOT approve by default**
   - Missing information = deny by default
   - Never guess user intent

2. **Request clarification from ECOS**
   ```bash
   curl -X POST "$AIMAESTRO_API/messages" \
     -H "Content-Type: application/json" \
     -d '{
       "from": "eama-assistant-manager",
       "to": "ecos-<project-name>",
       "subject": "Approval Clarification Needed",
       "priority": "high",
       "content": {
         "type": "clarification_request",
         "message": "Approval request incomplete. Missing: <field1>, <field2>. Please resend with full context."
       }
     }'
   ```

3. **If still unclear, escalate to user**
   ```
   Approval Blocked: Unclear Request

   Project: <project-name>
   Request from: ECOS
   Issue: Missing required approval information

   Details:
   - Risk level: <missing/unclear>
   - Proposed action: <incomplete description>
   - Impact: <not specified>

   I need your decision:
   - Approve anyway? (not recommended)
   - Deny and request more info?
   - Let me ask ECOS for clarification?
   ```

### When Multiple Conflicting Requests

**Symptoms:**
- Two approval requests for same resource
- Conflicting actions proposed simultaneously
- Priority conflict (e.g., deploy vs. rollback)

**Recovery Procedure:**

1. **Pause all approvals**
   - Do not process either request
   - Send "HOLD" response to both

2. **Escalate to user immediately**
   ```
   Conflict Detected: Multiple Approval Requests

   Project: <project-name>

   Request A:
   - From: <agent/ECOS>
   - Action: <action1>
   - Risk: <level>

   Request B:
   - From: <agent/ECOS>
   - Action: <action2>
   - Risk: <level>

   Conflict: Both requests target <resource> but propose incompatible actions

   Which should proceed?
   - Approve Request A only?
   - Approve Request B only?
   - Approve both in sequence (A then B)?
   - Deny both and investigate?
   ```

3. **Wait for user to resolve conflict**
   - Do not proceed until user provides clear direction
   - Do not attempt to resolve conflicts autonomously

---

## 4. Agent Spawning Failures (General)

When spawning specialist agents (EOA, EAA, EIA) fails.

### Symptoms

- `aimaestro-agent.sh create` exits with non-zero code
- Session created but agent doesn't respond
- Plugin loading errors in spawn output

### Recovery Procedure

1. **Check AI Maestro health** (same as Step 1 for ECOS)

2. **Verify plugin availability**
   ```bash
   # Check if specialist plugin exists
   ls -la ~/agents/<session-name>/.claude/plugins/emasoft-orchestrator-agent
   ls -la ~/agents/<session-name>/.claude/plugins/emasoft-architect-agent
   ls -la ~/agents/<session-name>/.claude/plugins/emasoft-integrator-agent
   ```

3. **Check for tmux session zombie processes**
   ```bash
   # List sessions
   tmux list-sessions

   # Kill orphaned sessions if needed
   tmux kill-session -t <zombie-session-name>
   ```

4. **Retry with clean environment**
   - Use fresh session name with timestamp
   - Ensure plugin directory is accessible
   - Verify all --plugin-dir paths are valid

5. **After 2 retries, escalate to user**
   ```
   Agent Spawn Failed: <agent-type>

   Session: <session-name>
   Attempts: 2
   Plugin: <plugin-name>
   Error: <error output>

   Diagnostic info:
   - AI Maestro: Running
   - Session name: Available
   - Plugin path: <verified/missing>

   Recommended actions:
   1. Check plugin installation
   2. Verify plugin compatibility
   3. Review spawn logs: `cat ~/agents/<session>/spawn.log`

   Should I:
   - Try alternate plugin version?
   - Spawn without this plugin?
   - Abort and manual investigation?
   ```

---

## 5. Logging and Audit Trail

All failures MUST be logged for debugging and audit purposes.

### Log Locations

| Failure Type | Log File | Format |
|--------------|----------|--------|
| ECOS spawn failures | `docs_dev/sessions/spawn-failures.md` | Markdown |
| Communication failures | `docs_dev/sessions/communication-failures.md` | Markdown |
| Approval conflicts | `docs_dev/sessions/approval-conflicts.md` | Markdown |
| Agent spawn failures | `docs_dev/sessions/agent-spawn-failures.md` | Markdown |

### Log Entry Template

```markdown
## Failure: <timestamp>
- Type: <spawn/communication/approval>
- Component: <ECOS/agent/messaging>
- Project: <project-name>
- Session: <session-name>
- Attempts: <count>
- Error: <error message>
- Recovery Actions: <list of actions taken>
- Resolution: <escalated/retry scheduled/fixed>
- User Notified: <yes/no>
```

---

## 6. Timeliness Requirements

**Response times for failure handling:**

- ECOS spawn failure detection: Immediate (exit code check)
- Communication timeout: 30 seconds before first retry
- Approval request clarification: Within 60 seconds
- User escalation: Within 2 minutes of detection
- Retry intervals: 10 seconds between spawn retries

**Do NOT:**
- Wait indefinitely for responses
- Retry more than 3 times without user input
- Approve unclear requests "to unblock work"
- Hide failures from user to "avoid concern"

**DO:**
- Report failures promptly and clearly
- Provide actionable diagnostic information
- Offer concrete next steps to user
- Log all failure events for audit

---

## 7. Example Scenarios

### Example 1: ECOS Spawn Fails (AI Maestro Down)

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

### Example 2: ECOS Not Responding to Routing Request

**Scenario**: Sent routing request 30s ago, no response

**Your Actions**:
1. Wait 30 seconds (already elapsed)
2. Send health check message
3. Wait 30 more seconds
4. No response → escalate

**Your Response to User**:
```
Communication issue detected with ECOS for inventory-system.

I sent a work routing request 60 seconds ago but received no response.

Status:
- AI Maestro API: Running ✅
- Message delivered: Yes ✅
- ECOS response: None ❌

This could mean:
- ECOS session crashed
- ECOS is stuck processing another request
- Messaging route is broken

Can you check the ECOS session? `tmux attach -t ecos-inventory-system`

Once you confirm ECOS status, I can retry routing your request.
```

### Example 3: Conflicting Approval Requests

**Scenario**: Two approvals arrive simultaneously

**Your Actions**:
1. Pause both
2. Escalate immediately

**Your Response to User**:
```
⚠️ Conflict Detected: Need Your Decision

Project: inventory-system

Request A (from EOA via ECOS):
- Action: Deploy to staging
- Risk: Medium (database migration included)

Request B (from EIA via ECOS):
- Action: Rollback staging (critical bug found)
- Risk: High (data loss possible)

These conflict! Both target staging environment.

What should I do?
1. Approve rollback first (safe, but delays deploy)
2. Approve deploy first (risky if bug critical)
3. Deny both and investigate the critical bug
4. Something else?
```

---

## Summary

Recovery from failures requires:

1. **Systematic diagnosis** - Check AI Maestro, tmux, plugins
2. **Automatic retries** - Up to 3 attempts with delays
3. **Clear user escalation** - Provide diagnostic info and options
4. **Comprehensive logging** - Audit trail for all failures
5. **Timeliness** - Don't block indefinitely; escalate quickly

**Key Principle**: When in doubt, escalate to user with clear options. Do NOT guess, assume, or hide failures.
