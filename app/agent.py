#!/usr/bin/env python3
"""
Custom ReAct Agent that parses text-based actions.
Works with any LLM that can follow the ReAct format.
"""

import re
import json
from typing import Dict, Any, List, Tuple
from langchain_core.tools import tool
from app.llm import get_llm
from app.mcp import MCPManager

# Global MCP manager singleton
_mcp_manager = None


def get_mcp_manager() -> MCPManager:
    """Initialize and return MCP manager with tools registered."""
    global _mcp_manager
    if _mcp_manager is None:
        _mcp_manager = MCPManager()
        from app.tools.file_tool import FileTool
        from app.tools.terminal_tool import TerminalTool
        _mcp_manager.register_tool(FileTool())
        _mcp_manager.register_tool(TerminalTool())
    return _mcp_manager


@tool
def file_reader(path: str) -> str:
    """
    Read contents of a file from disk.

    Args:
        path: File path to read (relative or absolute)

    Returns:
        File content as string, or error message
    """
    mcp = get_mcp_manager()
    result = mcp.execute("FileReader", {"path": path})

    if result["status"] == "success":
        return str(result["result"])
    else:
        return f"Error: {result['error']}"


@tool
def terminal(command: str) -> str:
    """
    Execute a shell command and return output.

    Args:
        command: Shell command to execute (e.g., 'ls -la', 'pwd')

    Returns:
        Command output as string, or error message
    """
    mcp = get_mcp_manager()
    result = mcp.execute("Terminal", {"command": command})

    if result["status"] == "success":
        return str(result["result"])
    else:
        return f"Error: {result['error']}"


class ReactAgent:
    """ReAct agent that uses text-based reasoning and tool use."""

    def __init__(self, llm, tools: List, max_iterations: int = 10):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations

    def run(self, query: str) -> str:
        """
        Run the agent on a user query.

        Args:
            query: User's question/command

        Returns:
            Agent's final answer
        """
        system_prompt = self._build_system_prompt()

        # Start conversation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        for step in range(self.max_iterations):
            try:
                # Get LLM response
                response = self.llm.invoke(messages)
                content = response.content
                messages.append({"role": "assistant", "content": content})

                # Check for final answer
                if "Final Answer:" in content:
                    final = content.split("Final Answer:")[-1].strip()
                    return final

                # Parse Action and Action Input
                action, action_input = self._parse_action(content)
                if not action:
                    # Provide feedback and let it try again
                    observation = "Error: Could not detect Action/Action Input. Use format:\nAction: <tool>\nAction Input: <JSON>"
                    messages.append({"role": "user", "content": f"Observation: {observation}"})
                    continue

                # Validate tool
                if action not in self.tools:
                    observation = f"Error: Tool '{action}' not found. Available: {list(self.tools.keys())}"
                    messages.append({"role": "user", "content": f"Observation: {observation}"})
                    continue

                # Execute tool
                try:
                    tool = self.tools[action]
                    # StructuredTool uses invoke
                    result = tool.invoke(action_input)
                    observation = str(result)
                except Exception as e:
                    observation = f"Error executing tool: {str(e)}"

                messages.append({"role": "user", "content": f"Observation: {observation}"})

            except Exception as e:
                return f"Agent error: {str(e)}"

        return "Max iterations reached without final answer."

    def _build_system_prompt(self) -> str:
        """Build system prompt with tool descriptions and ReAct instructions."""
        tools_desc = []
        for name, tool in self.tools.items():
            desc = getattr(tool, "description", "No description")
            # Get parameter info from tool's args schema if available
            # For simplicity, we just state the tool name and description
            tools_desc.append(f"- {name}: {desc}")
        tools_text = "\n".join(tools_desc)

        return f"""You are an autonomous AI agent that uses tools to answer questions.

Available tools:
{tools_text}

INSTRUCTIONS:
- Think step by step. Start with "Thought:".
- To use a tool, output exactly:
  Action: <tool name>
  Action Input: <JSON with arguments>
- After you receive "Observation:", think and decide next action.
- When you have the final answer, output:
  Thought: <final reasoning>
  Final Answer: <your answer>

EXAMPLE:
User: list files
Thought: I need to see the files, so I'll use the terminal tool.
Action: Terminal
Action Input: {{"command": "ls"}}
Observation: file1.txt  file2.txt
Thought: Now I have the list, I can answer.
Final Answer: The files are: file1.txt, file2.txt

Begin!"""

    def _parse_action(self, text: str) -> Tuple[Any, Any]:
        """
        Parse the LLM output to extract action and action_input.
        Returns (action, action_input) or (None, None).
        """
        # Find "Action:" line
        action_match = re.search(r'Action:\s*([^\n]+)', text, re.IGNORECASE)
        if not action_match:
            return None, None

        action = action_match.group(1).strip()

        # Find "Action Input:" after the action
        start = action_match.end()
        rest = text[start:]
        # Match a JSON object (may be single line or multiline)
        input_match = re.search(r'Action Input:\s*(\{.*?\})(?=\n\w+:|$)', rest, re.DOTALL | re.IGNORECASE)
        if not input_match:
            # Try single-line without braces? Not used
            return None, None

        input_str = input_match.group(1).strip()
        try:
            action_input = json.loads(input_str)
            return action, action_input
        except json.JSONDecodeError:
            return None, None


def create_agent() -> ReactAgent:
    """
    Create and return the ReAct agent.

    Returns:
        ReactAgent instance with tools registered
    """
    llm = get_llm()
    tools = [file_reader, terminal]
    return ReactAgent(llm, tools, max_iterations=10)


# For testing
if __name__ == "__main__":
    agent = create_agent()
    print("Agent created. Testing simple query...")
    result = agent.run("list files in current directory")
    print("Result:", result)
