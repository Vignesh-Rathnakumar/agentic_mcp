#!/usr/bin/env python3
"""
Custom ReAct Agent using MCP tools (File + Terminal)
"""

import re
import json
from typing import List, Tuple, Any
from langchain_core.tools import tool

from app.llm import get_llm
from app.mcp import MCPManager

# ----------------------------
# MCP Manager (Singleton)
# ----------------------------
_mcp_manager = None


def get_mcp_manager() -> MCPManager:
    global _mcp_manager
    if _mcp_manager is None:
        _mcp_manager = MCPManager()

        from app.tools.file_tool import FileTool
        from app.tools.terminal_tool import TerminalTool

        _mcp_manager.register_tool(FileTool())
        _mcp_manager.register_tool(TerminalTool())

    return _mcp_manager


# ----------------------------
# Tools (wrapped via MCP)
# ----------------------------
@tool
def file_reader(path: str) -> str:
    """Read file content from disk"""
    mcp = get_mcp_manager()
    result = mcp.execute("FileReader", {"path": path})

    if result["status"] == "success":
        return str(result["result"])
    return f"Error: {result['error']}"


@tool
def terminal(command: str) -> str:
    """Execute terminal command"""
    mcp = get_mcp_manager()
    result = mcp.execute("Terminal", {"command": command})

    if result["status"] == "success":
        return str(result["result"])
    return f"Error: {result['error']}"


# ----------------------------
# ReAct Agent
# ----------------------------
class ReactAgent:
    def __init__(self, llm, tools: List, max_iterations: int = 8):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations

    def run(self, query: str) -> str:
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": query}
        ]

        for _ in range(self.max_iterations):
            response = self.llm.invoke(messages)
            content = response.content
            messages.append({"role": "assistant", "content": content})

            # ✅ Final answer
            if "Final Answer:" in content:
                return content.split("Final Answer:")[-1].strip()

            # 🔍 Parse action
            action, action_input = self._parse_action(content)

            if not action:
                messages.append({
                    "role": "user",
                    "content": "Observation: Invalid format. Use Action + JSON input."
                })
                continue

            if action not in self.tools:
                messages.append({
                    "role": "user",
                    "content": f"Observation: Tool not found. Available: {list(self.tools.keys())}"
                })
                continue

            # ⚙️ Execute tool
            try:
                result = self.tools[action].invoke(action_input)
                observation = str(result)
            except Exception as e:
                observation = f"Error: {str(e)}"

            messages.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })

        return "Max iterations reached."

    # ----------------------------
    # Prompt
    # ----------------------------
    def _system_prompt(self) -> str:
        tool_desc = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])

        return f"""
You are an AI agent that uses tools.

TOOLS:
{tool_desc}

RULES:
- Think step by step
- Use EXACT format:

Thought: ...
Action: <tool name>
Action Input: {{ JSON }}

- After Observation → think again
- Final output:

Final Answer: ...

Example:
User: list files
Thought: I should use terminal
Action: Terminal
Action Input: {{"command": "ls"}}
Observation: file1.py
Thought: Done
Final Answer: file1.py
"""

    # ----------------------------
    # Parser
    # ----------------------------
    def _parse_action(self, text: str) -> Tuple[Any, Any]:
        action_match = re.search(r'Action:\s*(.+)', text)
        if not action_match:
            return None, None

        action = action_match.group(1).strip()

        input_match = re.search(
            r'Action Input:\s*(\{.*?\})',
            text,
            re.DOTALL
        )

        if not input_match:
            return None, None

        try:
            data = json.loads(input_match.group(1))
            return action, data
        except:
            return None, None


# ----------------------------
# Factory
# ----------------------------
def create_agent():
    llm = get_llm()
    tools = [file_reader, terminal]
    return ReactAgent(llm, tools)


# ----------------------------
# Test
# ----------------------------
if __name__ == "__main__":
    agent = create_agent()
    print(agent.run("list files"))