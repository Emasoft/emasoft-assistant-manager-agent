# Creating ECOS Instance (EAMA Exclusive Responsibility)

## Use-Case TOC

- When to create a new ECOS instance -> Section 1.3
- How to spawn ECOS with proper constraints -> Section 1.2
- Why only EAMA can create ECOS -> Section 1.1
- What to do after creating ECOS -> Section 1.4

## Table of Contents

1. Why EAMA Creates ECOS
2. How to Create ECOS
3. When to Create ECOS
4. Post-Creation Steps

---

## 1. Why EAMA Creates ECOS

EAMA is the ONLY agent authorized to create ECOS. This ensures:

1. **Single point of authority** - Only the user's representative can instantiate the operational coordinator
2. **Role constraint enforcement** - ECOS is created with proper constraints via `--agent` flag
3. **Audit trail** - All ECOS instances are traceable to EAMA approval

---

## 2. How to Create ECOS

When a new ECOS instance is needed (first time setup or after termination), EAMA spawns it using:

```bash
# SESSION_NAME is chosen by EAMA to avoid collisions (e.g., ecos-chief-of-staff-one)
SESSION_NAME="ecos-chief-of-staff-one"

aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Coordinate agents across all projects. You are the Chief of Staff." \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-chief-of-staff \
  --agent ecos-chief-of-staff-main-agent
```

**Session Name = AI Maestro Registry Name**

The session name you pass to `aimaestro-agent.sh create` becomes the agent's identity in AI Maestro:
- EAMA (Manager) chooses the session name for ECOS (e.g., `ecos-chief-of-staff-one`)
- ECOS then chooses session names for subordinate agents (e.g., `eoa-svgbbox-orchestrator`)
- Session names must be unique across all running agents

**Naming Convention:**
- Format: `<role-prefix>-<descriptive-name>[-number]`
- Examples: `ecos-chief-of-staff-one`, `eoa-project-alpha-orchestrator`, `eia-main-integrator`

**Notes:**
- `--dir`: Uses FLAT agent folder structure: `~/agents/<session-name>/`
- `--plugin-dir`: Points to LOCAL agent folder, NOT the development OUTPUT_SKILLS folder
- No `--continue` flag for NEW spawn (only used when WAKING a hibernated agent)
- The plugin must be copied to the local agent folder before spawning

### Critical: The `--agent` Flag

The `--agent ecos-chief-of-staff-main-agent` flag is **REQUIRED**. It:

1. **Injects the ECOS main agent prompt** into the Claude Code system prompt
2. **Enforces role constraints** - ECOS cannot violate its boundaries
3. **Links to documentation** - ECOS automatically reads ROLE_BOUNDARIES.md

**Without this flag, ECOS would be an unconstrained Claude Code instance!**

---

## 3. When to Create ECOS

| Scenario | Action |
|----------|--------|
| **First time** | Create when user starts using the Emasoft agent ecosystem |
| **After termination** | Create if previous ECOS was terminated due to failure |
| **Never duplicate** | Only ONE ECOS should exist at any time |

---

## 4. Post-Creation Steps

After creating ECOS:

1. Verify ECOS is running: `tmux list-sessions | grep ecos`
2. Send initialization message via AI Maestro
3. Confirm ECOS acknowledges its role constraints
4. Register ECOS in the organization agent registry

### Verification Command

```bash
tmux list-sessions | grep ecos
# Expected output: ecos-chief-of-staff: 1 windows (...)
```

### Initialization Message

Send via AI Maestro to confirm ECOS is properly configured:

```json
{
  "to": "ecos",
  "subject": "EAMA Initialization Check",
  "priority": "high",
  "content": {
    "type": "initialization-check",
    "expected_role": "chief-of-staff",
    "requested_at": "ISO-8601 timestamp"
  }
}
```

ECOS should respond confirming its role constraints are loaded.
