from app.llm import get_llm

llm = get_llm()

response = llm.invoke("Say hello like a cool AI agent")
print(response.content)


from app.mcp import MCPManager

mcp = MCPManager()


print("MCP initialized")

from app.mcp import MCPManager
from app.tools.file_tool import FileTool

mcp = MCPManager()

# register tool
file_tool = FileTool()
mcp.register_tool(file_tool)

# test execution
result = mcp.execute("FileReader", {"path": "main.py"})

print(result)

from app.mcp import MCPManager
from app.tools.terminal_tool import TerminalTool

mcp = MCPManager()

terminal_tool = TerminalTool()
mcp.register_tool(terminal_tool)

result = mcp.execute("Terminal", {"command": "ls"})

print(result)