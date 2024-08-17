import pyttsx3
import speech_recognition as sr
import random

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
    engine.setProperty('volume', 0.9)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

def take_command():
    """
    Function to take voice commands
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Dynamically adjust for ambient noise levels
        print("Calibrating microphone for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=2)

        # Set the pause threshold to be more forgiving for short pauses
        r.pause_threshold = 0.8

        print("Listening...")
        try:
            # Increase timeout and phrase_time_limit if needed
            audio = r.listen(source, timeout=10, phrase_time_limit=10)

            print("Recognizing...")
            query = r.recognize_google(audio, language="en-US")
            print(f"User said: {query}")
            return query

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start. Please try again.")
            return "Some error occurred. Sorry!."
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return "Some error occurred. Sorry!."
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return "Some error occurred. Sorry!."


def game_play():
    """
    This function lets user play rock, paper and scissors with Dorothea
    """
    say("Lets Play ROCK PAPER SCISSORS !!")
    print("LETS PLAYYYYYYYYYYYYYY")
    i = 0
    # Initializing the user's and Dorothea's score
    Me_score = 0
    Com_score = 0
    # There would be 5 turns for players
    while (i < 5):
        # Tuple having game moves
        choose = ("rock", "paper", "scissors")
        # Letting Dorothea choose a move
        com_choose = random.choice(choose)
        # Letting user choose a move and say it
        query = take_command().lower()
        # If the user chooses rock
        if (query == "rock"):
            # And if Dorothea chooses rock
            if (com_choose == "rock"):
                say("ROCK")
                # No points as same moves
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            # And if Dorothea chooses paper
            elif (com_choose == "paper"):
                say("paper")
                # Dorothea gets a point
                Com_score += 1
                # Printing the score
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                say("Scissors")
                # If Dorothea got scissors then the user wins
                # User gets a point
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

        # If the user chooses paper
        elif (query == "paper"):
            # And if Dorothea chooses rock
            if (com_choose == "rock"):
                say("ROCK")
                # User wins and gets a point
                Me_score += 1
                print(f"Score:- ME :- {Me_score + 1} : COM :- {Com_score}")

            # And if Dorothea chooses paper
            elif (com_choose == "paper"):
                say("paper")
                # Same moves so no points
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                say("Scissors")
                # Dorothea gets a point in this case
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

        # If the user chooses scissors/scissor
        elif (query == "scissors" or query == "scissor"):
            # And if Dorothea chooses rock
            if (com_choose == "rock"):
                say("ROCK")
                # Dorothea gets a point in this case
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            # And if Dorothea chooses paper
            elif (com_choose == "paper"):
                say("paper")
                # User gets a point in this case
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                say("Scissors")
                # No points since same move
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
        # Increasing i with 1
        i += 1
    # Printing the final score
    print(f"FINAL SCORE :- ME :- {Me_score} : COM :- {Com_score}")