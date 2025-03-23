# To install the required libraries for this script, open your terminal and run the following commands:

# Install gTTS (Google Text-to-Speech)
# This library is used for converting text into speech.
#pip install gtts

# Install SpeechRecognition
# This library is used to recognize speech and convert it into text.
#pip install SpeechRecognition

# Logging is part of the Python standard library, so no installation is needed for 'logging'.
# 'os' is also part of the Python standard library, so no installation is required for 'os'.


import os
from gtts import gTTS
import speech_recognition as sr
import logging

class TextToSpeech:
    def __init__(self, language='en', slow=False):
        """Initialize the Text-to-Speech engine with customizable settings."""
        self.language = language
        self.slow = slow

    def speak(self, text):
        """Convert the provided text to speech using Google TTS."""
        try:
            # Specify the path for saving the file (in Documents folder)
            documents_folder = os.path.expanduser("~/Documents")  # This will work on most systems
            output_dir = os.path.join(documents_folder, 'speech_output')

            # Make sure the directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_file = os.path.join(output_dir, 'speech.mp3')

            tts = gTTS(text=text, lang=self.language, slow=self.slow)
            tts.save(output_file)

            # Play the generated speech (cross-platform)
            if os.name == 'nt':  # For Windows
                os.system(f"start {output_file}")
            elif os.name == 'posix':  # For macOS or Linux
                os.system(f"afplay {output_file}")  # macOS
                # os.system(f"mpg321 {output_file}")  # Linux
        except Exception as e:
            logging.error(f"Error in Text-to-Speech: {e}")


class SpeechToText:
    def __init__(self, timeout=5, phrase_time_limit=10):
        """Initialize the Speech-to-Text engine with customizable settings."""
        self.recognizer = sr.Recognizer()
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

    def recognize_speech(self):
        """Convert speech to text using the microphone."""
        with sr.Microphone() as source:
            print("Listening... Speak something!")
            try:
                audio = self.recognizer.listen(source, timeout=self.timeout, phrase_time_limit=self.phrase_time_limit)
                text = self.recognizer.recognize_google(audio)
                print("You said:", text)
                return text
            except sr.UnknownValueError:
                print("Sorry, I could not understand your speech.")
            except sr.RequestError:
                print("Sorry, there seems to be an issue with the STT service.")
            except Exception as e:
                logging.error(f"Error in Speech-to-Text: {e}")
        return ""


def choose_voice():
    """Allow user to choose between different language-accent options for TTS."""
    print("Choose a voice for Text-to-Speech:")
    print("1. English (US)")
    print("2. English (UK)")
    print("3. Spanish (Spain)")
    print("4. Spanish (Mexico)")
    print("5. French")
    print("6. German")
    print("7. Italian")

    choice = input("Enter the number corresponding to the voice you want: ")

    voice_mapping = {
        "1": "en",
        "2": "en-uk",
        "3": "es",
        "4": "es-mx",
        "5": "fr",
        "6": "de",
        "7": "it"
    }

    return voice_mapping.get(choice, "en")  # Default to English if input is invalid


def main():
    """Main program loop to choose and execute TTS or STT."""
    tts = None
    stt = SpeechToText(timeout=5, phrase_time_limit=10)

    print("Choose an operation:")
    print("1. Text to Speech")
    print("2. Speech to Text")

    operation = input("Enter 1 or 2: ")

    if operation == "1":
        # Text-to-Speech
        language = choose_voice()
        tts = TextToSpeech(language=language, slow=False)
        text = input("Enter the text you want to convert to speech: ")
        tts.speak(text)

    elif operation == "2":
        # Speech-to-Text
        recognized_text = stt.recognize_speech()
        if recognized_text:
            response = f"You said: {recognized_text}. Have a great day!"
            if tts:
                tts.speak(response)
    else:
        print("Invalid selection. Please choose either 1 or 2.")


if __name__ == "__main__":
    main()
