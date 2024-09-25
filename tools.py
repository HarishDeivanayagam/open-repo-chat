tools_data = [
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "This function is used whenever the user needs to search across multiple files in the codebase",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The users search query",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        }
    }
]
