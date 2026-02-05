# Workflow Checklists

Use these checklists to ensure complete execution of each workflow. Check off items as you complete them.

## Checklist: Creating New Project

When user requests a new project:

- [ ] **Parse user request** for project name, purpose, and requirements
- [ ] **Clarify ambiguities** if location/structure not specified
- [ ] **Verify project name available** (directory doesn't exist)
- [ ] **Create project directory** at agreed location
- [ ] **Initialize git repository**
  ```bash
  cd /path/to/new-project
  git init
  git config user.name "Emasoft"
  git config user.email "713559+Emasoft@users.noreply.github.com"
  ```
- [ ] **Create initial structure**
  - README.md with project description
  - .gitignore appropriate for project type
  - docs_dev/, scripts_dev/ directories
- [ ] **Commit initial structure**
  ```bash
  git add -A
  git commit -m "Initial project structure"
  ```
- [ ] **Spawn ECOS for this project** using `aimaestro-agent.sh create`
- [ ] **Verify ECOS responding** via health check ping
- [ ] **Register project** in `docs_dev/projects/project-registry.md`
- [ ] **Report to user** with project path and ECOS session name
- [ ] **Log session creation** in `docs_dev/sessions/active-ecos-sessions.md`

**Success Criteria**: Project directory exists, git initialized, ECOS alive and registered.

## Checklist: Spawning ECOS

When creating a new ECOS instance:

- [ ] **Determine ECOS session name** (format: `ecos-<project-name>`)
- [ ] **Identify working directory** (project root)
- [ ] **Identify plugins to load** (emasoft-chief-of-staff required)
- [ ] **Prepare spawn command** with all flags:
  ```bash
  aimaestro-agent.sh create ecos-<project-name> \
    --dir ~/agents/ecos-<project-name> \
    --task "Coordinate agents for <project-name> development" \
    -- --dangerously-skip-permissions --chrome --add-dir /tmp \
    --plugin-dir ~/agents/ecos-<project-name>/.claude/plugins/emasoft-chief-of-staff \
    --agent ecos-chief-of-staff-main-agent
  ```
  Note: Copy plugin to `~/agents/ecos-<project-name>/.claude/plugins/` first!
- [ ] **Execute spawn command** via Bash tool
- [ ] **Verify exit code 0** (success)
- [ ] **Wait 5 seconds** for ECOS initialization
- [ ] **Send health check ping** via AI Maestro
  ```bash
  curl -X POST "$AIMAESTRO_API/api/messages" \
    -H "Content-Type: application/json" \
    -d '{"from":"eama-assistant-manager","to":"ecos-<project-name>","subject":"Health Check","priority":"normal","content":{"type":"ping","message":"Verify ECOS alive"}}'
  ```
- [ ] **Verify ECOS response** (check inbox for pong within 30 seconds)
- [ ] **Register ECOS session** in active sessions log
- [ ] **Report ECOS ready** to user

**Success Criteria**: ECOS session exists, responds to ping, registered in logs.

## Checklist: Processing ECOS Approval Request

When ECOS sends an approval request:

- [ ] **Read approval request** from AI Maestro inbox
  ```bash
  curl "$AIMAESTRO_API/api/messages?agent=eama-assistant-manager&action=list&status=unread"
  ```
- [ ] **Parse request details**:
  - Request ID
  - Operation description
  - Risk level (if provided)
  - Justification
- [ ] **Assess risk level**:
  - Is operation destructive? (delete files, drop tables)
  - Is operation irreversible? (deploy prod, publish release)
  - Is operation within ECOS documented scope?
  - Does operation align with user's stated goals?
- [ ] **Make decision**:
  - **If high risk OR out of scope**: Escalate to user for approval
  - **If routine and in-scope**: Approve autonomously
  - **If misaligned with goals**: Deny and explain
- [ ] **If escalating to user**:
  - [ ] Present request to user with risk assessment
  - [ ] Wait for user decision
  - [ ] Record user decision verbatim
- [ ] **Send approval decision** to ECOS via AI Maestro
  ```bash
  curl -X POST "$AIMAESTRO_API/api/messages" \
    -H "Content-Type: application/json" \
    -d '{"from":"eama-assistant-manager","to":"ecos-<project>","subject":"Approval Decision: <REQUEST-ID>","priority":"high","content":{"type":"approval_decision","request_id":"<REQUEST-ID>","decision":"approve|deny","reason":"<explanation>"}}'
  ```
- [ ] **Log approval** in `docs_dev/approvals/approval-log.md`
- [ ] **Verify ECOS acknowledgment** (if expected)

**Success Criteria**: Approval decision made, sent to ECOS, logged, acknowledged.

## Checklist: Routing User Request to ECOS

When user gives a work request:

- [ ] **Parse user request** for intent (build, design, test, etc.)
- [ ] **Identify target specialist** using routing table:
  - Design/plan → ARCHITECT (via ECOS)
  - Build/implement → ORCHESTRATOR (via ECOS)
  - Review/test/release → INTEGRATOR (via ECOS)
- [ ] **Identify target ECOS** (which project?)
- [ ] **Verify ECOS exists and is alive**
  - Check active sessions log
  - Send health ping if uncertain
  - Create ECOS if not exists
- [ ] **Format work request** for ECOS
- [ ] **Send request** to ECOS via AI Maestro
  ```bash
  curl -X POST "$AIMAESTRO_API/api/messages" \
    -H "Content-Type: application/json" \
    -d '{"from":"eama-assistant-manager","to":"ecos-<project>","subject":"User Request: <summary>","priority":"normal","content":{"type":"work_request","specialist":"<EOA|EAA|EIA>","task":"<task description>","user_context":"<relevant context>"}}'
  ```
- [ ] **Acknowledge to user** that request routed
- [ ] **Log interaction** in `docs_dev/sessions/user-interactions.md`

**Success Criteria**: Request parsed, routed to correct ECOS/specialist, user acknowledged.

## Checklist: Providing Status to User

When user requests status:

- [ ] **Parse status request** for scope (entire project? specific task?)
- [ ] **Identify relevant agents** to query
- [ ] **Send status query** to ECOS via AI Maestro
  ```bash
  curl -X POST "$AIMAESTRO_API/api/messages" \
    -H "Content-Type: application/json" \
    -d '{"from":"eama-assistant-manager","to":"ecos-<project>","subject":"Status Query","priority":"normal","content":{"type":"status_query","scope":"<scope>"}}'
  ```
- [ ] **Wait for responses** (30 second timeout per agent)
- [ ] **Aggregate responses** into human-readable summary
- [ ] **Format status report** for user:
  - Overall progress percentage
  - Current focus (what's being worked on now)
  - Recent completions
  - Blockers/issues
  - Next milestones
- [ ] **Present to user**
- [ ] **Handle follow-up questions**

**Success Criteria**: Status collected, aggregated, presented to user, acknowledged.
