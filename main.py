import pyttsx3
import random
import datetime
import speech_recognition as sr 
import os
import wikipedia
import platform
import pyaudio
import pyjokes
import pyowm
import webbrowser


engine = pyttsx3.init('dummy','sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def wishMe():
    '''This function will greet end user and introduce itself when called.'''

    hour = int(datetime.datetime.now().hour) # Will fetch time from datetime module.

    if hour>= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello, I am Max! How Should I call you?")
    name = (input("Enter Your name:  "))
    speak(f'Hello {name} How can i help you today?')

def takeCommand():
    '''It takes microphone input from the user and returns string output.'''

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try: 
        print("Recogninzing...")
        query = r.recognize_google(audio, language = 'en-us')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e) # Will print exception/error.
        print("Say that again please...")
        return "None"
    return query

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
    os.system("gnome-open " + app_name)

def open_app(app_name):
    system = platform.system().lower()

    if system == "windows":
        os.startfile(app_name)
    elif system == "darwin":  # macOS
        os.system("open -a " + app_name)
    elif system == "linux":
        os.system("xdg-open " + app_name)

def get_weather():
    owm = pyowm.OWM('your_openweathermap_api_key')
    observation = owm.weather_at_place('City, Country')  # Replace 'City, Country' with your desired location
    weather = observation.get_weather()
    temperature = weather.get_temperature('celsius')['temp']
    status = weather.get_status()
    return f"The weather in City is {status.lower()} with a temperature of {temperature}°C."

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

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        
        if "hello" in query:
            speak("How can I help you?")
        elif "what can you do" in query:
            qualities = "I can do all your tasks, open apps for you, and provide information from Wikipedia."
            speak(qualities)
        elif "search wikipedia" in query:
            speak("What do you want to search on Wikipedia?")
            search_query = takeCommand()
            search_wikipedia(search_query)
        elif "open" in query:
            app_name = query.split("open ")[-1]
            open_app(app_name)
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
        elif "weather" in query:
            weather_info = get_weather()
            speak(weather_info)
        elif "date" in query:
            date_info = get_date()
            speak(date_info)
        elif "random fact" in query:
            fact = get_random_fact()
            speak(fact)
        elif "open website" in query:
            speak("Sure, which website would you like to open?")
            website = takeCommand()
            webbrowser.open(f"https://{website}")
        elif "quit" in query or "exit" in query:
            speak("Goodbye!")
