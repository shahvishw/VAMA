class CommandParser:

    def parse(self,command):

        command = command.lower().strip()

        if not command:
            return None

        words = command.split()

        intent = words[0]

        entity = ' '.join(words[1:]) 
        
        return{
            'intent' : intent,
            'entity' : entity
        }