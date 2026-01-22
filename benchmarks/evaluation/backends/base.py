"""
Base class for agent backends.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List


class AgentBackend(ABC):
    """
    Abstract base class for agent backends.

    Each backend implements execution for a specific coding agent
    (Claude Code, OpenAI Codex, Aider, etc.)
    """

    name: str = "base"

    @abstractmethod
    def run(
        self,
        prompt: str,
        workspace: Path,
        max_turns: int = 50,
        timeout: int = 1800,
        allowed_tools: List[str] = None,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Run the agent with the given prompt.

        Args:
            prompt: The task prompt
            workspace: Working directory for the agent
            max_turns: Maximum conversation turns
            timeout: Timeout in seconds
            allowed_tools: List of allowed tools
            verbose: Enable verbose output

        Returns:
            Dict with keys:
                - status: "success", "failed", "timeout", "error"
                - stdout: Agent output
                - stderr: Error output
                - exit_code: Process exit code
                - elapsed: Execution time in seconds
                - agent_json: Parsed JSON output (if available)
        """
        pass

    @abstractmethod
    def verify(self) -> bool:
        """
        Verify the backend is available and configured.

        Returns:
            True if backend is ready, False otherwise
        """
        pass

    @property
    def description(self) -> str:
        """Human-readable description of the backend."""
        return f"{self.name} backend"
