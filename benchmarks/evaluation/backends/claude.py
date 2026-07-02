"""
Claude Code backend for benchmark harness.
"""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List

from .base import AgentBackend


class ClaudeBackend(AgentBackend):
    """
    Backend for Claude Code CLI.

    Uses the `claude` CLI tool with subscription-based authentication.
    """

    name = "claude"

    DEFAULT_TOOLS = [
        "Bash", "Read", "Write", "Edit", "Glob", "Grep",
        "WebSearch", "WebFetch", "TodoWrite"
    ]

    def run(
        self,
        prompt: str,
        workspace: Path,
        max_turns: int = 50,
        timeout: int = 1800,
        allowed_tools: List[str] = None,
        verbose: bool = False,
        model: str = None
    ) -> Dict[str, Any]:
        """
        Run Claude Code agent with the given prompt.

        `model` (Slice A1, rebase-2026-07-02): explicit model pin passed as
        `--model`; None preserves the legacy unpinned behavior.
        """
        if allowed_tools is None:
            allowed_tools = self.DEFAULT_TOOLS

        # Build command
        cmd = [
            "claude",
            "-p",  # Print mode (non-interactive)
            "--output-format", "json",
            "--dangerously-skip-permissions",  # Full autonomy
            "--allowedTools", ",".join(allowed_tools),
        ]
        if model:
            cmd += ["--model", model]  # Slice A1: pin executor model

        if verbose:
            print(f"  Command: {' '.join(cmd)}...")
            print(f"  Workspace: {workspace}")
            print(f"  Timeout: {timeout}s")

        start_time = time.time()

        try:
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(workspace.parent.parent),  # Project root
                env={**os.environ, "HOME": os.environ.get("HOME")}
            )

            elapsed = time.time() - start_time

            # Try to parse JSON output
            agent_json = {}
            try:
                agent_json = json.loads(result.stdout)
            except json.JSONDecodeError:
                pass

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "elapsed": elapsed,
                "agent_json": agent_json
            }

        except subprocess.TimeoutExpired as e:
            elapsed = time.time() - start_time
            return {
                "status": "timeout",
                "stdout": e.stdout or "",
                "stderr": e.stderr or f"Timeout after {timeout}s",
                "exit_code": -1,
                "elapsed": elapsed,
                "agent_json": {}
            }

        except Exception as e:
            elapsed = time.time() - start_time
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1,
                "elapsed": elapsed,
                "agent_json": {}
            }

    def verify(self) -> bool:
        """
        Verify Claude Code CLI is available.
        """
        try:
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    @property
    def description(self) -> str:
        return "Claude Code CLI (Anthropic)"
