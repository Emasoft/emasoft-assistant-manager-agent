# Creating ECOS Procedure

## Overview

EAMA (Assistant Manager) is the ONLY agent authorized to create ECOS (Chief of Staff) instances. This document describes the step-by-step procedure for spawning a new ECOS agent.

## Key Principles

1. **EAMA chooses the session name** - To avoid collisions and maintain naming consistency
2. **Session name = AI Maestro registry name** - The session name becomes the agent's identifier in AI Maestro
3. **Plugin must be pre-copied** - Plugin files must exist in the target directory BEFORE spawning
4. **Main agent injection** - The `--agent` flag ensures ECOS receives its role-specific system prompt

## Session Naming Convention

Use this format for ECOS session names:

```
<role-prefix>-<descriptive>[-number]
```

**Examples:**
- `ecos-chief-of-staff-one` - Primary ECOS instance
- `ecos-project-alpha` - ECOS for specific project "alpha"
- `ecos-inventory-system` - ECOS for inventory-system project

**Subordinate agents** spawned by ECOS follow their own naming:
- `eoa-svgbbox-orchestrator` (Orchestrator for svgbbox project)
- `eia-inventory-review` (Integrator for inventory review)

## Spawn Command Template

```bash
# EAMA picks a unique session name (this becomes the AI Maestro registry name)
SESSION_NAME="ecos-chief-of-staff-one"

aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Coordinate agents across all projects" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-chief-of-staff \
  --agent ecos-chief-of-staff-main-agent
```

## Command Flags Explained

| Flag | Purpose | Example Value |
|------|---------|---------------|
| `SESSION_NAME` | AI Maestro registry identifier | `ecos-chief-of-staff-one` |
| `--dir` | Working directory (flat structure) | `~/agents/ecos-chief-of-staff-one/` |
| `--task` | Task description (for context) | `"Coordinate agents across all projects"` |
| `--dangerously-skip-permissions` | Skip permission prompts | (flag only) |
| `--chrome` | Enable Chrome DevTools MCP | (flag only) |
| `--add-dir` | Additional working directory | `/tmp` |
| `--plugin-dir` | Path to ECOS plugin | `~/agents/$SESSION_NAME/.claude/plugins/emasoft-chief-of-staff` |
| `--agent` | Main agent prompt file | `ecos-chief-of-staff-main-agent` |

## Critical Notes

### Directory Structure

- Use **FLAT agent folder structure**: `~/agents/<session-name>/`
- NOT nested: `~/agents/project/session-name/`

### Plugin Path

- Use **LOCAL agent folder path**: `~/agents/$SESSION_NAME/.claude/plugins/`
- NOT development path: `./OUTPUT_SKILLS/emasoft-chief-of-staff/`

### Spawn vs Wake

- **NEW spawn**: Use command above (no `--continue` flag)
- **Wake hibernated agent**: Add `--continue` flag

### Pre-requisite

**Plugin files MUST be copied to target directory BEFORE spawning:**

```bash
# Copy plugin to agent's local directory
mkdir -p ~/agents/$SESSION_NAME/.claude/plugins/
cp -r /path/to/emasoft-chief-of-staff ~/agents/$SESSION_NAME/.claude/plugins/
```

## Step-by-Step Procedure

### Step 1: Choose Session Name

Pick a unique session name following the naming convention:

```bash
SESSION_NAME="ecos-chief-of-staff-one"
```

### Step 2: Prepare Agent Directory

Create the agent's working directory:

```bash
mkdir -p ~/agents/$SESSION_NAME
```

### Step 3: Copy Plugin

Copy the ECOS plugin to the agent's local plugins directory:

```bash
mkdir -p ~/agents/$SESSION_NAME/.claude/plugins/
cp -r /path/to/emasoft-chief-of-staff ~/agents/$SESSION_NAME/.claude/plugins/
```

### Step 4: Execute Spawn Command

Run the `aimaestro-agent.sh create` command:

```bash
aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Coordinate agents across all projects" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-chief-of-staff \
  --agent ecos-chief-of-staff-main-agent
```

### Step 5: Verify Spawn Success

Check the command exit code:

```bash
echo $?  # Should return 0 for success
```

### Step 6: Wait for Initialization

Wait 5 seconds for ECOS to initialize:

```bash
sleep 5
```

### Step 7: Health Check Ping

Send a health check message via AI Maestro:

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eama-assistant-manager",
    "to": "'"$SESSION_NAME"'",
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

### Step 8: Verify Response

Check AI Maestro inbox for ECOS response within 30 seconds:

```bash
curl "$AIMAESTRO_API/api/messages?agent=eama-assistant-manager&action=list&status=unread" \
  | jq '.[] | select(.from == "'"$SESSION_NAME"'") | select(.content.type == "pong")'
```

Expected response:

```json
{
  "from": "ecos-chief-of-staff-one",
  "to": "eama-assistant-manager",
  "subject": "Re: Health Check",
  "content": {
    "type": "pong",
    "status": "alive",
    "uptime": "5",
    "active_specialists": []
  }
}
```

### Step 9: Register ECOS

Record the new ECOS instance in the active sessions log:

File: `docs_dev/sessions/active-ecos-sessions.md`

```markdown
## Session: ecos-chief-of-staff-one
- **Spawned**: 2026-02-05 16:30:22
- **Plugins**: emasoft-chief-of-staff
- **Working Dir**: ~/agents/ecos-chief-of-staff-one
- **Last Health Check**: 2026-02-05 16:30:30 (ALIVE)
- **Active Specialists**: (none yet)
- **Current Tasks**: Awaiting work requests
```

### Step 10: Report to User

Notify the user that ECOS is ready:

```
✅ ECOS ready!

Session: ecos-chief-of-staff-one
Status: Active and responding
Working Dir: ~/agents/ecos-chief-of-staff-one

ECOS is now available to coordinate specialist agents (EOA, EAA, EIA).
```

## Success Criteria

A successful ECOS spawn meets ALL of the following criteria:

- [ ] `aimaestro-agent.sh create` command succeeded (exit code 0)
- [ ] ECOS session registered in AI Maestro (visible in session list)
- [ ] ECOS main agent loaded via `--agent` flag
- [ ] ECOS plugins loaded correctly
- [ ] ECOS working directory set correctly
- [ ] ECOS health check ping successful (pong received)
- [ ] ECOS added to active sessions log in `docs_dev/sessions/active-ecos-sessions.md`

## Troubleshooting

### Spawn Fails with Exit Code 1

**Cause**: AI Maestro service may be down or session name collision

**Solution**:
1. Check AI Maestro health: `curl $AIMAESTRO_API/health`
2. Check for existing session: `tmux list-sessions | grep $SESSION_NAME`
3. If collision, use different session name with suffix: `ecos-chief-of-staff-two`

### No Response to Health Ping

**Cause**: ECOS may not have finished initializing

**Solution**:
1. Wait additional 10 seconds
2. Retry health ping
3. Check tmux session manually: `tmux attach -t $SESSION_NAME`

### Plugin Not Found Error

**Cause**: Plugin not copied to local directory before spawn

**Solution**:
1. Verify plugin exists: `ls ~/agents/$SESSION_NAME/.claude/plugins/emasoft-chief-of-staff/`
2. Copy plugin if missing
3. Re-run spawn command

## Related Documents

- [ECOS Communication Protocol](./ecos-communication-protocol.md)
- [ECOS Approval Workflow](./ecos-approval-workflow.md)
- [Active ECOS Sessions Management](./managing-active-sessions.md)
