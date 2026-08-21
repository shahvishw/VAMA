import os
import json

from groq import Groq

from core.registry import get_tool_functions,get_tool_schemas
from core.security import authorize


class VamaBrain:

    MAX_ITERATIONS = 6

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-120b"

        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are VAMA, a personal AI assistant. "
                    "Speak naturally and conversationally. "
                    "Use conversation context. "
                    "Keep simple replies concise. "
                    "Use tools when the user asks you to perform an action. "
                    "IMPORTANT TOOL RULES: "
                    "Only call tools whose exact names appear in the provided tool definitions. "
                    "Never modify a tool name. "
                    "Never append channel names, formatting markers, or other text to a tool name. "
                    "Valid tool names must exactly match the provided names. "
                    "Use the minimum number of tool calls necessary to complete the task. "
                    "Do not repeat a tool call if the previous result already provides the required information. "
                    "For file editing: "
                    "Use edit_file when the user asks to replace specific existing text. "
                    "Use write_file only when replacing or creating the complete file contents. "
                    "Do not use write_file after edit_file unless the user explicitly asks to overwrite the entire file. "
                    "Never claim that an action was completed unless the tool actually reports success."
                    "Never claim that an action was completed unless the tool "
                    "actually reports success."
                    "For file operations, follow these rules exactly: "
                    "Use read_file when reading a known file. "
                    "Use search_project only when the requested file or code location "
                    "is unknown or ambiguous. "
                    "Use edit_file when the user asks to change, replace, modify, "
                    "or update specific existing text. "
                    "Use write_file only when the user explicitly wants to create a "
                    "file or replace the complete contents of a file. "
                    "Never use write_file to perform a text replacement inside an "
                    "existing file. "
                    "Never invent new content when the user requested a replacement."
                    "When editing files, never copy instruction words into new_text. "
                    "For a request of the form 'change X to Y', interpret X as old_text "
                    "and Y as new_text. "
                    "old_text must match the actual file contents exactly. "
                    "new_text must contain only what the user wants written."
                    "Never silently correct spelling, grammar, capitalization, or wording "
                    "in file-edit operations. Preserve the user's requested new_text exactly."
                ),
            }
        ]

        self.tools = get_tool_schemas()
        self.available_tools = get_tool_functions()

    def ask(self, user_input):

        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        for iteration in range(self.MAX_ITERATIONS):

            print(f"\n[Agent iteration {iteration + 1}]")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto",
            )

            message = response.choices[0].message

            self.messages.append(message)

            
            if not message.tool_calls:
                return message.content

            
            for tool_call in message.tool_calls:

                function_name = tool_call.function.name

                if function_name not in self.available_tools:
                    print(
                        f"[Tool Error] Model requested unknown tool: "
                        f"{function_name}"
                    )

                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": (
                                f"Error: Unknown tool '{function_name}'. "
                                "Do not call this tool. Use only the tools "
                                "provided in the tool definitions."
                            ),
                        }
                    )

                    continue

                raw_arguments = tool_call.function.arguments

                if raw_arguments is None:
                    arguments = {}

                elif isinstance(raw_arguments, dict):
                    arguments = raw_arguments

                elif isinstance(raw_arguments, str):

                    raw_arguments = raw_arguments.strip()

                    if raw_arguments:
                        arguments = json.loads(raw_arguments)
                    else:
                        arguments = {}

                else:
                    raise TypeError(
                        f"Unexpected tool arguments type: "
                        f"{type(raw_arguments)}"
                    )

                function = self.available_tools[function_name]

                if not authorize(function_name):

                    result = (
                        "The user denied permission to execute "
                        f"the action: {function_name}"
                    )

                else:

                    try:

                        print(f"[Tool] {function_name}")

                        result = function(**arguments)

                    except Exception as error:

                        result = (
                            f"Tool execution failed: {error}"
                        )

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result),
                    }
                )

        return (
            "I couldn't complete the task within the allowed "
            "number of steps."
        )