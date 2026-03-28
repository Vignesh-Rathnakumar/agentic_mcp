from app.tools.base import MCPTool

class FileTool(MCPTool):
    def __init__(self):
        super().__init__(
            name="FileReader",
            description="Reads a file from disk. Input should be a file path."
        )

    def _execute(self, input_data):
        path = input_data.get("path")

        if not path:
            raise ValueError("Missing 'path' in input")

        with open(path, "r") as f:
            return f.read()