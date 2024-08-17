import googletrans
from googletrans import Translator
import pyttsx3
import speech_recognition as sr

def say(text):
    """
    Function to set up the voice engine
    """
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()

def take_command():
    """
    Function to take voice commands
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an error with the request.")
            return ""

def translate_google(query):
    """
    Function to translate into different languages
    """
    say("Definitely, finally you are exploring other languages.")
    print(googletrans.LANGUAGES)  # List all available languages
    # Calling Translator()
    translator = Translator()

    say("Please state the language you want to translate into.")
    # Taking command for the language to be translated into
    target_language_command = take_command()

    # Process the voice command to extract the language code
    target_language = None
    for code, language in googletrans.LANGUAGES.items():
        if language in target_language_command:
            target_language = code
            break

    if not target_language:
        print("Invalid language code. Please try again.")
        say("Invalid language code. Please try again.")
        return

    try:
        # Translate the text
        translated_text = translator.translate(query, src="auto", dest=target_language)

        # Check if translation was successful
        if translated_text is not None and hasattr(translated_text, 'text'):
            text = translated_text.text
            print(f"Translated Text: {text}")
            say(text)

        else:
            print("Translation failed.")
            say("Translation failed. Please try again.")
    except Exception as e:
        print(f"Unable to translate due to: {str(e)}")
        say("Unable to translate. Please try again.")

