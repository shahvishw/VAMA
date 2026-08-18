from speech.stt import SpeechToText
from speech.tts import TextToSpeech
from ai.llm import VamaBrain


def main():

    stt = SpeechToText()
    tts = TextToSpeech()

    brain = VamaBrain()

    print("======= VAMA =======")
    print("Say 'exit' to quit.")

    try:

        while True:

            user_input = stt.listen()

            if not user_input:
                continue

            try:

                response = brain.ask(user_input)

                if response:
                    tts.speak(response)

            except Exception as error:
                print(f"VAMA: Something went wrong: {error}")

    except KeyboardInterrupt:

        print("\nVAMA: Shutting down.")

    finally:

        print("======= VAMA STOPPED =======")


if __name__ == "__main__":
    main()