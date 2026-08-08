from commands.general import handle_general
from commands.datetime_commands import handle_datetime
from commands.system import handle_system

class CommandRouter:

    def route(slef,parsed_command):

        if not parsed_command:
            return 'Please Enter a Command.'

        intent = parsed_command['intent']
        entity = parsed_command['entity']

        if intent in ("hello",'hi','hey','bye','exit'):
            return handle_general(intent)

        elif intent in ('time','date'):
            return handle_datetime(intent)

        elif intent in ('open','launch'):
            return handle_system(intent,entity)

        return "I don't understand that command."