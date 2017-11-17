import pyttsx3

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def say(self, message):
        self.engine.say(message)
        self.engine.runAndWait()
        self.engine.stop()
    
