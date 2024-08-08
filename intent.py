
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

def preprocess(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return tokens

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
    
                        
        
# while True:
#     user_input = input("enter :")
#     # ithu will generate actual intents 
#     response = read_convo.main(user_input)
#     if "none" in response:
#         # Take a convo from json file using read_convo.py code
#         response = Intent_Reg.intent_reg(user_input)
#         print("intent: " + response)
#         make_function(response,user_input) 
#     else:
#         # Likely to call the intent based functions
#         print(response)
#     print(response)
while True:
    user_input = input("enter: ")
    
    # Assume read_convo.main() generates the actual intent
    response = read_convo.main(user_input)
    
    if response == "none":
        # Take a convo from JSON file using read_convo.py code
        response = Intent_Reg.intent_reg(user_input)
        print("intent: " + response)
        # Make sure `make_function` is defined and can handle the intent
        func_call = make_function(response, user_input)
        print(func_call)
    else:
        # Print the response if it's not "none"
        print(response)
    # Print response after handling the intent if applicable
