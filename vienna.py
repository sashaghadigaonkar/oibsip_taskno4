import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import requests


def initialize_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 1 for female voice, 0 for male voice
    engine.setProperty('rate', 180)
    return engine

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        log_to_gui("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        log_to_gui("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
        log_to_gui(f"You said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        log_to_gui("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        log_to_gui("Sorry, my speech service is down.")
        return None
    return query

def tell_time(engine):
    now = datetime.datetime.now().strftime("%I:%M %p")
    print(now)
    log_to_gui(f"The current time is {now}")
    speak(engine, f"The current time is {now}")

def tell_date(engine):
    today = datetime.datetime.now().strftime("%B %d, %Y")
    print(today)
    log_to_gui(f"Today's date is {today}")
    speak(engine, f"Today's date is {today}")

def open_browser(engine, url):
    webbrowser.open(url)
    print("Opening " + url)
    log_to_gui(f"Opening {url}")
    speak(engine, f"Opening {url}")

def search_wikipedia(engine, query):
    result = wikipedia.summary(query, sentences=2)
    print(result)
    log_to_gui("According to wikipedia" + result)
    speak(engine, f"According to Wikipedia, {result}")

def get_weather(engine, city):
    api_key = "3e3478877717792204f0cfcd5fe207aa"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = "https://api.openweathermap.org/data/2.5/weather?q=mumbai&appid=3e3478877717792204f0cfcd5fe207aa"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        temperature_kelvin = main["temp"]
        temperature_celsius = temperature_kelvin - 273.15
        humidity = main["humidity"]
        weather_desc = data["weather"][0]["description"]
        print(f"Temperature in {city} is {temperature_celsius:.2f} degrees Celsius. Humidity is {humidity} percent. Weather is {weather_desc}.")
        log_to_gui(f"Temperature in {city} is {temperature_celsius:.2f} degrees Celsius. Humidity is {humidity} percent. Weather is {weather_desc}.")
        speak(engine, f"Temperature in {city} is {temperature_celsius:.2f} degrees Celsius. Humidity is {humidity} percent. Weather is {weather_desc}.")
    else:
        print("City Not Found.")
        log_to_gui("City Not Found.")
        speak(engine, "City Not Found.")

def run_assistant():
    engine = initialize_engine()
    speak(engine, "Hello, I am Vienna. How can I assist you today?")
    log_to_gui("Hello, I am Vienna. How can I assist you today?")
    print("Hello, I am Vienna. How can I assist you today?")
    
    while True:
        query = listen()
        if query is None:
            continue
        query = query.lower()
        
        if "hello" in query:
            speak(engine, "Hello! How are you?")
            log_to_gui("Hello! How are you?")
            print("Hello! How are you?")
            
        elif "how are you" in query:
            speak(engine, "I am good, just here to help you!")
            log_to_gui("I am good, just here to help you!")
            
        elif "time" in query:
            tell_time(engine)
            
        elif "date" in query:
            tell_date(engine)
            
        elif "open" in query:
            speak(engine, "Which website would you like to open?")
            log_to_gui("Which website would you like to open?")
            website = listen().lower()
            if website:
                open_browser(engine, f"https://{website}")
                
        elif "wikipedia" in query:
            speak(engine, "What would you like to know about?")
            log_to_gui("What would you like to know about?")
            topic = listen().lower()
            if topic:
                search_wikipedia(engine, topic)
        
        elif "weather" in query:
            speak(engine, "Which city's weather would you like to know?")
            log_to_gui("Which city's weather would you like to know?")
            city = listen().lower()
            if city:
                get_weather(engine, city)
                
        elif "exit" in query or "bye" in query:
            confirm_exit = messagebox.askyesno("Exit Voice Assistant", "Are you sure you want to exit?")
            if confirm_exit:
                speak(engine, "Goodbye! See you soon.")
                log_to_gui("Goodbye! See you soon.")
                print("Goodbye! See you soon.")
                break
            else:
                speak(engine, "Cancelled exit. How can I assist you further?")
                log_to_gui("Cancelled exit. How can I assist you further?")
        
        else:
            speak(engine, "I am sorry, I didn't catch that. Can you please repeat?")
            log_to_gui("I am sorry, I didn't catch that. Can you please repeat?")
            print("I am sorry, I didn't catch that. Can you please repeat?")

def log_to_gui(message):
    terminal_output.insert(tk.END, message + "\n")
    terminal_output.see(tk.END)


def start_assistant():
    threading.Thread(target=run_assistant).start()

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("1000x600")
root.configure(bg="#F8F3EE")


terminal_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#ffffff", fg="#333333", font=("Poppins", 12))
terminal_output.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)


start_button = tk.Button(root, text="Start Assistant", bg="#F8C144", fg="#62483F", font=("Poppins", 14), command=start_assistant)
start_button.pack(pady=30)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
