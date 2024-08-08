
import nltk

intent = [
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
intents = {
    "check_weather": ["weather", "forecast"],
    "set_reminder": ["remind", "reminder"],
    "play_music": ["song", "music"],
    "send_message" : ["whatsapp","message","send"],
    "read_news" : ["news"],
    "make_call" : ["call" , "phone"],
    "Search_query" : ["what","when","why","is"],
    
    }

def preprocess(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return tokens

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

user_input = input("enter :")
user_input_tokens = preprocess(user_input)

max_similarity = 0
best_response = "none"
for pattern, response in intents:
    pattern_tokens = preprocess(pattern)
    similarity = jaccard_similarity(set(user_input_tokens), set(pattern_tokens))
    if similarity > max_similarity:
        max_similarity = similarity
        best_response = response
print(best_response)
        
