
import Intent_Reg


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


convo_general = [
    ("hello javis", "ima not javis"),
    ("javis", "Iam not jarvis"),
    ("hey Denver", ",Yes sir"),
    ("Hello", "Hello sir!"),
    ("How are you?", "Iam fine sir ! "),
    ("What's your name?", "iam is Denver."),
    ("what's going on", "Nothing much, sir."),
    ("help me?", "Of course! What do you need help with sir?"),
    ("Do you like music?", "I don't have preferences, but I can find music recommendations for you!"),
    ("Goodbye", "Goodbye! Have a great day! sir"),
    ("Thanks", "You're welcome! sir"),
    ("Thank you", "No problem! Happy to help."),
    ("what are you doing", "Iam just listning for you sir"),
    ("javis", "Iam not jarvis, iam denver, developed by kalaiyarasan"),
    ("vignesh", "Hello mister vignesh")
]
def preprocess(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return tokens

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def intent_req(user_input,convo1):
    user_input_tokens = preprocess(user_input)
    conversation = convo1
    max_similarity = 0
    best_response = "none"
    for pattern, response in conversation:
        pattern_tokens = preprocess(pattern)
        similarity = jaccard_similarity(set(user_input_tokens), set(pattern_tokens))
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = response
    return(best_response)


def make_function(response,user_input_tokens,user_input):
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
            return "playing"+user_input
    elif "send_message" in response:
        pattern = r"\bsend\s+(a\s+(whatsapp\s+)?)?message\s+to\s+([A-Z][a-z]*)"
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            name = match.group(3)
            print(name)
    
                        
        
while True:
    user_input = input("enter :")
    response = Intent_Reg.intent_reg(user_input)
    user_input_tokens = preprocess(user_input)
    print("intent: "+response)
    
    if "none" in response:
        response = intent_req(user_input,convo_general)
        print(response)
    else:
        make_function(response,user_input_tokens,user_input)