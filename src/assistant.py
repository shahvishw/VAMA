from core.router import CommandRouter
from core.parser import CommandParser

class VamaAssistant:

    def __init__(self):
        self.parser = CommandParser()
        self.router = CommandRouter()

    def process(self,command):

        parsed_command = self.parser.parse(command)

        return self.router.route(parsed_command)