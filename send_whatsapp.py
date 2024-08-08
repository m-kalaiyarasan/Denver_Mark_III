import webbrowser

kalai = "7339614080"
kishore = "8610846045"
kamalesh = "9342045912"

def nam(var_name):
    try:
        return globals()[var_name]
    except KeyError:
        return "Variable not found"

def send_whatsapp_message(phone_number, message):
    # Create the URL for WhatsApp Web with the pre-filled message
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    
    # Open the URL in the default web browser
    webbrowser.open(url)

def data(name, message):
    varname = name
    phone_number = "+91" + nam(varname)
    print(phone_number)

    if "bot" in message:
        message = f"Dear {varname.capitalize()}, I am DENVER👾 Kalaiyarasan's Virtual Assistant. He is busy right now, and he will ping you later. Thank you."
    else:
        message = message

    send_whatsapp_message(phone_number, message)

# Example usage:
# data("kalai", "Hello")
