from core.tools import (
    open_application,
    search_project,
    read_file,
    write_file,
    edit_file
)

TOOL_REGISTRY = {
    "open_application": {
        "function": open_application,
        "risk": "low",
        "requires_confirmation": False,
        "schema": {
            "type": "function",
            "function": {
                "name": "open_application",
                "description": (
                    "Open an installed application on the user's "
                    "Windows computer."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "application": {
                            "type": "string",
                            "description": (
                                "Application to open. "
                                "Examples: notepad, calculator, paint."
                            ),
                        }
                    },
                    "required": ["application"],
                },
            },
        },
    },

    "read_file": {
        "function": read_file,
        "risk": "low",
        "requires_confirmation": False,
        "schema": {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": (
                    "Read the contents of a text file inside "
                    "the VAMA project."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": (
                                "Path of the file relative to "
                                "the VAMA project. "
                                "Example: README.md or src/main.py"
                            ),
                        }
                    },
                    "required": ["path"],
                },
            },
        },
    },

    "search_project": {
        "function": search_project,
        "risk": "low",
        "requires_confirmation": False,
        "schema": {
            "type": "function",
            "function": {
                "name": "search_project",
                "description": (
                    "Search the VAMA project for a text string. "
                    "Use this when you need to find which file or "
                    "code contains something before reading it."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "Text, function name, class name, "
                                "or concept to search for."
                            ),
                        }
                    },
                    "required": ["query"],
                },
            },
        },
    },

    "write_file": {
        "function": write_file,
        "risk": "high",
        "requires_confirmation": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": (
                    "Create a new text file or completely replace the entire contents "
                    "of an existing file. "
                    "IMPORTANT: Do NOT use this tool when the user asks to replace "
                    "specific text inside an existing file. Use edit_file instead."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": (
                                "Path of the file relative to "
                                "the VAMA project."
                            ),
                        },
                        "content": {
                            "type": "string",
                            "description": (
                                "Complete new contents of the file."
                            ),
                        },
                    },
                    "required": ["path", "content"],
                },
            },
        },
    },
    "edit_file": {
        "function": edit_file,
        "risk": "high",
        "requires_confirmation": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "edit_file",
                "description": (
                    "Edit part of an existing text file by replacing exact text. "
                    "IMPORTANT: Use this tool whenever the user asks to change, "
                    "replace, modify, or update specific text inside an existing file. "
                    "For example, if the user says 'change A to B', use edit_file. "
                    "Do NOT use write_file for replacing specific text. "
                    "The old_text must be the exact existing text in the file."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": (
                                "Path of the file relative to "
                                "the VAMA project."
                            ),
                        },
                        "old_text": {
                            "type": "string",
                            "description": (
                                "EXACT text currently present in the file that the user "
                                "wants replaced. Copy it exactly from the file content. "
                                "Do not include words such as 'from', 'to', 'change', "
                                "'replace', or other instruction words unless they are "
                                "actually part of the file."
                            ),
                        },
                       "new_text": {
                            "type": "string",
                            "description": (
                                "Only the new replacement text requested by the user. "
                                "Do not include instruction words such as 'from', 'to', "
                                "'change', or 'replace' unless the user explicitly wants "
                                "those words written into the file."
                            ),
                        },
                    },
                    "required": [
                        "path",
                        "old_text",
                        "new_text",
                    ],
                },
            },
        },
    },
}

def get_tool(name):
    return TOOL_REGISTRY.get(name)

def get_all_tools():
    return list(TOOL_REGISTRY.values())

def get_tool_schemas():
    return [
        tool['schema']
        for tool in TOOL_REGISTRY.values()
    ]

def get_tool_functions():
    return {
        name : tool['function']
        for name,tool in TOOL_REGISTRY.items()
    }