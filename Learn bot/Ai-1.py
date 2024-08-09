import sqlite3
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

# Database setup
conn = sqlite3.connect('conversation_history.db')
c = conn.cursor()

# Create a table to store conversations
c.execute('''CREATE TABLE IF NOT EXISTS conversations
             (id INTEGER PRIMARY KEY, user_input TEXT, ai_response TEXT, intent TEXT)''')
conn.commit()

# Define the intents and corresponding keywords
intents = {
    "check_weather": ["weather", "forecast"],
    "set_reminder": ["remind", "reminder"],
    "play_music": ["song", "music"],
    "send_message": ["whatsapp", "message", "send"],
    "read_news": ["news"],
    "make_call": ["call", "phone"],
    "search_query": ["who", "what", "when", "where", "why", "how", "is", "are", "was", "were"],
}

# Function to classify intent based on keywords
def classify_intent(text):
    for intent, keywords in intents.items():
        if any(keyword in text.lower() for keyword in keywords):
            return intent
    return "unknown"

# Function to store a conversation in the database
def store_conversation(user_input, ai_response, intent):
    c.execute("INSERT INTO conversations (user_input, ai_response, intent) VALUES (?, ?, ?)", 
              (user_input, ai_response, intent))
    conn.commit()

# Function to print the first 25 words or two lines of a text
def print_limited_output(text, max_words=25, max_lines=2):
    words = text.split()
    lines = text.splitlines()

    if len(words) <= max_words:
        limited_output = ' '.join(words[:max_words])
    else:
        limited_output = ' '.join(words[:max_words])

    if len(lines) <= max_lines:
        limited_output = '\n'.join(lines[:max_lines])
    else:
        limited_output = '\n'.join(lines[:max_lines])

    return limited_output

# Function to search Google and retrieve a snippet
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
                snippet_text = snippet.get_text()
                limited_snippet = print_limited_output(snippet_text)
                return limited_snippet
            else:
                return "No snippet found."
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise
    return "Failed to retrieve data after multiple attempts"

# Function to learn from user feedback
def learn_from_feedback(user_feedback, user_input, ai_response, intent):
    if user_feedback.lower() == 'yes':
        # Store this as a successful interaction
        store_conversation(user_input, ai_response, intent)
        print("Great! I've stored this information.")
    else:
        print("Thanks for the feedback! I won't store this conversation.")

# Function to retrieve past responses from the database
def retrieve_past_responses(user_input):
    c.execute("SELECT ai_response FROM conversations WHERE user_input LIKE ?", ('%' + user_input + '%',))
    past_responses = c.fetchall()
    return past_responses

# Main function
def main():
    user_id = 1  # Unique identifier for each user
    user_context = {}

    def update_context(conversation):
        if user_id not in user_context:
            user_context[user_id] = []
        user_context[user_id].append(conversation)

    print("Hello! I'm your assistant. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        intent = classify_intent(user_input)
        
        past_responses = retrieve_past_responses(user_input)
        if past_responses:
            ai_response = past_responses[0][0]
        else:
            if intent == "search_query":
                ai_response = search_google(user_input)
            else:
                ai_response = f"I'm not sure how to respond to that, but I'll learn!"

        print(f"Assistant: {ai_response}")
        
        # Update context with the current conversation
        update_context(user_input)

        # Ask for feedback and learn from it
        feedback = input("Was this response helpful? (yes/no): ")
        learn_from_feedback(feedback, user_input, ai_response, intent)

if __name__ == "__main__":
    main()
