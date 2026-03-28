class MCPTool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self, input_data):
        try:
            result = self._execute(input_data)

            return {
                "status": "success",
                "result": result
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _execute(self, input_data):
        raise NotImplementedError("Tool must implement _execute method")