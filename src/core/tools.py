import subprocess
from config import APPS
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def open_application(application:str)-> str:

    application = application.lower().strip()

    if application not in APPS:
        return f"I don't know how to open {application}."

    try:
        subprocess.Popen(APPS[application])
        return f"{application} opened successfully."

    except Exception as e:
        return f"Failed to open {application} : {e}"

def read_file(path : str) -> str :
    """Read a text file from the VAMA project."""

    requested_path = Path(path)

    if not requested_path.is_absolute():
        requested_path = PROJECT_ROOT / requested_path

    requested_path = requested_path.resolve()

    try:
        requested_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return "Error: Access denied. The requested file is outside the VAMA project."

    if not requested_path.exists():
        return f"Error: File not found: {path}"

    if not requested_path.is_file():
        return f"Error: This is not a file: {path}"

    try:
        content = requested_path.read_text(
            encoding="utf-8"
        )

        return content

    except UnicodeDecodeError:
        return "Error: This file is not a supported UTF-8 text file."

    except Exception as error:
        return f"Error reading file: {error}"


def search_project(query : str) -> str :

    query = query.strip()

    if not query:
        return "Search query cannot be empty."

    results = []

    ignored_dics ={
        ".git",
        ".venv",
        "__pycache__"
    }

    for path in PROJECT_ROOT.rglob("*"):

        if not path.is_file():
            continue

        if any(
            part in ignored_dics
            for part in path.parts
        ):
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        except Exception:
            continue

        for line_number,line in enumerate(
            text.splitlines(),
            start=1
        ):
            if query.lower() in line.lower():

                relative_path = path.relative_to(PROJECT_ROOT)

                results.append(
                    f"{relative_path} : {line_number} : {line.strip()}"
                )

                if len(results) >= 30:
                    return "\n".join(results)

    if not results:
        return f"No matches found for {query}"

    return "\n".join(results)

def write_file(path : str, content : str) -> str:

    requested_path = Path(path)

    if not requested_path.is_absolute():
        requested_path = PROJECT_ROOT / requested_path

    requested_path = requested_path.resolve()

    try:
        requested_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return "Error : Access Denied. The requested file is outside the Vama Project"

    try:
        requested_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        requested_path.write_text(
            content,
            encoding="utf-8"
        )

        return f"File written successfully: {path}"

    except Exception as e:
        return f"Error writing file : {e}"

def edit_file(path: str, old_text: str, new_text: str) -> str:

    requested_path = Path(path)

    if not requested_path.is_absolute():
        requested_path = PROJECT_ROOT / requested_path

    requested_path = requested_path.resolve()

    # Security boundary: only allow files inside VAMA.
    try:
        requested_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return "Error: Access denied. The requested file is outside the VAMA project."

    if not requested_path.exists():
        return f"Error: File not found: {path}"

    if not requested_path.is_file():
        return f"Error: This is not a file: {path}"

    try:
        content = requested_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "Error: This file is not a supported UTF-8 text file."
        
    except Exception as error:
        return f"Error reading file: {error}"

    # Important safety check.
    if old_text not in content:
        return "Error: The requested text was not found in the file. \n No changes were made."

    occurrences = content.count(old_text)

    if occurrences > 1:
        return f"Error: The requested text appears {occurrences} times in the file. No changes were made because the target is ambiguous."


    new_content = content.replace(old_text, new_text, 1)

    try:
        requested_path.write_text(
            new_content,
            encoding="utf-8"
        )
    except Exception as error:
        return f"Error writing file: {error}"

    return f"Successfully edited {path}."