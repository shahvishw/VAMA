from datetime import datetime, date
import subprocess

from config import APPS
from core.command import Command


def execute(command: Command):

    if command.intent == "hello":
        return "Hello, I am Vama."

    elif command.intent == "time":
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Current Time is {current_time}"

    elif command.intent == "date":
        today = date.today().isoformat()
        return f"Today's Date is {today}"

    elif command.intent == "open":

        if not command.entity:
            return "What should I open?"

        app = command.entity.lower()

        if app in APPS:
            subprocess.Popen(APPS[app])
            return f"{app} opened successfully."

        return f"I don't know how to open {command.entity}."

    elif command.intent == "exit":
        return "Goodbye!"

    else:
        return "I don't understand that command."