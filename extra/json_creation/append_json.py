import json

# New conversations to add
new_conversations = [
    {"input": "tell me a joke", "response": "Why don’t scientists trust atoms? Because they make up everything!"},
    {"input": "do you know any jokes?", "response": "Sure! Why did the scarecrow win an award? Because he was outstanding in his field!"},
    {"input": "make me laugh", "response": "Why don’t skeletons fight each other? They don’t have the guts!"},
    {"input": "what's the funniest thing you know?", "response": "I told my computer I needed a break, and now it won't stop sending me Kit-Kats!"},
    {"input": "tell me a funny story", "response": "Once, a snail decided to buy a fast sports car. When he sped around town, he had 'S' painted on the car so everyone would say, 'Look at that S-car-go!'"},
    {"input": "tell me a pun", "response": "I’d tell you a chemistry joke, but I know I wouldn’t get a reaction."},
    {"input": "what's your favorite joke?", "response": "I’m reading a book on anti-gravity. It’s impossible to put down!"},
    {"input": "say something funny", "response": "Why did the math book look sad? It had too many problems."},
    {"input": "make a pun", "response": "I used to be a baker, but I couldn’t make enough dough."},
    {"input": "what's the best joke you know?", "response": "Why did the bicycle fall over? It was two-tired!"}
]

# Function to append new conversations to the existing JSON file
def append_conversations(file_path, new_data):
    # Load existing data
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    # Append new conversations
    existing_data.extend(new_data)
    
    # Write updated data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    print("Conversations appended to", file_path)

# Path to your conversation JSON file
convo_file_path = 'denver_conversations.json'

# Append new conversations
append_conversations(convo_file_path, new_conversations)
