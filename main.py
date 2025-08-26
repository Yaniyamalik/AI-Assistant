import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary
import requests
import time
import google.generativeai as genai
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = ""


API_KEY = ""
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(command):
    """Send command to Gemini API and return response"""
    try:
        response = model.generate_content(command)

        return response.text 
    except Exception as e:
        return f"Error: {e}"
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def speak_old(text):
    """Speak the given text"""
    engine.say(text)
    engine.runAndWait()

def processcommand(command):
    cmd = command.lower()
    if "open google" in cmd:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in cmd:
        webbrowser.open("https://www.linkedin.com")
    elif "open instagram" in cmd:
        webbrowser.open("https://www.instagram.com")
    elif cmd.startswith("play"):
        song = cmd.split(" ")[1]
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I don't have that song in my library.")
    elif "news" in cmd:
        r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2025-07-09&sortBy=publishedAt&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if articles:
                speak("Here are the top news headlines")
                for article in articles[:5]:
                    speak(article["title"])
                    print(article["title"])
            else:
                speak("Sorry, no news found.")
        else:
            print(f"Error fetching news: {r.status_code} - {r.text}")
            speak("Sorry, I couldn't fetch the news.")
    else:
        
        ai_reply = ask_gemini(command)
        print("\nGemini:", ai_reply)
        speak(ai_reply)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")

                if command.lower() == "jarvis":
                    speak("Yes, how can I assist you?")
                    time.sleep(0.5)
                    with sr.Microphone() as source:
                        print("Jarvis Active, listening for command...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        print(f"Command received: {command}")
                        processcommand(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except Exception as e:
            print(f"Error: {e}")
