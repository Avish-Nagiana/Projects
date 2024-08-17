import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep

# Dictionary having some apps as keys and their nicknames as values
app_dict = {'commandprompt': 'cmd',
            'word': 'winword',
            'excel': 'excel',
            'chrome': 'chrome',
            'vscode': 'vscode',
            'pycharm': 'pycharm',
            'github': 'githubdesktop',
            'music': 'applemusic',
            'mail': 'outlook',
            'whatsapp':'whatsapp',
            'powerpoint': 'powerpoint'}

def say(text):
    """
    Function to set up the voice engine
    """
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

def open_app_web(query):
    """
    Function to open applications and websites
    """
    say("Just a second my friend!")

    # Checking if the query has words to identify a website
    if '.com' in query.lower() or '.org' in query.lower() or '.net' in query.lower():
        # Replacing some words in query
        query = query.replace('open','')
        query = query.replace('dorothea', '')
        query = query.replace('launch', '')
        query = query.replace(' ', '')
        # Opening the website
        webbrowser.open(f"https://www.{query}")

    else:
        # Opening the application
        keys = list(app_dict.keys())
        for app in keys:
            if app in query.lower():
                os.system(f'start {app_dict[app]}')


def close_app_web(query):
    """
    Function to close applications and websites
    """
    say("Just a second my friend!")
    # If any tab/tabs are asked to close
    if 'one tab' in query.lower() or '1 tab' in query.lower():
        pyautogui.hotkey('ctrl', 'w')
        say("Everything seems to be closed now.")

    elif 'two tabs' in query.lower() or '2 tabs' in query.lower():
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        say("Everything seems to be closed now.")

    elif 'three tabs' in query.lower() or '3 tabs' in query.lower():
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        say("Everything seems to be closed now.")

    elif 'four tabs' in query.lower() or '4 tabs' in query.lower():
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        say("Everything seems to be closed now.")

    elif 'five tabs' in query.lower() or '5 tabs' in query.lower():
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
        say("Everything seems to be closed now.")

    else:
        # Closing the application
        keys = list(app_dict.keys())
        for app in keys:
            if app in query.lower():
                os.system(f"taskkill /f /im {app_dict[app]}.exe")
