from langchain.agents import initialize_agent, Tool
from app.llm import get_llm
from app.mcp import MCPManager
from app.tools.file_tool import FileTool
from app.tools.terminal_tool import TerminalTool


def create_agent():
    llm = get_llm()

    mcp = MCPManager()
    mcp.register_tool(FileTool())
    mcp.register_tool(TerminalTool())

    tools = [
        Tool(
            name="FileReader",
            func=lambda input: str(mcp.execute("FileReader", {"path": input})),
            description="Read file content. Input is file path."
        ),
        Tool(
            name="Terminal",
            func=lambda input: str(mcp.execute("Terminal", {"command": input})),
            description="Run terminal commands like ls, pwd"
        )
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True
    )

    return agent