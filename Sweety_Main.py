import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import requests
from geopy.geocoders import Nominatim
import webbrowser
import random

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

GNEWS_API_KEY = '245540c1449882c320f890470822129b'
GNEWS_URL = "https://gnews.io/api/v4/top-headlines"


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=2)
            print('Listening...')
            talk('Listening...')
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice, language="en-US")
            print(f"Command in English: {command}")
            return command.lower()
    except sr.WaitTimeoutError:
        print("Listening timed out. No speech detected.")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return ""


def fetch_news():
    params = {
        'token': GNEWS_API_KEY,
        'lang': 'en',
    }
    response = requests.get(GNEWS_URL, params=params)
    news_data = response.json()

    if 'articles' in news_data:
        headlines = [article['title'] for article in news_data['articles'][:5]]
        return "\n".join(headlines)
    else:
        return "Sorry, I couldn't fetch the news right now."


def verify_sweety():
    talk("Say 'Sweety'  or ' Siri' to activate me.")
    while True:
        command = take_command()
        if 'sweety' in command or 'sweetie' in command or 'siri' in command:
            talk("Hello, I'm Sweety! How can I assist you today?")
            return True
        else:
            talk("Please say 'Sweety' to activate me.")


def run_sweety():
    command = take_command()
    if not command:
        talk("I didn't catch that. Please try again.")
        return

    if 'hi' in command or 'hello' in command:
        talk("Hi there! How can I assist you today?")
    elif "how is your day" in command or "how are you" in command:
        talk("I'm having a great day! Thanks for asking. How about you?")

    elif 'play' in command and 'song' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time}")
        print(time)

    elif 'date' in command:
        date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        talk(f"Today's date is {date}")
        print(date)

    elif 'weather' in command:
        talk("Which city's weather do you want to know?")
        city = take_command()
        api_key = "ccd8a0cf161c2dbafaaf2e6f4f14f985"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                weather = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                print(f"Weather in {city}: {weather}, Temperature: {temperature}°C")
                talk(f"The weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
            else:
                talk("Sorry, I couldn't fetch the weather details.")
        except Exception as e:
            talk("There was an error fetching the weather information.")
            print(f"Error: {e}")

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'news' in command:
        headlines = fetch_news()
        talk(headlines)

    elif 'find' in command and 'place' in command:
        talk("What type of place are you looking for?")
        place_type = take_command()
        geolocator = Nominatim(user_agent="assistant")

        talk("Please tell me the city where I should search.")
        city = take_command()

        try:
            location = geolocator.geocode(city)
            if location:
                talk(f"Searching for {place_type} near {location.address}")
                print(f"Searching for {place_type} near {location.address}")
                webbrowser.open(
                    f"https://www.google.com/maps/search/{place_type}+near+{location.latitude},{location.longitude}")
            else:
                talk("Sorry, I couldn't find the location you provided.")
                print("Location not found.")
        except Exception as e:
            talk("There was an error finding the location.")
            print(f"Error: {e}")

    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        talk(f"Searching for {person}")

        # GNews API parameters
        gnews_url = "https://gnews.io/api/v4/search"
        params = {
            'q': person,
            'token': GNEWS_API_KEY,
            'lang': 'en',
            'max': 3,
        }

        try:
            response = requests.get(gnews_url, params=params)
            data = response.json()
            if 'articles' in data and data['articles']:
                talk(f"Here are some news headlines about {person}:")
                for article in data['articles']:
                    talk(article['title'])
                    print(f"Title: {article['title']}\nURL: {article['url']}\n")
            else:
                talk(f"Sorry, I couldn't find any recent news about {person}.")
        except Exception as e:
            talk("There was an error fetching the information.")
            print(f"Error: {e}")

    elif 'fitness ' in command or 'workout' in command:
            fitness_tips = [
                "Drink plenty of water and stay hydrated.",
                "Do 30 minutes of cardio every day.",
                "Try doing 15 push-ups and 20 squats every morning.",
                "Stretch before and after your workout to avoid injury.",
                "Get at least 7 hours of sleep to recover well.",
                "Incorporate healthy fats, protein, and fiber into your diet."
            ]
            talk(fitness_tips[random.randint(0, len(fitness_tips) - 1)])

    elif 'diet' in command:
            diet_tips = [
                "Try to eat balanced meals with proteins, carbs, and fats.",
                "Avoid sugary drinks and snacks.",
                "Eat more vegetables and fruits.",
                "Keep track of your calories if you're aiming for weight loss.",
                "Include lean proteins like chicken and fish in your diet."
            ]
            talk(f"Diet tip: {diet_tips[random.randint(0, len(diet_tips) - 1)]}")

    elif 'stop' in command or 'exit' in command:
            talk("Thank you! Have a nice day!")
            exit()


try:
    talk("Hi, I'm Sweety, your assistant! Say 'Sweety' to activate me.")
    if verify_sweety():
        while True:
            run_sweety()
except KeyboardInterrupt:
    print("Program terminated by user.")
