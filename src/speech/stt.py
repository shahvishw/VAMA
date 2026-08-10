import speech_recognition as sr


class SpeechToText:

    def __init__(self):
        self.recognizer = sr.Recognizer()


    def listen(self, device_index=None):

        with sr.Microphone(device_index=device_index) as source:

            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)

            print(f"You: {text}")

            return text.lower()

        except sr.UnknownValueError:
            print("VAMA: I couldn't understand that.")
            return ""

        except sr.RequestError as error:
            print(f"VAMA: Speech recognition service error: {error}")
            return ""