"""
Agent Transcript Generator

Captures and formats the full agent interaction for traceability:
- Every tool call and result
- Agent reasoning/thinking
- Timestamps and token usage
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import re


@dataclass
class ToolCall:
    """Record of a single tool invocation."""
    tool_name: str
    arguments: Dict[str, Any]
    result: str
    success: bool
    duration_ms: Optional[int] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "tool": self.tool_name,
            "arguments": self.arguments,
            "result": self.result[:1000] if len(self.result) > 1000 else self.result,
            "result_truncated": len(self.result) > 1000,
            "success": self.success,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp
        }


@dataclass
class Turn:
    """A single turn in the agent conversation."""
    turn_number: int
    agent_thinking: Optional[str] = None
    agent_response: Optional[str] = None
    tool_calls: List[ToolCall] = field(default_factory=list)

    # Token usage for this turn
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "turn": self.turn_number,
            "thinking": self.agent_thinking[:500] if self.agent_thinking and len(self.agent_thinking) > 500 else self.agent_thinking,
            "response": self.agent_response,
            "tool_calls": [tc.to_dict() for tc in self.tool_calls],
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "timestamp": self.timestamp
        }


@dataclass
class AgentTranscript:
    """Complete transcript of an agent benchmark run."""
    benchmark_id: str
    run_id: str

    # Initial state
    prompt: str
    workspace_path: str

    # Conversation
    turns: List[Turn] = field(default_factory=list)

    # Final state
    final_result: Optional[str] = None
    files_created: List[str] = field(default_factory=list)
    exit_code: Optional[int] = None

    # Metadata
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    total_duration_seconds: Optional[float] = None

    # Token totals
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    estimated_cost_usd: float = 0.0

    def add_turn(self, turn: Turn):
        """Add a turn to the transcript."""
        self.turns.append(turn)
        if turn.input_tokens:
            self.total_input_tokens += turn.input_tokens
        if turn.output_tokens:
            self.total_output_tokens += turn.output_tokens

    def complete(self, files_created: List[str], exit_code: int, final_result: str = None):
        """Mark transcript as complete."""
        self.completed_at = datetime.now().isoformat()
        self.files_created = files_created
        self.exit_code = exit_code
        self.final_result = final_result

        if self.started_at:
            start = datetime.fromisoformat(self.started_at)
            end = datetime.fromisoformat(self.completed_at)
            self.total_duration_seconds = (end - start).total_seconds()

        # Estimate cost (rough, based on Claude pricing)
        # Input: $3/1M tokens, Output: $15/1M tokens (Opus)
        self.estimated_cost_usd = (
            (self.total_input_tokens * 3 / 1_000_000) +
            (self.total_output_tokens * 15 / 1_000_000)
        )

    def to_dict(self) -> Dict:
        return {
            "benchmark_id": self.benchmark_id,
            "run_id": self.run_id,
            "prompt": self.prompt,
            "workspace_path": self.workspace_path,
            "turns": [t.to_dict() for t in self.turns],
            "final_result": self.final_result,
            "files_created": self.files_created,
            "exit_code": self.exit_code,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_duration_seconds": self.total_duration_seconds,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "estimated_cost_usd": round(self.estimated_cost_usd, 4),
            "num_turns": len(self.turns),
            "num_tool_calls": sum(len(t.tool_calls) for t in self.turns)
        }

    def save(self, path: Path):
        """Save transcript to JSON file."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def to_markdown(self) -> str:
        """Generate human-readable markdown transcript."""
        lines = [
            f"# Agent Transcript: {self.benchmark_id}",
            f"",
            f"**Run ID:** {self.run_id}",
            f"**Duration:** {self.total_duration_seconds:.1f}s" if self.total_duration_seconds else "",
            f"**Turns:** {len(self.turns)}",
            f"**Tool Calls:** {sum(len(t.tool_calls) for t in self.turns)}",
            f"**Exit Code:** {self.exit_code}",
            f"**Est. Cost:** ${self.estimated_cost_usd:.4f}",
            f"",
            "---",
            "",
            "## Prompt",
            "",
            "```",
            self.prompt[:2000] if len(self.prompt) > 2000 else self.prompt,
            "```",
            "",
            "---",
            ""
        ]

        for turn in self.turns:
            lines.append(f"## Turn {turn.turn_number}")
            lines.append(f"*{turn.timestamp}*")
            lines.append("")

            if turn.agent_thinking:
                lines.append("### Thinking")
                lines.append(f"> {turn.agent_thinking[:500]}...")
                lines.append("")

            if turn.tool_calls:
                lines.append("### Tool Calls")
                for tc in turn.tool_calls:
                    status = "SUCCESS" if tc.success else "FAILED"
                    lines.append(f"")
                    lines.append(f"**{tc.tool_name}** [{status}]")

                    # Format arguments nicely
                    if tc.tool_name == "Bash":
                        cmd = tc.arguments.get('command', '')
                        lines.append(f"```bash")
                        lines.append(cmd[:500])
                        lines.append(f"```")
                    elif tc.tool_name in ("Write", "Edit"):
                        file_path = tc.arguments.get('file_path', '')
                        lines.append(f"File: `{file_path}`")
                    elif tc.tool_name == "Read":
                        file_path = tc.arguments.get('file_path', '')
                        lines.append(f"File: `{file_path}`")
                    else:
                        lines.append(f"```json")
                        lines.append(json.dumps(tc.arguments, indent=2)[:300])
                        lines.append(f"```")

                    # Show result excerpt
                    if tc.result:
                        result_preview = tc.result[:200].replace('\n', ' ')
                        lines.append(f"Result: {result_preview}...")
                lines.append("")

            if turn.agent_response:
                lines.append("### Response")
                lines.append(turn.agent_response[:1000])
                lines.append("")

            lines.append("---")
            lines.append("")

        # Final state
        lines.append("## Final State")
        lines.append("")

        if self.files_created:
            lines.append("### Files Created")
            for f in self.files_created[:20]:  # Limit to 20
                lines.append(f"- `{f}`")
            if len(self.files_created) > 20:
                lines.append(f"- ... and {len(self.files_created) - 20} more")
            lines.append("")

        if self.final_result:
            lines.append("### Final Result")
            lines.append("```")
            lines.append(self.final_result[:2000])
            lines.append("```")

        return "\n".join(lines)


def parse_claude_output(output: str, benchmark_id: str, run_id: str, prompt: str, workspace: str) -> AgentTranscript:
    """
    Parse Claude Code JSON output into a structured transcript.

    Claude Code returns JSON with the full conversation when using --output-format json.
    """
    transcript = AgentTranscript(
        benchmark_id=benchmark_id,
        run_id=run_id,
        prompt=prompt,
        workspace_path=workspace
    )

    try:
        data = json.loads(output)

        # Handle different output formats
        if isinstance(data, dict):
            # JSON format output
            result = data.get('result', '')
            usage = data.get('usage', {})
            model_usage = data.get('modelUsage', {})

            # Calculate totals from model usage
            for model, usage_data in model_usage.items():
                transcript.total_input_tokens += usage_data.get('inputTokens', 0)
                transcript.total_output_tokens += usage_data.get('outputTokens', 0)

            # The result is the final agent output
            transcript.final_result = result

            # Create a single turn from the result
            # (Claude Code doesn't expose individual turns in JSON output)
            turn = Turn(
                turn_number=1,
                agent_response=result,
                input_tokens=transcript.total_input_tokens,
                output_tokens=transcript.total_output_tokens
            )
            transcript.add_turn(turn)

    except json.JSONDecodeError:
        # Plain text output - create single turn
        turn = Turn(
            turn_number=1,
            agent_response=output
        )
        transcript.add_turn(turn)
        transcript.final_result = output

    return transcript


def extract_tool_calls_from_text(text: str) -> List[ToolCall]:
    """
    Extract tool calls from agent text output.

    Looks for patterns like:
    - <tool_call name="Bash">...</tool_call>
    - [Tool: Bash] ...
    """
    tool_calls = []

    # Pattern for XML-style tool calls
    xml_pattern = r'<tool_call\s+name="(\w+)">(.*?)</tool_call>'
    for match in re.finditer(xml_pattern, text, re.DOTALL):
        tool_name = match.group(1)
        content = match.group(2)
        tool_calls.append(ToolCall(
            tool_name=tool_name,
            arguments={"raw": content},
            result="",
            success=True
        ))

    # Pattern for bracket-style tool calls
    bracket_pattern = r'\[Tool:\s*(\w+)\](.*?)(?=\[Tool:|$)'
    for match in re.finditer(bracket_pattern, text, re.DOTALL):
        tool_name = match.group(1)
        content = match.group(2).strip()
        tool_calls.append(ToolCall(
            tool_name=tool_name,
            arguments={"raw": content},
            result="",
            success=True
        ))

    return tool_calls
