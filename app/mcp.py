class MCPManager:
    def __init__(self):
        self.tools = {}

    def register_tool(self, tool):
        self.tools[tool.name] = tool

    def execute(self, tool_name, input_data):
        if tool_name not in self.tools:
            return {
                "status": "error",
                "error": f"Tool '{tool_name}' not found"
            }

        tool = self.tools[tool_name]
        return tool.execute(input_data)

    def list_tools(self):
        return list(self.tools.keys())