"""
thresholds.py - Shared constants for Assistant Manager Agent.

These thresholds configure behavior for user communication,
status reporting, and approval workflows.
"""

# Session memory configuration
MAX_MEMORY_ENTRIES = 100
MEMORY_TTL_DAYS = 30

# Status reporting thresholds
STATUS_POLL_INTERVAL_SECONDS = 60
MAX_STATUS_RETRIES = 3

# Approval workflow timeouts
APPROVAL_TIMEOUT_SECONDS = 300
APPROVAL_REMINDER_INTERVAL_SECONDS = 60

# Communication thresholds
MAX_MESSAGE_LENGTH = 4000
MAX_HANDOFF_SIZE_KB = 100

# Role routing
VALID_ROLES = frozenset(["architect", "orchestrator", "integrator"])
