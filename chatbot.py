import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from rapidfuzz import process

load_dotenv()

API_KEY = os.getenv("TIMEZONEDB_API_KEY")

app = Flask(__name__)

# Country-to-timezone mapping
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
    "new zealand": "Pacific/Auckland",
    "singapore": "Asia/Singapore",
    "south korea": "Asia/Seoul",
    "switzerland": "Europe/Zurich",
    "philippines": "Asia/Manila",
    "norway": "Europe/Oslo",
    "denmark": "Europe/Copenhagen",
    "finland": "Europe/Helsinki",
    "portugal": "Europe/Lisbon",
    "belgium": "Europe/Brussels",
    "austria": "Europe/Vienna",
    "ireland": "Europe/Dublin",
    "greece": "Europe/Athens",
    "turkey": "Europe/Istanbul",
    "poland": "Europe/Warsaw",
    "hungary": "Europe/Budapest",
    "czech republic": "Europe/Prague",
    "slovakia": "Europe/Bratislava",
    "romania": "Europe/Bucharest",
    "bulgaria": "Europe/Sofia",
    "serbia": "Europe/Belgrade",
    "croatia": "Europe/Zagreb",
    "slovenia": "Europe/Ljubljana",
    "ukraine": "Europe/Kyiv",
    "belarus": "Europe/Minsk",
    "latvia": "Europe/Riga",
    "lithuania": "Europe/Vilnius",
    "estonia": "Europe/Tallinn",
    "iceland": "Atlantic/Reykjavik",
    "greenland": "America/Godthab",
    "chile": "America/Santiago",
    "peru": "America/Lima",
    "venezuela": "America/Caracas",
    "colombia": "America/Bogota",
    "ecuador": "America/Guayaquil",
    "bolivia": "America/La_Paz",
    "paraguay": "America/Asuncion",
    "uruguay": "America/Montevideo",
    "egypt": "Africa/Cairo",
    "morocco": "Africa/Casablanca",
    "tunisia": "Africa/Tunis",
    "algeria": "Africa/Algiers",
    "nigeria": "Africa/Lagos",
    "kenya": "Africa/Nairobi",
    "ethiopia": "Africa/Addis_Ababa",
    "ghana": "Africa/Accra",
    "sudan": "Africa/Khartoum",
    "tanzania": "Africa/Dar_es_Salaam",
    "saudi arabia": "Asia/Riyadh",
    "iran": "Asia/Tehran",
    "pakistan": "Asia/Karachi",
    "bangladesh": "Asia/Dhaka",
    "thailand": "Asia/Bangkok",
    "indonesia": "Asia/Jakarta",
    "malaysia": "Asia/Kuala_Lumpur",
    "vietnam": "Asia/Ho_Chi_Minh",
    "myanmar": "Asia/Yangon",
    "kazakhstan": "Asia/Almaty",
    "uzbekistan": "Asia/Tashkent",
    "afghanistan": "Asia/Kabul"
}
from rapidfuzz import process, fuzz

def get_best_match(country):
    """Finds the closest matching country name using fuzzy matching."""
    result = process.extractOne(country, country_map.keys(), scorer=fuzz.ratio)

    if not result or len(result) < 2:  # Ensure result is valid and has at least two values
        return None

    match, score = result[:2]  # Extract only the first two values
    return match if score > 80 else None  # Use a confidence threshold of 80%


def get_time_in_country(country):
    """Fetches the current time for a given country, correcting typos if needed."""
    try:
        country = country.lower().strip()
        best_match = get_best_match(country)

        if not best_match:
            return f"Sorry, I couldn't recognize '{country}'. Please try again."

        timezone = country_map[best_match]
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone={timezone}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                current_time = data["formatted"]
                return f"The current time in {best_match.title()} is {current_time}."
            else:
                return f"Error fetching time for {best_match.title()}. Message: {data.get('message', 'Unknown error')}"

        return f"Error fetching time for {best_match.title()}. Status code: {response.status_code}"

    except Exception as e:
        return f"Error fetching time: {str(e)}"

def generate_response(user_input):
    """Provides chatbot responses and handles country requests."""
    responses = {
        "hello": "Hi! How can I assist you today?",
        "how are you": "I'm doing great, thank you! How about you?",
        "bye": "Goodbye! Have a great day!",
    }

    user_input = user_input.lower().strip()

    for key in responses:
        if key in user_input:
            return responses[key]

    return get_time_in_country(user_input)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chat interactions and returns responses."""
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify(response="Please enter a valid country or message.")

    bot_response = generate_response(user_message)
    return jsonify(response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
