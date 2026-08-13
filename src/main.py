from speech.stt import SpeechToText
from speech.tts import TextToSpeech
from ai.llm import ask_vama
from core.parser import parse_llm_response
from core.executor import execute

def understand_command(user_input):
    prompt = f"""
You are the command understanding system for VAMA.

Convert the user's request into JSON.

Allowed intents:
- open
- time
- date
- exit
- hello
- unknown

Return ONLY valid JSON.
Do not include markdown.
Do not explain anything.

Required format:
{{
    "intent": "<intent>",
    "entity": "<entity>"
}}

User command:
{user_input}
"""

    response = ask_vama(prompt)

    print("LLM:", response)

    return parse_llm_response(response)

def main():

    stt = SpeechToText()
    tts = TextToSpeech()

    print("======= VAMA =======")
    print("Say 'exit' to quite.")

    while True:

        user_input = stt.listen()

        if not user_input:
            continue

        try :
            command = understand_command(user_input)

            print('Command : ',command)

            response = execute(command)

            tts.speak(response)

            if command.intent == 'exit':
                break

        except Exception as e:
            print(f"VAMA : Something went worng : {e}")


if __name__ == '__main__':
    main()