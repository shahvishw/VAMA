from assistant import VamaAssistant
from speech.stt import SpeechToText
from speech.tts import TextToSpeech

def main():
    vama = VamaAssistant()
    stt = SpeechToText()
    tts = TextToSpeech()

    print('======= VAMA  =======')
    print('Say exit to quit.')

    while True:

        command = stt.listen()

        if not command:
            continue

        response = vama.process(command)

        tts.speak(response)

        if command in ('exit','bye'):
            break

if __name__ == '__main__':
    main()