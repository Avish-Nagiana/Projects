import re
import subprocess
import tkinter as tk
from tkinter import *
import threading
import queue
import speech_recognition as sr
import datetime
import random
from plyer import notification
import pygame
import openai
from config import apikey
from translator import translate_google
from search import *
from app import *
from time_pass_game import game_play
from calculator import calculate
from search import *
from PIL import Image, ImageTk
from tkinter import ttk

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def say(text):
    """
    Function to speak the text.
    """
    engine.say(text)
    engine.runAndWait()

def take_command():
    """
    Function to listen to voice commands
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Dynamically adjust for ambient noise levels
        # Commented to decrease time taken to execute
        #print("Calibrating microphone for ambient noise...")
        #r.adjust_for_ambient_noise(source, duration=2)

        # Set the pause threshold to be more forgiving for short pauses
        r.pause_threshold = 0.8

        print("Listening...")
        try:
            # Increase timeout and phrase_time_limit if needed
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            print("Recognizing...")
            # Recognizing voice input according to US English vocabulary
            query = r.recognize_google(audio, language="en-US")
            print(f"User said: {query}")
            # Return the recognized voice command
            return query
        # Handling listening timed out error.
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to "
                  "start. Please try again.")
            return "No response"
        # Handling error for non-understandable commands
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return "No response"
        # Handling error caused due to request issues
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech "
                  f"API; {e}")
            return "No response"

def greet_me():
    """
    This function basically greets the user depending on the time.
    """
    # Getting the hour of the current time
    hour = int(datetime.datetime.now().hour)
    # Checking if hour is more than 0 and less than 12
    if hour >= 0 and hour <= 12:
        # Wishing morning in this case
        return "Good Morning friend!"
    # Checking if the hour is more than 12 and less than 18
    elif hour > 12 and hour <= 18:
        # Wishing afternoon in this case
        return "Good Afternoon friend!"
    # If none above, then this gets executed
    else:
        return "Good Evening friend!"

def password_protect(gui):
    """
    Function to protect the voice assistant with a password and run
    the rest of the code only if the entered one matches the set one.
    """
    # Giving three chances to enter the correct password
    for i in range(3):
        # command shown on screen to ask for voice input of password
        gui.insert_command("Maybe Dorothea: Please speak the secret "
                           "code to wake up Dorothea.\n")
        # Taking the voice input
        entry = take_command()

        # Normalize the entry text according to the set password
        normalized_entry = entry.replace("I'll", "I will")

        # Opening the file having the password in read mode
        with open("top_secret.txt", "r") as code_file:
            # Reading the password
            # Removing any extra whitespace
            read_code = code_file.read().strip()
        # If the entry and the code in the file matches
        if normalized_entry == read_code:
            gui.insert_command("Dorothea: So you know the secret. "
                               "Now, ask me to wake up politely.")
            # True is returned since the entry is correct
            return True
        else:
            print("Incorrect code.")
            if i == 2:  # Checking if it's the last attempt
                print("You have entered the wrong code too many "
                      "times. Exiting.")
                exit()

def chat(query):
    """
    Function to chat and interact with the openai
    """
    # Making a global variable
    global chatStr
    chatStr = ""
    # Getting the api key for the openai
    openai.api_key = apikey
    # Setting up the chatStr
    chatStr += f"Avish: {query}\n Dorothea: "
    # Fetching the response from openai for the chatStr
    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Saying the response received
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    # Fetching the openai apikey
    openai.api_key = apikey
    text = (f"OpenAI response for Prompt: {prompt} \n ****************"
            f"*********\n\n")
    # Getting the response for the entered prompt
    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

def parse_time_input(time_string):
    """
    Function to parse the time according to different patterns
    """
    # Defining regex patterns for different time formats including AM/PM
    patterns = [
        r'(\d{1,2}):(\d{2})(:(\d{2}))?\s*(am|pm)?',  # HH:MM[:SS] AM/PM
        # Hours Minutes Seconds AM/PM
        r'(\d{1,2})\s*hours?\s*(\d{1,2})\s*minutes?\s*(\d{1,2})\s*seconds?\s*(am|pm)?',
        r'(\d{1,2})\s*(am|pm)?'  # Only hours and AM/PM
    ]

    # Normalizing the time string
    time_string = time_string.lower()
    print(f"Normalized time string: {time_string}")  # Debug print

    # Checking for the pattern
    for pattern in patterns:
        # Matching the pattern of the time string
        match = re.match(pattern, time_string)
        # If it matches, then this code will execute
        if match:
            # Checking if it matched with the mentioned pattern
            if pattern == r'(\d{1,2}):(\d{2})(:(\d{2}))?\s*(am|pm)?':
                hours, minutes, _, seconds, period = match.groups()
                if not minutes:
                    minutes = '00'
                if not seconds:
                    seconds = '00'
                # Converting to 24-hour format
                if period:
                    if period == 'pm' and int(hours) < 12:
                        hours = str(int(hours) + 12)
                    elif period == 'am' and int(hours) == 12:
                        hours = '00'
                result = f"{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}"
                print(f"Parsed time: {result}")  # Debug print
                return result

            elif pattern == r'(\d{1,2})\s*hours?\s*(\d{1,2})\s*minutes?\s*(\d{1,2})\s*seconds?\s*(am|pm)?':
                hours, minutes, seconds, period = match.groups()
                # Converting to 24-hour format
                if period:
                    if period == 'pm' and int(hours) < 12:
                        hours = str(int(hours) + 12)
                    elif period == 'am' and int(hours) == 12:
                        hours = '00'
                result = f"{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}"
                print(f"Parsed time: {result}")  # Debug print
                return result

            elif pattern == r'(\d{1,2})\s*(am|pm)?':
                hours, period = match.groups()
                # Converting to 24-hour format
                if period:
                    if period == 'pm' and int(hours) < 12:
                        hours = str(int(hours) + 12)
                    elif period == 'am' and int(hours) == 12:
                        hours = '00'
                result = f"{hours.zfill(2)}:00:00"
                print(f"Parsed time: {result}")  # Debug print
                return result
    # None will be returned if there is no matching pattern
    return None


def validate_time_format(time_string):
    """
    Function to validate the time format
    """
    try:
        # Checking if the time format matches '%H:%M:%S'
        datetime.datetime.strptime(time_string, '%H:%M:%S')
        # Returning true if it matches
        return True
    except ValueError:
        return False

def set_alarm(gui):
    """
    Function to set an alarm using voice input
    """
    # Setting the status of the voice assistant on gui
    gui.set_status("Setting up alarm.")
    # Asking for time input to set alarm
    say("Please tell me the time to set the alarm. You can say it in "
        "12-hour format like '2:30 PM' or 24-hour format like '14:30:00'.")

    # Clear the alarm text file before writing new time
    with open('alarmtext.txt', 'w') as file:
        file.truncate()

    while True:
        # Taking the time input and parsing it.
        time_input = take_command().lower()
        parsed_time = parse_time_input(time_input)

        # Checking if the time parsed and satisfies the time format
        if parsed_time and validate_time_format(parsed_time):
            # Write=ing the parsed time to alarmtext.txt
            with open('alarmtext.txt', 'w') as file:
                file.write(parsed_time)

            # Confirming the alarm is set
            gui.set_status("Alarm set! You better wake up!")
            gui.insert_command(f"Dorothea: Done and dusted!")
            # Telling the alarm time as a confirmation
            say(f"Done! I hope you wake up when that alarm rings at {parsed_time}!")

            # Running the alarm.py script to wait for the alarm time
            subprocess.Popen(["python", "alarm.py"])

            break
        else:
            say("Invalid time format. Please try again.")
            gui.set_status("Invalid time format. Please try again.")

def search_songs(directory, query):
    """
    Function to search songs
    """
    # Declaring an empty list
    songs = []
    # Checking for a file in a directory
    for file in os.listdir(directory):
        # Checking if the file matches any of the mentioned below
        if file.endswith(('.mp3', '.wav', '.ogg')) and query in file.lower():
            # If there is such file then appending it in the list
            songs.append(file)
    # Returning the list
    return songs

def play_song(song_path):
    """
    Function to play songs using its file path
    """
    # Initializing the pygame mixer
    pygame.mixer.init()
    # Loading the song file
    pygame.mixer.music.load(song_path)
    # Playing the song file
    pygame.mixer.music.play()
    print(f"Playing: {song_path}")

# Declaring a dictionary
# Number words as keys and the number values as values
number_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}

def get_task_number():
    """
    Function to get the number of tasks to be set
    """
    while True:
        # Asking for the number of tasks
        say("How many tasks do you want to schedule?")
        # Taking the voice command
        command = take_command()

        # Checking if the command contains a number word or digit
        for word in command.split():
            # If the word is digit then returning the integer
            if word.isdigit():
                return int(word)
            # Else returning the value after matching in the dictionary
            elif word in number_words:
                return number_words[word]

        # Additional check for phrases like "three tasks"
        for key, value in number_words.items():
            if key in command:
                return value

        say("Please speak a valid number.")

def schedule_tasks():
    """
    Function to schedule the number of tasks desired
    """
    tasks = []
    # Asking if the previous tasks are wished to be removed
    say("Do you want to remove the previous tasks? Yes or No?")
    # Taking user command
    query = take_command()

    if "yes" in query:
        with open("tasks.txt", "w") as file:
            # Clearing the file content
            # Basically the previous tasks
            file.write("")

    def add_tasks(task_numbers):
        """
        A sub-function to add the tasks in the tasks.txt file
        """
        # Opening the file and taking user input for the tasks
        with open("tasks.txt", "a") as file:
            for i in range(task_numbers):
                say(f"Please speak the task number {i+1}.")
                task = take_command().strip()
                tasks.append(task)
                file.write(f"{i + 1} - {tasks[i]}\n")

    # Calling the functions to execute their codes
    task_numbers = get_task_number()
    add_tasks(task_numbers)
    say("Schedule is set.")

def handle_command(command_queue, gui):
    """
    This function handles all the user commands and provides
    the desired outputs.
    """
    # Checking if the password protect function returns True
    if password_protect(gui):
        gui.set_status("Initializing...")

    while True:
        gui.set_status("Listening for command...")
        # Taking the user voice command
        query = take_command().lower()

        # If there is a successful voice input
        # Inserting the command on the gui window
        if query:
            gui.insert_command(f"\nUser said: {query}")
            command_queue.put(query)

            # If the user says wake up then this code executes
            if "wake up" in query:
                gui.set_status("Greeting...")
                # Calling the greet_me()
                response_greet = greet_me()
                # Saying the response received from the function
                say(response_greet)
                # Putting the response on the gui
                gui.insert_command(f"Dorothea: {response_greet}")
                # Asking the user how they need to be assisted
                say("Dorothea this side, please tell me, how may I help you today?")
                gui.set_status("Ready for action, bring it on!")
                music_directory = "C:/Users/avish/Downloads"

                while True:
                    # Further asking for command once Dorothea is up
                    query = take_command().lower()

                    # If there is a successful voice input
                    # Inserting the command on the gui window
                    if query:
                        gui.insert_command(f"\nUser said: {query}")

                        # Some common sites and their urls
                        sites = [['maps', 'https://maps.google.com/'],
                                 ['gpt', 'https://chatgpt.com'],
                                 ['linkedin', 'www.linkedin.com/in/avish-nagiana-9ba44b2b8'],
                                 ['youtube', 'www.youtube.com']]

                        # Checking for site is the sites list
                        for site in sites:
                            # If user asks for opening a site in query
                            if f"Open {site[0]}".lower() in query:
                                say(f"Opening {site[0]} for you in a second.")
                                # Opening that site using webbrowser.open()
                                webbrowser.open(site[1])

                        # If the user asks Dorothea to take some rest
                        # Then the code will break
                        # It won't take any voice input
                        # Wake up command is to make Dorothea work again
                        if "take some rest" in query:
                            gui.set_status("Snacks Time!")
                            say("Just ask me to wake up again if you "
                                "need me. Toodles!")
                            gui.insert_command("Dorothea: Toodles!")
                            break

                        # If the user asks to play music in the query
                        elif "play music" in query:
                            gui.set_status("Searching for music...")
                            # Asking for the song name to be played
                            say("What song would you like to play?")
                            # Voice command being taken here
                            song_query = take_command()
                            # Inserting the command on the gui
                            gui.insert_command(f"\nUser said: "
                                               f"{song_query}")
                            if song_query:
                                # Checking for matching songs
                                matching_songs = search_songs(music_directory, song_query)
                                # If there is a matching song
                                if matching_songs:
                                    # Specifying the path of the file
                                    song_path = os.path.join(music_directory, matching_songs[0])
                                    # Playing the song
                                    play_song(song_path)
                                    response = f"Playing {matching_songs[0]}."
                                else:
                                    # Telling no matching songs are there
                                    response = "No matching songs found."
                                    gui.set_status("No matching songs found.")

                                say(response)
                                gui.insert_command(f"Dorothea: {response}")

                        # If user asks to stop the music in query
                        elif "stop music" in query:
                            gui.set_status("Stopping the music.")
                            # Stopping the music being played
                            pygame.mixer.music.stop()
                            response = "Music stopped."
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")

                        # Changing the password / secret code
                        elif "change secret code" in query:
                            gui.set_status("Changing the secret code.")
                            say("What's the new secret code?")
                            # Taking voice input for new code
                            new_code = take_command()
                            # Writing the new code in the file
                            with open("top_secret.txt", "w") as code_file:
                                code_file.write(new_code)
                            gui.set_status("Top secret changed, damn!")
                            response = "Top secret code has been changed!"
                            say(response)
                            # Saying the new code for confirmation
                            say(f"Just to be clear the new secret code is {new_code}.")
                            gui.insert_command(f"Dorothea: {response}")

                        # If the user asks for weather
                        elif "weather" in query:
                            gui.set_status("Weather report is up captain!")
                            say(f"Opening weather forecast for you right now.")
                            # Simply opening up a weather site
                            webbrowser.open("https://www.accuweather.com/en/ca/winnipeg/r3b/weather-forecast/48989")
                            gui.insert_command("Dorothea: Opening weather forecast.")

                        # If the user wants to pause the YouTube video
                        elif "pause" in query:
                            gui.set_status("Pausing the video.")
                            # Using pyautogui
                            # To press key 'k' command to system
                            # 'k' is basically pressed to pause
                            pyautogui.press("k")
                            response = "video paused"
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")

                        # If the user wants to resume the YouTube video
                        elif "resume" in query:
                            gui.set_status("Resuming the video.")
                            # Using pyautogui
                            # To press key 'k' command to system
                            # 'k' is basically pressed to resume
                            # pause and resume are interchangeable
                            pyautogui.press("k")
                            response = "video resumed"
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")

                        # If the user wants to mute the YouTube video
                        elif "mute" in query:
                            gui.set_status("Muting the video.")
                            # Using pyautogui
                            # To press key 'm' command to system
                            # 'm' is basically pressed to mute
                            pyautogui.press("m")
                            response = "video muted"
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")

                        # If the user wants to unmute the YouTube video
                        elif "unmute" in query:
                            gui.set_status("Unmuting the video.")
                            # Using pyautogui
                            # To press key 'm' command to system
                            # 'm' is basically pressed to unmute
                            pyautogui.press("m")
                            response = "video unmuted"
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")

                        # If the user wants to increase the volume
                        elif "volume up" in query:
                            gui.set_status("Voluming up.")
                            # Importing volumeup function
                            from keyboard import volumeup
                            response = "Turning volume up as requested"
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")
                            # Calling the function
                            volumeup()

                        # If the user wants to decrease the volume
                        elif "volume down" in query:
                            gui.set_status("Voluming down.")
                            # Importing volumedown function
                            from keyboard import volumedown
                            response = "Turning volume down as requested"
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")
                            # Calling the function
                            volumedown()

                        # If user wants Dorothea to remember something
                        elif "remember that" in query:
                            gui.set_status("I will try to keep that in mind.")
                            # Replacing the words in query
                            remember_message = query.replace("dorothea", "").replace("i", "you")
                            say("You asked me to" + remember_message)
                            # Opening the file and writing the note
                            with open("remember.txt", "w") as remember:
                                remember.write(remember_message)
                            response = "Note saved"
                            say(response)
                            gui.insert_command(f"Dorothea: {response}")

                        # If user wants Dorothea to remind them the note
                        elif "do you remember" in query:
                            gui.set_status("I guess I remember.")
                            # Reading the note from the file
                            with open("remember.txt", "r") as remember:
                                say("Well, you asked me to" + remember.read())
                            gui.insert_command("Dorothea: I guess I "
                                               "have a good memory.")

                        # If user wants to create day's schedule
                        elif "schedule my day" in query:
                            gui.set_status("Setting up the schedule.")
                            # Calling the function
                            schedule_tasks()
                            gui.insert_command("Dorothea: Tasks "
                                               "scheduled (which you "
                                               "might not even get done"
                                               " hehe!).")

                        # If user wants to see the schedule set
                        elif "show my schedule" in query:
                            gui.set_status("Better get those tasks done.")
                            # Reading the tasks from the file
                            with open("tasks.txt", "r") as file:
                                content = file.read()
                            # Using pygame mixer to play alert sound
                            pygame.mixer.init()
                            pygame.mixer.music.load("schedule_alert.mp3")
                            pygame.mixer.music.play()
                            # Using notify() from notification library
                            # This creates a small notification window
                            notification.notify(
                                title="My Schedule",
                                message=content,
                                timeout=15,
                                app_name="Dorothea",
                                app_icon=None
                            )
                            gui.insert_command("Dorothea: See your "
                                               "screen silly!")

                        # If user wants to take a screenshot
                        elif "screenshot" in query:
                            gui.set_status("Screen says cheese!")
                            # Using ppyautogui to take screenshot
                            sshot = pyautogui.screenshot()
                            # Saving the screenshot
                            sshot.save("screen_shot.jpg")
                            gui.insert_command("Dorothea: Took a cute"
                            " pic of the screen and saved it.")

                        # If the user wants to open something
                        elif "open" in query:
                            gui.set_status("Opening")
                            # Calling the function
                            open_app_web(query)
                            gui.insert_command("Dorothea: Opening")

                        # If the user wants to google something
                        elif "google" in query:
                            gui.set_status("Texting my friend Google.")
                            # Calling the search_google()
                            search_google(query)
                            gui.insert_command("Dorothea: Google is"
                                               " working so good.")

                        # If the user wants to play something on YouTube
                        elif "youtube" in query:
                            gui.set_status("Youtube here I am!")
                            # Calling the function
                            search_youtube(query)
                            gui.insert_command("Dorothea: Youtube is"
                                               " open now.")

                        # If user wants to search something on wikipedia
                        elif "wikipedia" in query:
                            gui.set_status("Studying on wikipedia!")
                            search_wikipedia(query)
                            gui.insert_command("Dorothea: Wikipedia "
                                               "is up.")

                        # If user wants to play a game with Dorothea
                        elif "play game" in query:
                            gui.insert_command("Dorothea: Game Time!")
                            gui.set_status("It is game time, finally!")
                            # Calling the game_play()
                            game_play()
                            say("Game finished.")

                        # If the user wants to calculate something
                        elif "calculate" in query:
                            gui.set_status("Need to revise maths to"
                                           " calculate.")
                            say("What should I calculate?")
                            # Taking the command for calculating
                            calculation_query = take_command()
                            if calculation_query:
                                # Calling the calculate()
                                result = calculate(calculation_query)
                                gui.set_status("Wow! I still know maths.")
                                say(f"The result is {result}")
                            gui.insert_command(f"Dorothea: The result"
                                               f" is {result}")

                        # If the user wants to translate something
                        elif "translate" in query:
                            gui.insert_command("Dorothea: Translating"
                                               " for you because I am"
                                               " better than you, hehe!")
                            gui.set_status("Translating for you.")
                            # Replacing some words in the query
                            query = query.replace("dorothea", "")
                            query = query.replace("translate", "")
                            query = query.replace("for me", "")
                            # Calling the translate_query()
                            translate_google(query)

                        # If the user wants to set an alarm
                        elif "set an alarm" in query or "alarm" in query:
                            # Calling the function
                            set_alarm(gui)

                        # If user wants Dorothea to pick a song for you
                        elif "any song in your mind" in query:
                            gui.insert_command("Dorothea: Song, huh!")
                            gui.set_status("Thinking which song to play, hmm!")
                            say("Let me think, what about this one?")
                            # A tuple of numbers
                            a = (1, 2, 3, 4, 5, 6)
                            # Choosing a random number from tuple a
                            b = random.choice(a)
                            # Playing the number on basis of choice
                            if b == 1:
                                webbrowser.open("https://youtu.be/UZhBMj5EZhM?si=godrjZo9UeW5Vczw")
                            elif b == 2:
                                webbrowser.open("https://youtu.be/MqdLD2YX-Zo?si=Bph46wl1gLtb2AcZ")
                            elif b == 3:
                                webbrowser.open("https://youtu.be/hbcGx4MGUMg?si=Eqw0liyv6c-lPdw7")
                            elif b == 4:
                                webbrowser.open("https://youtu.be/i8_w_m6HLJ0?si=iRsC15AsXcQhZUYA")
                            elif b == 5:
                                webbrowser.open("https://youtu.be/H5v3kku4y6Q?si=7DRR3QqRV6DEKIQd")
                            elif b == 6:
                                webbrowser.open("https://youtu.be/bGZplqeIb3w?si=HXPx35Lk2EQrI-7R")
                            else:
                                say("Ran into some error, maybe try "
                                    "again!")

                            gui.insert_command("I hope so you like "
                                               "this one.")

                        # If user wants to use AI from openai
                        elif ("Using artificial intelligence".lower()
                              in query):
                            # Calling the function
                            ai(prompt=query)

                        # If the user wants to chat with Dorothea
                        elif "chat" in query:
                            gui.set_status("Chatting")
                            # Calling the function
                            chat(query)
                            gui.insert_command(f"Dorothea: {response}")

                        # If the user wants to put Dorothea to sleep
                        # Or exit from the voice assistant
                        elif "go to sleep" in query:
                            gui.set_status("Hello to my cozy pillow!")
                            say("Hope so I was helpful. Have a great day!")
                            gui.insert_command("Dorothea: Sleeping time!")
                            # Closing the gui window
                            gui.close_window()

                        # If the user's command isn't understandable
                        # Then setting the status
                        else:
                            gui.set_status("Sorry, can you repeat?")

                    else:
                        gui.insert_command("")

            else:
                gui.insert_command("")

# Creating a class for the gui
class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        # Setting the window's title
        self.root.title("Dorothea: Your AI Friend")
        # Setting the window's size
        self.root.geometry("600x500")

        # Loading and displaying the background image for the entire window
        self.bg_image = Image.open("Gemini_Generated_Image_leui6nleui6nleui.jpeg")
        self.bg_image = self.bg_image.resize((600,500))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.background_label = tk.Label(root, image=self.bg_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Setting the dimensions and position for the text area
        text_area_x = 90 # Adjusting the X position
        text_area_y = 200 # Adjusting the Y position
        text_area_width = 400 # Adjusting the width
        text_area_height = 145  # Adjusting the height

        # Creating a Text widget in the specific area
        self.command_text = Text(root, wrap=tk.WORD, bd=0, bg="#4e4f4a",
                                 fg="white", font=("Helvetica", 9))
        self.command_text.place(x=text_area_x,
                                y=text_area_y,
                                width=text_area_width,
                                height=text_area_height)

        # Creating a custom ttk Scrollbar
        # and attaching it to the Text widget
        scrollbar = ttk.Scrollbar(root,
                                  orient="vertical",
                                  command=self.command_text.yview)

        # Configuring the Scrollbar's appearance
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Vertical.TScrollbar",
                        troughcolor="#4e4f4a",
                        background="#4e4f4a",
                        darkcolor="#4e4f4a",
                        lightcolor="#4e4f4a",
                        arrowcolor="white")

        # Placing the Scrollbar and linking it to the Text widget
        scrollbar.place(x=text_area_x + text_area_width,
                        y=text_area_y,
                        height=text_area_height)
        self.command_text.config(yscrollcommand=scrollbar.set)

        # Status label on the main window
        self.status_label = tk.Label(root,
                                     text="Dorothea is asleep.",
                                     font=("Arial", 10),
                                     bg="black",
                                     fg="white")
        self.status_label.pack(side = tk.TOP, pady=150, anchor='n')

        # Command queue for updating the GUI
        self.command_queue = queue.Queue()
        self.update_gui()

    def set_status(self, status):
        """
         Function to set Dorothea's current status
        """
        self.status_label.config(text=status)

    def insert_command(self, command):
        """
        Function to insert commands on gui window
        """
        self.command_text.insert(tk.END, f"{command}\n")
        self.command_text.yview(tk.END)  # Scroll to the end

    def update_gui(self):
        """
        Function to update the gui window
        """
        try:
            command = self.command_queue.get_nowait()
            #self.insert_command(f"Command received: {command}")
        except queue.Empty:
            pass
        self.root.after(100, self.update_gui)  # Check the queue every 100 ms

    def close_window(self):
        """
        Function to close the window and exit the code
        """
        self.root.destroy()

def main():
    """
    Function that creates the base of gui window
    """
    # Creating the root window using tkinter
    root = tk.Tk()
    # Passing the root
    gui = VoiceAssistantGUI(root)
    # Creating threads
    assistant_thread = threading.Thread(target=handle_command,
                                        args=(gui.command_queue, gui),
                                        daemon=True)
    assistant_thread.start()
    # Putting root on loop
    root.mainloop()

if __name__ == "__main__":
    # Calling the main function
    main()
