
import Intent_Reg
import read_convo


import sys
import nltk
import pyautogui
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import requests
import pyaudio
from bs4 import BeautifulSoup
import urllib.parse
import time
import pywhatkit
import re

recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def take_command():
    with sr.Microphone() as source: 
        print("Listening...")
        recognizer.pause_threshold=1
        recognizer.adjust_for_ambient_noise(source,duration=1)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        speak("")
        query = "None"
    return query.lower()

def preprocess(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return tokens

def search_google(query, retries=3, delay=5):
    query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            snippet = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
            if snippet:
                return snippet.get_text()
            else:
                return "No snippet found."
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise
    return "Failed to retrieve data after multiple attempts"

def make_function(response,user_input):
    user_input_tokens = preprocess(user_input)
    if "check_weather" in response:
        print("weather")
    elif "set_reminder" in response:
        print("remainder")
    elif "play_music" in response:
        if "local" in user_input_tokens:
            print("local music")
        elif "play" in user_input_tokens:
            user_input=user_input.replace('play','') 
            user_input= user_input.replace('denver','')
            pywhatkit.playonyt(user_input)
            return "playing "+user_input
    elif "send_message" in response:
        pattern = r"\bsend\s+(a\s+(whatsapp\s+)?)?message\s+to\s+([A-Z][a-z]*)"
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            name = match.group(3)
            print(name)
    elif "search_query" in response:
        answer = search_google(user_input + " in one line")
        return(answer)
    
while True:
    # user_input = input("enter: ")
    user_input = take_command()
    # Assume read_convo.main() generates the actual intent
    response = read_convo.main(user_input)
    
    if response == "none":
        # Take a convo from JSON file using read_convo.py code
        response = Intent_Reg.intent_reg(user_input)
        print("intent: " + response)
        # Make sure `make_function` is defined and can handle the intent
        func_call = make_function(response, user_input)
        if response != "none":
            print(func_call)
            speak(func_call)
        else:
            print("iam not trained yet")
            speak("i'am not trained yet")
    else:
        # Print the response if it's not "none"
        print(response)
        speak(response)