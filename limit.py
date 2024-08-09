import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def print_limited_output(text, max_words=5, max_lines=1):
    # Split the text into words and lines
    words = text.split()
    lines = text.splitlines()

    # If the number of words is less than or equal to max_words
    if len(words) <= max_words:
        limited_output = ' '.join(words[:max_words])
    else:
        # Get the first max_words words
        limited_output = ' '.join(words[:max_words])

    # If the number of lines is less than or equal to max_lines
    if len(lines) <= max_lines:
        limited_output = '\n'.join(lines[:max_lines])
    else:
        # Get the first max_lines lines
        limited_output = '\n'.join(lines[:max_lines])

    return limited_output

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
                # Get the raw snippet text
                snippet_text = snippet.get_text()
                # Print the limited output (first 25 words or 2 lines)
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

def main():
    print("Hello! I'm your assistant. How can I help you today?")
    while True:
        user_input = input("Enter Query: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        # Call the search_google function
        result = search_google(user_input)
        print(f"Answer: {result}")

if __name__ == "__main__":
    main()
