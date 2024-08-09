
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
import subprocess
import pywhatkit
import pyautogui
import send_whatsapp

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
        query = "none"
    return query.lower()

def preprocess(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return tokens

# def search_google(query, retries=3, delay=5):
#     query = urllib.parse.quote_plus(query)
#     url = f"https://www.google.com/search?q={query}"
#     headers = {"User-Agent": "Mozilla/5.0"}

#     for attempt in range(retries):
#         try:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
#             snippet = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
#             if snippet:
#                 return snippet.get_text()
#             else:
#                 return "No snippet found."
#         except requests.exceptions.HTTPError as e:
#             if e.response.status_code == 429:
#                 print(f"Rate limit exceeded. Retrying in {delay} seconds...")
#                 time.sleep(delay)
#             else:
#                 raise
#     return "Failed to retrieve data after multiple attempts"

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
                print(f"Rate limit exceeded. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                raise
    return "Failed to retrieve data after multiple attempts"


def get_weather(city):
    base_url = f"http://wttr.in/{city}?format=%C+%t"  # Adjust format to exclude emoji
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.text + " sir"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return "I couldn't retrieve the weather information right now. Please try again later."

def make_function(response,user_input):
    user_input_tokens = preprocess(user_input)
    if "check_weather" in response:
        city = None
        if "in" in user_input_tokens:
            in_index = user_input_tokens.index("in")
            if in_index + 1 < len(user_input_tokens):
                city = user_input_tokens[in_index + 1]
        if not city:
            for token in user_input_tokens:
                if token not in ["weather", "in"]:
                    city = token
                    break
        if city:
            return get_weather(city)
        else:
            return "I couldn't determine the city. Please specify the city name."
    elif "set_reminder" in response:
        return("remainder")
    elif "play_music" in response:
        if "local" in user_input_tokens:
            return("local music")
        elif "play" in user_input_tokens:
            user_input=user_input.replace('play','') 
            user_input= user_input.replace('denver','')
            pywhatkit.playonyt(user_input)
            return "playing "+user_input
        
        
    elif "send_message" in response or "make_call" in response:
        if "send_message" in response:
            pattern = r"\bsend\s+(a\s+(whatsapp\s+)?)?message\s+to\s+([A-Z][a-z]*)"
        if "make_call" in response:
            pattern = r"\bcall\b\s+(to\s+)?([A-Z][a-z]*)"
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            if "send_message" in response:
                name = match.group(3)
                print(name)
            else:
                name = match.group(2)
                print(name)
            if "make_call" in response:
                message = "make_call"
            else:
                print("message ?")
                speak("message ?")
                # message = take_command()
                message = input("message :")
            send_whatsapp.data(name,message)
        else:
            print("test ")
            print("Name ?")
            speak("Name")
            name = take_command()
            print("message ?")
            speak("message ?")
            message = take_command()
            send_whatsapp.data(name,message)
        return "none"
    elif "search_query" in response:
        answer = search_google(user_input + " in one line")
        return(answer)
    elif "open_request" in response:
        if 'youtube' in user_input_tokens:
            webbrowser.open("https://www.youtube.com")
            return "sure sir, Opening YouTube"
        elif 'google' in user_input_tokens:
            webbrowser.open("https://www.google.com")
            return "Sure sir, opening google"
        elif 'inbox' in user_input_tokens:
            webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
            return "sure sir, Opening mail inbox"
        elif 'whatsapp' in user_input_tokens:
            webbrowser.open("https://web.whatsapp.com/")
            return "sure sir, Opening whatsapp"
        elif 'notepad' in user_input_tokens:
            subprocess.run(['notepad.exe'])
            return "sure sir, Opening notepad"
    elif "type_key" in response:
        if "notepad" in user_input_tokens:
            subprocess.run(['notepad.exe'])
            time.sleep(3)
        if "type" in  user_input_tokens:
            # match = re.search(r'type\s+(.+)', user_input, re.IGNORECASE)
            # text_to_type = match.group(1)
            # pyautogui.write(text_to_type)
            user_input=user_input.replace('type','')
            speak(".writting sir")
            pyautogui.write(user_input)
            return "none"
    elif "control_mode" in response:
        print("control mode activated sir")
        speak("control mode activated sir")
        while True:
            # user_input = input("control: ")
            print("in control mode")
            user_input = take_command()
            user_input_tokens = preprocess(user_input)
            if "exit" in user_input_tokens or "normal" in user_input_tokens:
                return "sure sir"
            elif "type" in user_input_tokens:
                user_input=user_input.replace('type','')
                speak(".writting sir")
                pyautogui.write(user_input)
            elif "search" in user_input_tokens or "navigate" in user_input_tokens:
                pyautogui.press('enter')
            elif "close" in user_input_tokens:
                if "close window" in user_input_tokens:
                    pyautogui.hotkey('alt','f4')  
                pyautogui.hotkey('ctrl','w')    
            elif "open" in user_input_tokens:
                make_function("open_request",user_input)
    elif "window_fun" in response:
        if "send" in user_input_tokens:
            pyautogui.press('enter')
    elif "get_time" in response:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}, sir "
        
                  
        
    
    
    
    return "none"
    
while True:
    user_input = input("enter: ")
    # user_input = take_command()
    # Assume read_convo.main() generates the actual intent
    response = read_convo.main(user_input)
    
    if response == "none" or response == "None":
        # Take a convo from JSON file using read_convo.py code
        response = Intent_Reg.intent_reg(user_input)
        print("intent: " + response)
        # Make sure `make_function` is defined and can handle the intent
        func_call = make_function(response, user_input)
        if func_call != "none" :
            print(func_call)
            speak(func_call)
        # else:
        #     print("iam not trained yet")
        #     speak("i'am not trained yet")
    else:
        # Print the response if it's not "none"
        print(response)
        speak(response)