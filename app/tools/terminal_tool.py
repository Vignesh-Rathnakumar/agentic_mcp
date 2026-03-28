import os
from app.tools.base import MCPTool

class TerminalTool(MCPTool):
    def __init__(self):
        super().__init__(
            name="Terminal",
            description="Executes terminal commands. Input should be a command."
        )

    def _execute(self, input_data):
        command = input_data.get("command")

        if not command:
            raise ValueError("Missing 'command' in input")

        result = os.popen(command).read()
        return result