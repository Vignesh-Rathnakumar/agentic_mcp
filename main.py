from app.llm import get_llm

llm = get_llm()

response = llm.invoke("Say hello like a cool AI agent")
print(response.content)


from app.mcp import MCPManager

mcp = MCPManager()

print("MCP initialized")