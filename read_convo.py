import json
from fuzzywuzzy import fuzz, process

# Load conversation data from the JSON file
def load_conversations(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Function to find the best matching response based on similarity score
def get_best_response(query, conversations, threshold=70):
    # Extract input texts from conversations
    inputs = [convo['input'] for convo in conversations]
    
    # Find the best match using fuzzywuzzy's process module
    best_match, score = process.extractOne(query, inputs, scorer=fuzz.token_sort_ratio)
    
    # If the score meets the threshold, return the corresponding response
    if score >= threshold:
        # Find the index of the best match
        index = inputs.index(best_match)
        return conversations[index]['response']
    else:
        return "none"

# Main function to interact with the user
def main(user_input):
    # Path to your conversation JSON file
    convo_file_path = 'general_convo.json'
    
    # Load conversations
    conversations = load_conversations(convo_file_path)
        
    # Get the best response from loaded conversations
    response = get_best_response(user_input, conversations)
        
        # Print the response
    # print(f"Denver: {response}")
    return response

# if __name__ == "__main__":
#     while True:
#         user_input = input("You: ")
#         main(user_input)
