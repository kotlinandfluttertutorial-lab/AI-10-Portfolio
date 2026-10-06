"""Domain-level exception hierarchy.

Raise these from domain and application service code.
API handlers map them to HTTP responses.
"""


class AgentOpsError(Exception):
    """Base exception for all AgentOps domain errors."""


class NotFoundError(AgentOpsError):
    """The requested resource does not exist."""


class AuthenticationError(AgentOpsError):
    """The request is not authenticated."""


class AuthorizationError(AgentOpsError):
    """The authenticated identity is not permitted to perform this action."""


class ValidationError(AgentOpsError):
    """Input data failed domain-level validation."""


class RateLimitError(AgentOpsError):
    """The caller has exceeded an allowed rate."""


class ConflictError(AgentOpsError):
    """The request conflicts with current state (e.g. duplicate resource)."""
