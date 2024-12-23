# Define the intents and corresponding keywords
intents = {
    "check_weather" : ["weather ","climate "],
    "search_query" : ["what ", "when ", "why ", "is ", " mean "," meant ", "who ","tell ","about","does"],
    "set_reminder" : ["remind ", "reminder"],
    "play_music" : ["song", "play"],
    "send_message" : [" whatsapp ", " message ", "send "],
    "read_news" : [" news "],
    "make_call" : ["call ", "phone "],
    "get_time" : ["time"," clock "," is "," now"],
    "open_request" : ["open","show"],
    "thank_msg" : ["thank you","thankyou"],
    "face_rec" : [" scan "," face "],
    "type_key" : ["type ","take a note ","note"],
    "window_fun" : ["close","window","open"],
    "control_mode" : ["control mode","mode","windows",]
}


# Example usage
# text_output = """This is an example output. It contains more than twenty-five words, 
# and we want to make sure that only the first twenty-five words or the first two lines 
# are printed. This way, we can control the amount of text that is displayed to the user, 
# which is useful in scenarios where the text might be too long to display in its entirety."""

# print_limited_output(text_output)


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
        intent = classify_intent(user_input)
        return(intent)

# if __name__ == "__main__":
#     print("Hello! I'm your assistant. How can I help you today?")
#     while True:
#         user_input = input("You:  ")
#         print(intent_reg(user_input))
