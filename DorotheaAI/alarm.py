import datetime
import os
import time as t
import pyttsx3
from gui import validate_time_format

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

def read_alarm_time(file_path):
    """
    Reads the alarm time from the specified file.
    """
    with open(file_path, 'rt') as file:
        time_str = file.read().strip()

    return time_str

def ring(alarm_time):
    """
    Rings the alarm at the specified time.
    """
    print(f"Alarm set for: {alarm_time}")

    while True:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        if current_time == alarm_time:
            say('Wake up, alarm is ringing since ages!')
            os.startfile("C:/Users/avish/Downloads/night.mp3")

        t.sleep(1)  # Sleep for a second to avoid excessive CPU usage

if __name__ == "__main__":
    alarm_raw_time = read_alarm_time('alarmtext.txt')
    if alarm_raw_time:
        ring(alarm_raw_time)
    else:
        print("Invalid alarm time format.")
