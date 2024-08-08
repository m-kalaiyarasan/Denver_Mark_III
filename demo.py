import re

user_input = "send a message to kishore."
pattern = r"\bsend\s+(a\s+(whatsapp\s+)?)?message\s+to\s+([A-Z][a-z]*)"

match = re.search(pattern, user_input, re.IGNORECASE)
if match:
    name = match.group(3)
    print(name)