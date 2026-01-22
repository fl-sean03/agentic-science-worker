"""
Agent Backends for Benchmark Harness

Provides abstraction layer for different coding agents.
"""

from .base import AgentBackend
from .claude import ClaudeBackend

# Register available backends
BACKENDS = {
    'claude': ClaudeBackend,
    # Future backends:
    # 'codex': CodexBackend,
    # 'aider': AiderBackend,
}

def get_backend(name: str = 'claude') -> AgentBackend:
    """Get a backend by name."""
    if name not in BACKENDS:
        available = ', '.join(BACKENDS.keys())
        raise ValueError(f"Unknown backend: {name}. Available: {available}")
    return BACKENDS[name]()

__all__ = ['AgentBackend', 'ClaudeBackend', 'BACKENDS', 'get_backend']
