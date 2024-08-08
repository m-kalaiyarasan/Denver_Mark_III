# Define the intents and corresponding keywords
intents = {
    "check_weather" : ["weather ","climate "],
    "set_reminder" : ["remind ", "reminder"],
    "play_music" : ["song", "play"],
    "send_message" : [" whatsapp ", " message ", " send "],
    "read_news" : [" news "],
    "make_call" : ["call ", "phone "],
    "get_time" : ["time"," clock "," is "," now"],
    "search_query" : ["what ", "when ", "why ", " is ", " mean "," meant ", "who "],
    "open_request" : ["open","show"],
    "thank_msg" : ["thank you","thankyou"],
    "face_rec" : [" scan "," face "],
    "type_key" : ["type ","take a note ","note"],
    "window_fun" : ["close","window","open",],
    "greet_msg" : ["hello","denver","hey","hai",],
    "" : [] 
}

def classify_intent(text):
    text_lower = text.lower()
    intent_scores = {intent: 0 for intent in intents} 
    
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text_lower:
                intent_scores[intent] += 1
    
    best_intent = max(intent_scores, key=intent_scores.get)
    if intent_scores[best_intent] == 0:
        return "none"
    return best_intent

def intent_reg(user_input):
    while True:
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Assistant: Goodbye!")
            break
        intent = classify_intent(user_input)
        return(intent)

# if __name__ == "__main__":
#     print("Hello! I'm your assistant. How can I help you today?")
#     while True:
#         user_input = input("You:  ")
#         print(intent_reg(user_input))