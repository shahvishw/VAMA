from core.registry import get_tool

def authorize(tool_name : str) -> bool:

    tool = get_tool(tool_name)

    if tool is None:
        raise RuntimeError(
            f"Unknown tool : {tool_name}"
        )

    if not tool["requires_confirmation"]:
        return True

    print(f"Vama wants to use : {tool_name}")
    print(f"Risk level : {tool['risk'].upper()}")
    print(f"This action requires your permission.")

    answer = input("Allow this action? (yes/no) : ")

    return answer.strip().lower() in {
        'yes',
        'y'
    }