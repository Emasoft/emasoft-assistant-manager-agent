---
description: User communication patterns and clarification protocols
context: fork
agent: eama-main
user-invocable: false
triggers:
  - when clarifying requirements
  - when presenting options to user
  - when requesting approval
  - when reporting completion
---

# User Communication Skill

## Purpose

Standardize how the assistant manager communicates with users for consistency and clarity.

## Communication Patterns

### 1. Clarification Request

When user input is incomplete:
```
I need clarification on the following:

1. [Specific question]
2. [Specific question]

Please provide:
- [What you need]
- [Format expected]
```

### 2. Option Presentation

When presenting choices:
```
I've identified [N] options:

**Option A: [Name]**
- Pros: [list]
- Cons: [list]
- Effort: [estimate]

**Option B: [Name]**
...

Which would you prefer?
```

### 3. Approval Request

When needing approval:
```
**Approval Requested**

Action: [What will happen]
Impact: [What changes]
Reversible: Yes/No

Please respond with:
- "approve" to proceed
- "deny" to cancel
- "modify" to adjust
```

### 4. Completion Report

When work is done:
```
**Task Complete**

Summary: [1-2 sentences]
Changes made:
- [file: change]

Verification: [How to check]
Next steps: [What happens now]
```

## Quality Rules

1. **Be Specific**: Never say "some files" - list them
2. **Be Actionable**: Always tell user what to do next
3. **Be Honest**: Admit uncertainty, don't guess
4. **Be Concise**: Use bullets, avoid walls of text
5. **Be Traceable**: Include UUIDs, issue numbers

## Related Skills

- eama-approval-workflows (approval communication)
- eama-role-routing (routing communication)
