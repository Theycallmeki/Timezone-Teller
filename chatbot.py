import os
import requests
from dotenv import load_dotenv

# Load .env file for any environment variables
load_dotenv()

# Retrieve the API key from the .env file
API_KEY = os.getenv("TIMEZONEDB_API_KEY")

# Debugging step to ensure the API key is being loaded correctly
print("Loaded API Key:", API_KEY)  # This should print the API key to verify it's loaded

def get_time_in_country(country):
    try:
        # Normalize the country name to lowercase
        country = country.lower().strip()

        # TimeZoneDB API needs a city or country, so we map country to a city
        country_map = {
            "japan": "Asia/Tokyo",
            "usa": "America/New_York",
            "uk": "Europe/London",
            "india": "Asia/Kolkata",
            "canada": "America/Toronto",
            "australia": "Australia/Sydney",
            "france": "Europe/Paris",
            "germany": "Europe/Berlin",
            "brazil": "America/Sao_Paulo",
            "south africa": "Africa/Johannesburg",
            "china": "Asia/Shanghai",
            "russia": "Europe/Moscow",
            "mexico": "America/Mexico_City",
            "italy": "Europe/Rome",
            "spain": "Europe/Madrid",
            "netherlands": "Europe/Amsterdam",
            "sweden": "Europe/Stockholm",
            "argentina": "America/Argentina/Buenos_Aires",
            "india": "Asia/Kolkata",
            "new zealand": "Pacific/Auckland",
            "singapore": "Asia/Singapore",
            "south korea": "Asia/Seoul",
            "switzerland": "Europe/Zurich",
            "philippines": "Asia/Manila"
        
        }

        print(f"Looking up time for: {country}")
        
        if country not in country_map:
            return f"Sorry, I don't have time data for {country}."

        # Get the timezone for the country
        timezone = country_map[country]
        
        # TimeZoneDB API request URL
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone={timezone}"
        print(f"Making API request to: {url}")

        # Make the API request
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                current_time = data["formatted"]
                return f"The current time in {country.title()} is {current_time}."
            else:
                return f"Error fetching time for {country.title()}. Message: {data.get('message', 'Unknown error')}"
        else:
            return f"Error fetching time for {country.title()}. Status code: {response.status_code}"

    except Exception as e:
        return f"Error fetching time: {str(e)}"

def generate_response(user_input):
    responses = {
        "hello": "Hi! How can I assist you today?",
        "how are you": "I'm doing great, thank you! How about you?",
        "bye": "Goodbye! Have a great day!",
    }
    for key in responses:
        if key in user_input.lower():
            return responses[key]
    return "I'm not sure how to respond to that. Can you try again?"

def chat_with_ai():
    print("AI Chatbot: Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # Get time response based on country
        time_response = get_time_in_country(user_input)
        print(f"Time response: {time_response}")

        if "current time" in time_response:
            print(f"Chatbot: {time_response}")
        else:
            chatbot_response = generate_response(user_input)
            print("Chatbot:", chatbot_response)

if __name__ == "__main__":
    chat_with_ai()
