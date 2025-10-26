from flask import Blueprint, jsonify, request, render_template
import random
import requests
from datetime import date

utils_bp = Blueprint("utils", __name__)


@utils_bp.route("/wizard")
def generate_wizard_name():
    prefixes = ["Thal", "Eld", "Zyn", "Mor", "Alar", "Xan", "Vor", "Gal", "Ser"]
    roots = ["drak", "mir", "vyn", "zar", "quor", "lith", "mael", "gorn", "ther"]
    suffixes = ["ion", "ar", "ius", "en", "or", "eth", "azar", "em", "yx"]
    titles = ["Archmage", "Sorcerer", "Seer", "Mystic", "Enchanter", "Spellbinder"]
    name = random.choice(prefixes) + random.choice(roots) + random.choice(suffixes)
    return f"{random.choice(titles)} {name.capitalize()}"


@utils_bp.route("/generatePassword")
def generatePassword():
    # Provide the same behavior as the previous implementation but safe defaults
    Length = request.args.get("Length", default=12, type=int)
    Complexity = request.args.get("Complexity", default="simple")
    letters = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    symbols = "~!@#$%^&*()-_=+[{]}|;:,<.>/?"
    password = ""
    characters = ""
    if Complexity == "basic":
        characters = letters
    elif Complexity == "simple":
        characters = letters + numbers
    elif Complexity == "complex":
        characters = letters + letters.upper() + numbers + symbols
    else:
        return jsonify({"error": "Choose a valid option: basic, simple, or complex."}), 400
    for _ in range(Length):
        password += random.choice(characters)
    return jsonify({"password": password})


@utils_bp.route("/randomRestaurant")
def choose_restaurant():
    restaurants = [
        "Red Fort Cuisine Of India",
        "Painted Pony Restaurant",
        "Sakura Japanese Steakhouse",
        "Rusty Crab Daddy",
        "Mixed Greens",
        "Cliffside Restaurant",
        "Aubergine Kitchen",
        "Panda Express",
        "Del Taco",
        "Chic-fil-a",
    ]
    return jsonify({"restaurant": random.choice(restaurants)})


@utils_bp.route("/random-weather")
def random_weather():
    conditions = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]
    condition = random.choice(conditions)
    temperature = f"{random.randint(-30, 50)}C"
    humidity = f"{random.randint(10, 100)}%"
    return jsonify({"condition": condition, "temperature": temperature, "humidity": humidity})


@utils_bp.route("/real-weather")
def real_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.1041&longitude=-113.5841&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min,precipitation_probability_mean&current=temperature_2m,relative_humidity_2m,is_day,precipitation,wind_speed_10m,wind_direction_10m&timezone=America%2FDenver&forecast_days=1&wind_speed_unit=mph&temperature_unit=fahrenheit"
    try:
        data = requests.get(url, timeout=3).json()
    except Exception:
        return jsonify({"error": "failed to fetch weather"}), 502
    current_weather = data.get("current", {})
    daily_data = data.get("daily", {})

    current_data = {
        "time": current_weather.get("time"),
        "temperature": current_weather.get("temperature_2m"),
        "humidity": current_weather.get("relative_humidity_2m"),
        "windspeed": current_weather.get("wind_speed_10m"),
        "winddirection": current_weather.get("wind_direction_10m"),
    }

    daily_data = {
        "sunrise": daily_data.get("sunrise"),
        "sunset": daily_data.get("sunset"),
        "temperature_min": daily_data.get("temperature_2m_min"),
        "temperature_max": daily_data.get("temperature_2m_max"),
        "precipitation_probability": daily_data.get("precipitation_probability_mean"),
    }

    return jsonify(current_data, daily_data)


@utils_bp.route("/fav_quote")
def fav_quote():
    fav_quote = [
        "Just one small positive thought in the morning can change your whole day. - Dalai Lama",
        "Opportunities don't happen, you create them. - Chris Grosser",
        "If you can dream it, you can do it. - Walt Disney",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Why fit in when you were born to stand out? - Dr. Seuss",
        "One day or day one. You decide. - Unknown",
        "Slow is smooth, smooth is fast, fast is sexy. - Old Grunt",
    ]
    return jsonify({"fav_quote": random.choice(fav_quote)})


@utils_bp.route("/client")
def client_info():
    from user_agents import parse

    user_agent_string = request.headers.get("User-Agent")
    user_agent = parse(user_agent_string)
    return jsonify(
        {
            "Browser": user_agent.browser.family,
            "Version": user_agent.browser.version_string,
            "OS": user_agent.os.family,
            "OS Version": user_agent.os.version_string,
        }
    )


@utils_bp.route("/random_pokemon")
def random_pokemon():
    a = random.randint(1, 1010)
    return jsonify({"redirect_to": f"https://www.pokemon.com/us/pokedex/{a}"})
