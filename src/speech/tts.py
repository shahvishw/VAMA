import pyttsx3

class TextToSpeech:

    def speak(self,text):
        
        print(f"VAMA : {text}")

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()