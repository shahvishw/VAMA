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
                    "Write or replace the complete contents of "
                    "a text file inside the VAMA project. "
                    "Use only when the user explicitly asks "
                    "to create or modify a file."
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
                    "Edit a specific part of a text file inside "
                    "the VAMA project by replacing exact existing "
                    "text with new text. "
                    "Use this instead of write_file when modifying "
                    "part of an existing file."
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
                                "The exact existing text that "
                                "must be replaced."
                            ),
                        },
                        "new_text": {
                            "type": "string",
                            "description": (
                                "The replacement text."
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