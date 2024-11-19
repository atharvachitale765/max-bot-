import subprocess
import pyttsx3
import datetime
import speech_recognition as sr
import os
import sys
from sys import platform
import wikipedia    
import platform
import pyjokes
import pyowm
import webbrowser
import random
import json
import requests
import urllib.parse

engine = pyttsx3.init('espeak', 'sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

with open("queries.json", "r") as file:
    queries_config = json.load(file)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello, I am Max! ,  How should I call you?")
    name = input("Enter Your name: ")
    speak(f'Hello {name}! , How can I help you today?')


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source, duration=1)

        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "None"
    except Exception as e:
        if 'ALSA lib' in str(e):
            # Supresses unnecssary Linux ALSA Errors.
            subprocess.call(["python3", "main.py"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print("Error:", e)
        speak("Say that again, please...")
        return "None"
    return query.lower()


def search_wikipedia(query):
    try:
        speak('Searching Wikipedia...')
        results = wikipedia.summary(query, sentences=1)
        speak('According to Wikipedia:')
        speak(results)
    except wikipedia.exceptions.PageError:
        speak('Sorry, I could not find any information on that topic.')
    except wikipedia.exceptions.DisambiguationError:
        speak('There are multiple options for this topic. Please be more specific.')


def open_app(app_name):
    system = platform.system().lower()

    try:
        if system == "windows":
            subprocess.Popen(["start", " ", app_name], shell=True)
        elif system == "darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
        elif system == "linux":
            subprocess.Popen(["xdg-open", app_name])
        else:
            print(f"Unsupported operating system: {system}")
    except Exception as e:
        print("Error opening the application:", e)


def get_weather():
    try:
        response = requests.get("https://wttr.in/City?format=%t+%C+%w")
        if response.status_code == 200:
            weather_info = response.text
            return f"The current weather in City is {weather_info}."
        else:
            return "Sorry, I couldn't fetch the weather information at the moment."
    except Exception as e:
        return f"Error: {e}"


def get_date():
    now = datetime.datetime.now()
    return now.strftime("Today is %A, %d %B %Y.")


def get_random_fact():
    facts = [
        "The Eiffel Tower can grow up to 6 inches taller during the summer.",
        "Polar bears have black skin under their white fur.",
        "The strongest muscle in the human body is the tongue.",
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly safe to eat.",
        "Octopuses have three hearts. Two pump blood through the gills, and one pumps blood through the rest of the body.",
        "A group of flamingos is called a 'flamboyance.'",
        "The fingerprints of a koala are so indistinguishable from humans that they have, on occasion, been confused at a crime scene.",
        "Bananas are berries, but strawberries are not.",
    ]
    return random.choice(facts)


def play_youtube(query):
    search_query = urllib.parse.urlencode({'search_query': query})
    search_url = f"https://www.youtube.com/results?{search_query}"

    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            videos = []
            results = response.text.split(
                '{"commandMetadata":{"webCommandMetadata":{"url":"/watch?v=')
            for result in results[1:]:
                video_id = result.split('"')[0]
                title = result.split('title":{"runs":[{"text":"')[
                    1].split('"')[0]
                videos.append({'title': title, 'video_id': video_id})

            # Assume the first result is the desired video
            if videos:
                first_video = videos[0]
                video_url = f"https://www.youtube.com/watch?v={first_video['video_id']}"
                speak(f"Playing video: {first_video['title']}")
                webbrowser.open(video_url)
            else:
                speak("Sorry, I couldn't find any relevant videos.")

        else:
            speak("Sorry, I couldn't fetch YouTube search results at the moment.")
    except Exception as e:
        speak(f"Error: {e}")


def process_query(query):
    if query in queries_config["greetings"]:
        speak("How can I help you?")
    elif query in queries_config["goodbyes"]:
        speak("Goodbye!")
        exit()
    elif query in queries_config["jokes"]:
        joke = pyjokes.get_joke()
        speak(joke)
    elif query in queries_config["weather"]:
        weather_info = get_weather()
        speak(weather_info)
    elif query in queries_config["time"]:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif query in queries_config["wikipedia"]:
        speak("What do you want to search on Wikipedia?")
        search_query = take_command()
        search_wikipedia(search_query)
    elif query in queries_config["open_app"]:
        app_name = query.split("open ")[-1]
        open_app(app_name)
    elif query in queries_config["random_fact"]:
        fact = get_random_fact()
        speak(fact)
    elif query in queries_config["youtube"]:
        if "play video" in query:
            speak("Sure, what topic or channel would you like to watch?")
            video_query = take_command()
            search_query = f"https://www.youtube.com/results?search_query={video_query.replace(' ', '+')}"
            speak(f"Playing videos related to {video_query} on YouTube.")
            webbrowser.open(search_query)
    elif "search google for" in query:
        search_query = query.replace("search Google for", "").strip()
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        speak(f"Searching Google for {search_query}")
        webbrowser.open(search_url)

    elif query.startswith("play") and "on youtube" in query:
        topic = query.split("play")[-1].replace("on youtube", "").strip()
        topic = f"youtube.com/results?search_query={topic.replace(' ', '+')}"
        speak(f"Playing videos related to {topic} on YouTube.")
        webbrowser.open(topic)

    else:
        speak("Sorry, I don't understand that command.")

## Only for Surpassing ASLA unwanted messages on Linux.##


def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


if __name__ == "__main__":
    wish_me()
    take_command()

    while True:
        query = take_command()
        process_query(query)
