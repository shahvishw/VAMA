import subprocess
from config import APPS

def handle_system(intent,entity):

    if intent in ('open','launch'):

        if not entity :
            return 'Which Application should I open ?'

        app = APPS.get(entity)

        if not app :
            return f"I don't know how to open {entity}"

        try:
            subprocess.Popen(app)
            return f'{entity} opened successfully.'
        except Exception:
            return "I couldn't open {entity}"

    return "I don't know that command."