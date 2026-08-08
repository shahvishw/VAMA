def handle_general(intent):

    if intent in ('hi','hello','hey'):
        return "Hello I am VAMA."

    elif intent in ('bye','exit'):
        return 'Goodbye!'

    return "I don't understand that command"