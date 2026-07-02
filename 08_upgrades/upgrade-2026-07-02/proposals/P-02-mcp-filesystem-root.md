# P-02 — `.mcp.json`: repoint filesystem MCP server root (Track B-2)

**Status:** PROPOSED · **Author model:** claude-fable-5 · **Date:** 2026-07-02
**Target:** `.mcp.json` (untracked in git; read by the live session at boot).

## Why
The filesystem MCP server is rooted at the dead pre-reorg path, so the server
has been a silent no-op since 2026-06-13 (flagged as a blind spot in
`docs/rebase/REASONING_DEBT.md`).

## Exact diff

```diff
--- .mcp.json (current)
+++ .mcp.json (proposed)
@@ mcpServers.filesystem.args @@
-      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/sf2/LabWork/Workspace/29-AgenticScienceWorker"],
+      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/sf2/work/agents/science-agent"],
```

(Root chosen = the project *parent*, matching the original intent of covering
the repo + asta siblings; use `/home/sf2/work/agents/science-agent/1-ScienceAgent`
instead if the owner wants repo-only scope — one word to change.)

## Expected effect
Filesystem MCP works again in live sessions; no behavior/prompt change.

## Eval plan
Fresh session: list the MCP server, read one file through it. Revert = restore
the old string (quoted above).

## APPROVAL
- [ ] APPROVED ____________ (date / initials)   ·   [ ] REJECTED: ____________
