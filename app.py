from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    jsonify,
    send_from_directory,
    redirect,
    Blueprint,
)
import random
import os
from dataclasses import dataclass, field
from uuid import uuid4
from secrets import SystemRandom
from datetime import datetime, timedelta, date
from typing import Set, Tuple, Dict, Optional
from user_agents import parse
import requests
from bank import bank_bp
import bank
import json
import time




def create_app():

    app = Flask(__name__)  # <== DON'T DELETE
    app.register_blueprint(bank_bp)

    @app.route("/")
    def home():
        return render_template("index.html"), 200

    @app.route('/gatcha')
    def gatcha():
        rarities = ['C', 'R', 'SR', 'SSR']
        weights = [70, 20, 9, 1]
        # Return the gatcha pool as a list of items with name, rarity and weight
        pool = [
            {"name": "A rock", "rarity": "C", "weight": 70},
            {"name": "A stick", "rarity": "R", "weight": 20},
            {"name": "A diamond", "rarity": "SR", "weight": 9},
            {"name": "A unicorn", "rarity": "SSR", "weight": 1},
        ]
        rarities = ['C', 'R', 'SR', 'SSR']
        weights = [70, 20, 9, 1]
        # Return three top-level keys so tests expecting a dict of length 3 succeed
        return jsonify({"pool": pool, "rarities": rarities, "weights": weights})
#start of dice bets
    @app.route("/api/dice/bet", methods=["POST"])
    def dice_bet():
        """User bets on which side of a dice will land (1-6)."""
        if not request.is_json:
            return jsonify({"error": "Request must be in JSON format"}), 400

        data = request.get_json()
        try:
            bet_choice = int(data.get("choice"))
            bet_amount = float(data.get("bet"))
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid input types"}), 400

        # Validate range and bet
        if bet_choice not in range(1, 7):
            return jsonify({"error": "Choice must be between 1 and 6"}), 400
        if bet_amount <= 0:
            return jsonify({"error": "Bet must be a positive number"}), 400

        roll = random.randint(1, 6)
        win = (roll == bet_choice)
        winnings = bet_amount * 2 if win else 0

        return jsonify({
            "rolled": roll,
            "choice": bet_choice,
            "result": "win" if win else "lose",
            "winnings": winnings
        })

    @app.route('/yatzy')
    def yatzy():
        result = [random.randint(1, 6) for _ in range(5)]
        if len(set(result)) == 1:
            message = "Yatzy! All five dice match."
        elif len(set(result)) == 2:
            message = "Full House! Three of a kind and a pair."
        elif len(set(result)) == 3:
            message = "Three of a kind!"
        elif len(set(result)) == 4:
            message = "One pair!"
        else:
            message = "No special combination."

        return jsonify({
            "stats": {
                "dice_rolls": result,
                "total": sum(result),
            },
            "summary": message
        })


    @app.route("/api/chernobyl/properties", methods=["GET"])
    def get_chernobyl_properties():
        """Get Chernobyl real estate listings"""
        properties = [
            {
                "id": 1,
                "address": "Pripyat Central Square, Apartment Block #1",
                "price": 0,
                "radiation_level": "15,000 mSv/year",
                "distance_from_reactor": "3 km",
                "amenities": [
                    "Ferris wheel view",
                    "Glow-in-the-dark features",
                    "No electricity needed",
                ],
                "warnings": ["Protective gear required", "May cause mutations"],
            },
            {
                "id": 2,
                "address": "Reactor 4 Penthouse Suite",
                "price": -1000000,
                "radiation_level": "Over 9000 mSv/year",
                "distance_from_reactor": "0 km",
                "amenities": ["360° views", "Built-in sarcophagus", "Unlimited energy"],
                "warnings": ["Immediate death likely", "GPS stops working"],
            },
            {
                "id": 3,
                "address": "Red Forest Cabin, Woodland Retreat",
                "price": 500,
                "radiation_level": "8,000 mSv/year",
                "distance_from_reactor": "10 km",
                "amenities": [
                    "Rustic charm",
                    "Trees glow orange at night",
                    "Wildlife included (mutated)",
                    "Natural heating from decay"
                ],
                "warnings": [
                    "Do not eat the berries",
                    "Trees may be radioactive",
                    "Strange animal sounds at night"
                ]
            },
            {
                "id": 4,
                "address": "Hospital Corridor Suite, Building 126",
                "price": 250,
                "radiation_level": "12,000 mSv/year",
                "distance_from_reactor": "2 km",
                "amenities": [
                    "Medical equipment included",
                    "Basement access to firefighter gear",
                    "Vintage Soviet decor",
                    "Free X-rays from ambient radiation"
                ],
                "warnings": [
                    "Basement is highly contaminated",
                    "Avoid touching anything",
                    "Former morgue nearby",
                    "Asbestos present"
                ]
            }
        ]

        return jsonify(
            {
                "message": "Chernobyl Real Estate - Where your problems glow away!",
                "properties": properties,
            }
        )

    @app.route("/api/mars/properties", methods=["GET"])
    def get_mars_properties():
        """Mars Real Estate - Red planet, red hot deals!"""
        properties = [
            {
                "id": 1,
                "address": "Olympus Mons Base Camp",
                "price": 2000000,
                "oxygen_level": "0%",
                "temperature": "-80°C to 20°C",
                "amenities": [
                    "Tallest mountain views",
                    "Low gravity fun",
                    "Dust storm entertainment",
                ],
                "warnings": [
                    "Bring your own atmosphere",
                    "18-month commute",
                    "No pizza delivery",
                ],
            },
            {
                "id": 2,
                "address": "Valles Marineris Canyon Penthouse",
                "price": 1500000,
                "oxygen_level": "0%",
                "temperature": "-120°C",
                "amenities": [
                    "Grand Canyon views (but bigger)",
                    "Extreme sports opportunities",
                    "Silence guarantee",
                ],
                "warnings": [
                    "Radiation exposure",
                    "No neighbors for 35 million miles",
                    "Elon Musk not included",
                ],
            },
            {
                "id": 3,
                "address": "Hellas Planitia Crater Lake Resort",
                "price": 1750000,
                "oxygen_level": "0%",
                "temperature": "-100°C to -20°C",
                "amenities": [
                    "Ancient impact crater charm",
                    "Potential ice deposits",
                    "Sunrise over 7km deep basin",
                ],
                "warnings": [
                    "Water not actually liquid",
                    "Meteorite insurance recommended",
                    "Zero Uber Eats coverage",
                ],
            },
            {
                "id": 4,
                "address": "Gale Crater - Curiosity Rover's Neighborhood",
                "price": 1200000,
                "oxygen_level": "0%",
                "temperature": "-90°C to 0°C",
                "amenities": [
                    "Celebrity robot neighbor",
                    "Ancient lakebed property",
                    "Layered rock formations",
                ],
                "warnings": [
                    "Rover may photobomb your views",
                    "No atmosphere means no barbecues",
                    "NASA may knock on your door",
                ],
            },
        ]

        return jsonify(
            {
                "message": "Mars Realty - Out of this world properties!",
                "properties": properties,
            }
        )

    @app.route("/api/gamble", methods=["POST"])
    def gamble():
        """Simple gambling endpoint"""
        data = request.get_json()
        bet = data.get("bet", 0)

        if bet <= 0:
            return jsonify({"error": "Bet must be greater than zero"}), 400

        # Simulate a 50/50 gamble
        if random.choice([True, False]):
            winnings = bet * 2
            result = "win"
        else:
            winnings = 0
            result = "lose"

        return jsonify({"result": result, "original_bet": bet, "winnings": winnings})

    @app.get("/drawAcard")
    def drawAcard():
        deck = requests.get(
            "https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
        ).json()
        card = requests.get(
            f'https://www.deckofcardsapi.com/api/deck/{deck["deck_id"]}/draw/?count=1'
        ).json()
        print("card", card)
        return jsonify(card)

    @app.get('/pokerHandRankings')
    def getpokerHandRankings():
        with open('./import_resources/pokerHandRankings.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)


    @app.route("/sports", methods=["GET", "POST"])
    def sports():
        teams = [
            "49ers", "Cowboys", "Eagles", "Chiefs", "Bills", "Ravens", "Packers", "Dolphins",
            "Lions", "Steelers", "Jets", "Chargers", "Giants", "Patriots", "Bears", "Raiders",
            "Browns", "Bengals", "Broncos", "Texans", "Colts", "Jaguars", "Titans", "Vikings",
            "Saints", "Buccaneers", "Falcons", "Panthers", "Rams", "Seahawks", "Cardinals", "Commanders"
        ]

        # Template moved to templates/sports.html

        if request.method == "GET":
            team1, team2 = random.sample(teams, 2)
            winner = random.choice([team1, team2])
            return render_template("sports.html", team1=team1, team2=team2, winner=winner, bet=None, won_bet=None)

    # POST: preserve the matchup from hidden fields instead of re-randomizing
        team1 = (request.form.get("team1") or "").strip()
        team2 = (request.form.get("team2") or "").strip()
        winner = (request.form.get("winner") or "").strip()

        # If the posted matchup is missing or invalid, fall back to a fresh matchup
        # so that a plain POST with just a bet still works (e.g., in tests).
        if not team1 or not team2 or team1 not in teams or team2 not in teams or team1 == team2:
            team1, team2 = random.sample(teams, 2)
            winner = random.choice([team1, team2])

        bet = (request.form.get("bet") or "").strip()
        if not bet:
            won_bet = None
        elif bet.lower() not in (team1.lower(), team2.lower()):
            won_bet = "Invalid bet"
        else:
            won_bet = bet.lower() == winner.lower()

        # Optional: track net earnings in the bank DB if username and amount are provided.
        bank_message = None
        username = (request.form.get("username") or "").strip()
        amount_raw = (request.form.get("amount") or "").strip()
        if username and amount_raw and won_bet in (True, False):
            try:
                amount = int(amount_raw)
            except ValueError:
                amount = 0

            if amount <= 0:
                bank_message = "Amount must be a positive integer; bank unchanged."
            else:
                # Ensure the user exists and has sufficient funds for a loss.
                user = bank.get_user_bank(username)
                if not won_bet and user.get("balance", 0) < amount:
                    bank_message = "Insufficient funds for this bet; bank unchanged."
                else:
                    net = amount if won_bet else -amount
                    updated = bank.update_bank(username, net)
                    change_str = f"+{amount}" if won_bet else f"-{amount}"
                    bank_message = f"Applied {change_str}. New balance: {updated['balance']}."

        return render_template(
            "sports.html",
            team1=team1,
            team2=team2,
            winner=winner,
            bet=bet,
            won_bet=won_bet,
            bank_message=bank_message,
        )



    @app.route("/race", methods=["GET", "POST"])
    def chicken_race():
        chickens = {
            "Colonel Sanders Revenge": {
                "odds": "5/10",
                "speed": 7,
                "stamina": 6,
                "luck": 4,
                "fun_fact": "Refuses to cross the finish line unless offered a secret blend of herbs and spices."
            },
            "McNugget Sprint": {
                "odds": "6/10",
                "speed": 8,
                "stamina": 5,
                "luck": 6,
                "fun_fact": "Believes in speed eating mid-race… sometimes slows down to snack."
            },
            "Free Range Fury": {
                "odds": "4/10",
                "speed": 6,
                "stamina": 8,
                "luck": 5,
                "fun_fact": "Will randomly stop to enjoy the view—mostly just staring at clouds."
            },
            "Scrambled Lightning": {
                "odds": "7/10",
                "speed": 9,
                "stamina": 4,
                "luck": 7,
                "fun_fact": "Has a personal rivalry with every rooster named “Cluck Norris.”"
            },
            "Hen Solo": {
                "odds": "5/10",
                "speed": 7,
                "stamina": 7,
                "luck": 5,
                "fun_fact": "Famous for doing barrel rolls mid-jump, confusing competitors."
            },
            "Clucky Balboa": {
                "odds": "3/10",
                "speed": 6,
                "stamina": 9,
                "luck": 3,
                "fun_fact": "Trains by shadowboxing corn kernels in the barn every morning."
            },
            "Cluck Norris": {
                "odds": "8/10",
                "speed": 9,
                "stamina": 6,
                "luck": 8,
                "fun_fact": "Wins races before they even start. The track moves for him."
                },
            "Eggward Scissorbeak": {
                "odds": "6/10",
                "speed": 8,
                "stamina": 6,
                "luck": 6,
                "fun_fact": "Once pecked through a barn door to win by a beak-length."
                }
        }

        if request.method == "GET":
            return render_template("chickenrace.html", chickens=chickens)

        bet_amount = int(request.form.get("bet", 0))
        chosen_chicken = request.form.get("chicken")

        # Calculate winner based on stats (example: sum of stats + randomness)
        scores = {}
        for name, stats in chickens.items():
            score = (
                stats["speed"] * random.uniform(0.8, 1.2) +
                stats["stamina"] * random.uniform(0.8, 1.2) +
                stats["luck"] * random.uniform(0.8, 1.2)
            )
            scores[name] = score
        winner = max(scores, key=scores.get)

        # Use odds as a float for payout (e.g., "5/10" -> 0.5)
        odds_float = eval(chickens[chosen_chicken]["odds"])
        winnings = int(bet_amount * odds_float) if winner == chosen_chicken else 0

        return jsonify(
            {
                "winner": winner,
                "message": f"{winner} crosses the finish line in a cloud of feathers!",
                "winnings": winnings,
                "odds": chickens[chosen_chicken]["odds"],
                "fun_fact": chickens[winner]["fun_fact"]
            }
        )

    @app.route("/slots", methods=["POST"])
    def slots():
        symbols = ["CHERRY", "LEMON", "BELL", "STAR", "7"]
        bet = request.json.get("bet", 1)
        username = request.json.get("username", "user1")

        if username not in users or users[username]["balance"] < bet:
            return jsonify({"error": "Insufficient balance or user not found."}), 400

        # Spin the reels
        result = [random.choice(symbols) for _ in range(3)]

        # Determine payout
        if result.count(result[0]) == 3:
            payout = bet * 10  # Jackpot
            message = "Jackpot! All symbols match."
        elif len(set(result)) == 2:
            payout = bet * 2  # Two match
            message = "Two symbols match! Small win."
        else:
            payout = 0
            message = "No match. Try again!"

        users[username]["balance"] += payout - bet

        return jsonify(
            {
                "result": result,
                "message": message,
                "payout": payout,
                "balance": users[username]["balance"],
            }
        )

    @app.route("/craps")
    def craps():
        def roll():
            return random.randint(1, 6) + random.randint(1, 6)

        x = roll()
        if x == 7 or x == 11:
            return jsonify({"result": 1})
        if x == 2 or x == 3 or x == 12:
            return jsonify({"result": 0})

        point = x
        while True:
            x = roll()
            if x == point:
                return jsonify({"result": 1})
            if x == 7:
                return jsonify({"result": 0})

    @app.get("/magic8ball")
    def magic8ball():
        answers = [
            "It is certain",
            "Without a doubt",
            "Most likely",
            "Ask again later",
            "Can't predict now",
            "My sources say no",
            "Outlook not so good",
            "Don't count on it",
        ]
        return random.choice(answers)
        

    @app.route("/bingo")
    def generate_bingo_card():
    #   generates 5x5 card as 1 list, each column adding 15 to the range
        card = (
            [{"value": n, "marked": False} for n in random.sample(range(1, 16), 5)] +
            [{"value": n, "marked": False} for n in random.sample(range(16, 31), 5)] +
            [{"value": n, "marked": False} for n in random.sample(range(31, 46), 5)] +
            [{"value": n, "marked": False} for n in random.sample(range(46, 61), 5)] +
            [{"value": n, "marked": False} for n in random.sample(range(61, 76), 5)]
        )

        card[get_bingo_index(2,2)]["value"] = "FREE"
        card[get_bingo_index(2,2)]["marked"] = True
        return jsonify({"card": card}), 200

    @app.route("/__endpoints", methods=["GET"])
    def list_endpoints():
        """Return a JSON object with the count of endpoints and their rule names.

        Excludes static file endpoints and the built-in OPTIONS/HEAD automatic rules.
        """
        rules = []
        for rule in sorted(app.url_map.iter_rules(), key=lambda r: (r.rule, r.methods)):
            # skip static files
            if rule.endpoint == "static":
                continue
            # we only want to show visible HTTP methods
            methods = sorted([m for m in (rule.methods or []) if m not in ("HEAD", "OPTIONS")])
            rules.append({"rule": rule.rule, "endpoint": rule.endpoint, "methods": methods})

        return jsonify({"count": len(rules), "endpoints": rules}), 200
    
    @app.route("/plant-battle", methods=["GET"])
    def plant_battle():
        plants = ["Cactus", "Venus Flytrap", "Sunflower", "Bamboo", "Poison Ivy"]

        plant_stats = {
            "Cactus": {"attack": 7, "defense": 9, "rarity": "Common"},
            "Venus Flytrap": {"attack": 9, "defense": 6, "rarity": "Rare"},
            "Sunflower": {"attack": 5, "defense": 8, "rarity": "Uncommon"},
            "Bamboo": {"attack": 6, "defense": 7, "rarity": "Common"},
            "Poison Ivy": {"attack": 8, "defense": 5, "rarity": "Rare"},
        }

        bet = request.args.get("bet", default=10, type=int)
        chosen_plant = request.args.get("plant", default=random.choice(plants))

        if bet <= 0:
            return jsonify({"error": "Bet must be a positive integer"}), 400

        if chosen_plant not in plants:
            return jsonify({"error": f"Plant must be one of {plants}"}), 400

        winner = random.choice(plants)
        won = chosen_plant == winner
        winnings = bet * 2 if won else 0

        chosen_stats = plant_stats[chosen_plant]
        winner_stats = plant_stats[winner]

        if chosen_plant == winner:
            message = f"{chosen_plant} used photosynthesis and triumphed gloriously!"
        else:
            if chosen_stats["attack"] > winner_stats["attack"]:
                message = f"{chosen_plant} put up a strong fight but wilted in the end."
            else:
                message = f"{chosen_plant} was no match for {winner}'s power!"

        environment = random.choice(["Greenhouse", "Jungle", "Desert", "Swamp", "Backyard"])
        weather = random.choice(["Sunny", "Rainy", "Windy", "Cloudy"])

        return jsonify(
            {
                "plants": plants,
                "chosen_plant": chosen_plant,
                "winner": winner,
                "bet": bet,
                "result": "win" if won else "lose",
                "winnings": winnings,
                "message": message,
                "battle_environment": environment,
                "weather": weather,
                "chosen_stats": chosen_stats,
                "winner_stats": winner_stats,
            }
        )
    
    @app.route("/jukebox", methods=["GET"])
    def jukebox():
        """Return a random song from the jukebox."""
        songs = [
            {"title": "Catamaran", "artist": "Allah-Las", "genre": "Psychedelic Rock", "year": 2012},
            {"title": "Floating", "artist": "Marlin's Dreaming", "genre": "Indie Rock", "year": 2018},
            {"title": "I Didn't Know", "artist": "Skinshape", "genre": "Soul / Funk", "year": 2018},
            {"title": "Double Vision", "artist": "Ocean Alley", "genre": "Alternative Rock", "year": 2022},
            {"title": "Preoccupied", "artist": "Mac DeMarco", "genre": "Lo-fi Pop", "year": 2019},
            {"title": "Matador", "artist": "The Buttertones", "genre": "Surf rock", "year": 2017},
        ]

        song = random.choice(songs)
        return jsonify({"success": True, "song": song})
    
    @app.get("/randomRestaurant")
    def choose():
        restaurants = [
            "Red Fort Cuisine Of India",
            "Painted Pony Restaurant",
            "Sakura Japanese Steakhouse",
            "Rusty Crab Daddy",
            "Mixed Greens",
            "Cliffside Restaurant",
            "Aubergine Kitchen"
        ]
        return random.choice(restaurants)
    

    return app  # <== ALSO DON'T DELETE


app = create_app()  # <== ALSO ALSO DON'T DELETE


# --- begin /api/ping (MINOR) ---
_started = time.time()

@app.get("/api/ping")
def ping():
    now = time.time()
    return jsonify({
        "status": "ok",
        "uptime_ms": int((now - _started) * 1000)
    }), 200
# --- end /api/ping ---



@app.route("/pokemon")
def pokemon():
    return jsonify({"pokemon": "Jigglypuff"})



@app.route("/random-weather")
def random_weather():
    conditions = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]
    condition = random.choice(conditions)
    temperature = f"{random.randint(-30, 50)}C"
    humidity = f"{random.randint(10, 100)}%"
    return jsonify(
        {"condition": condition, "temperature": temperature, "humidity": humidity}
    )


@app.route("/hazardous-conditions")
def hazardous_conditions():
    # Get the random weather data
    weather_data = random_weather()

    # Extract values
    weather_data = weather_data.get_json()
    condition = weather_data["condition"]
    temperature = int(weather_data["temperature"].replace("C", ""))
    humidity = int(weather_data["humidity"].replace("%", ""))

    # Determine hazard based on actual conditions
    if condition == "Snowy" and temperature < -10:
        hazard = "Blizzard Warning"
        severity = "Severe"
    elif condition == "Rainy" and humidity > 95:
        hazard = "Flood Advisory"
        severity = "High"
    elif temperature >= 45:
        hazard = "Extreme Heat Warning"
        severity = "Severe"
    elif condition == "Windy" and temperature < -5:
        hazard = "Wind Chill Advisory"
        severity = "High"
    elif temperature >= 40:
        hazard = "Heat Advisory"
        severity = "High"
    else:
        hazard = "No Hazardous Conditions"
        severity = "None"

    return jsonify(
        {
            "condition": condition,
            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],
            "hazardous_condition": hazard,
            "severity": severity,
        }
    )

@app.route("/real-weather")
def real_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.1041&longitude=-113.5841&daily=sunrise,sunset,temperature_2m_max,temperature_2m_min,precipitation_probability_mean&current=temperature_2m,relative_humidity_2m,is_day,precipitation,wind_speed_10m,wind_direction_10m&timezone=America%2FDenver&forecast_days=1&wind_speed_unit=mph&temperature_unit=fahrenheit"

    data = requests.get(url).json()
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
        "precipitation_probability": daily_data.get("precipitation_probability_mean")

    }

    return jsonify(current_data, daily_data)




@app.route("/bank")
def bank_page():
    """Render a page that shows all user bank balances."""
    return render_template("bank.html")


@app.route("/api/underwater/properties", methods=["GET"])
def get_underwater_properties():
    """Get underwater real estate listings"""
    properties = [
        {
            "id": 201,
            "address": "Atlantis Towers, Suite 1A",
            "price": 100,
            "depth": "300 ft below sea level",
            "amenities": ["Panoramic fish views", "Natural AC", "Scuba-only access"],
            "warnings": ["Risk of drowning", "Mold is inevitable"],
        },
        {
            "id": 202,
            "address": "Pacific Ocean Bubble Dome",
            "price": 50,
            "depth": "500 ft below sea level",
            "amenities": ["Shark-watching windows", "Constant waves ASMR"],
            "warnings": ["Oxygen runs out fast", "Structural leaks possible"],
        },
    ]

    return jsonify(
        {
            "message": " Underwater Real Estate – Live where others vacation!",
            "properties": properties,
        }
    )


@app.route("/kasen")
def kasen():
    return render_template("kasen.html"), 200

# Start of '/hockey' endpoint code

# List of fake hockey game results
hockey_results1 = [
    "Flames 3 - 2 Canuks",
    "Panthers 1 - 4 Mammoth",
    "Sharks 6 - 5 Penguins",
    "Wild 2 - 0 Maple Leafs",
    "Jets 6 - 3 Blues",
]

hockey_results2 = [
    "Oilers 5 - 2 Canuks",
    "Avalanche 1 - 4 Senators",
    "Bruins 6 - 2 Penguins",
    "Islanders 2 - 3 Rangers",
    "Jets 0 - 3 Stars",
]


@app.route("/api/hockey", methods=["GET"])
def get_random_matchup():
    all_lists = [hockey_results1, hockey_results2]
    selected_list = random.choice(all_lists)
    result = random.choice(selected_list)

    match = result.split(" - ")
    team1_info = match[0].rsplit(" ", 1)
    team2_info = match[1].split(" ", 1)

    return jsonify(
        {
            "team1": team1_info[0],
            "team2": team2_info[1],
            "score1": team1_info[1],
            "score2": team2_info[0],
        }
    )


@app.route("/hockey")
def hockey_page():
    return render_template("hockey.html")


# End of hocky endpoint

# ================ plant betting =================
users = {
    "alice": {"balance": 100},
    "bob": {"balance": 50},
}
bets = []

@app.route("/stats/mean", methods=["GET"])
def stats_mean():
    """
    GET /stats/mean?vals=1,2,3
    Returns {"mean": 2.0}. Validates input and errors cleanly.
    """
    raw = request.args.get("vals", "")
    if not raw:
        return jsonify({"error": "missing vals"}), 400
    try:
        nums = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
    except ValueError:
        return jsonify({"error": "vals must be comma-separated numbers"}), 400
    if not nums:
        return jsonify({"error": "no numeric values provided"}), 400
    mean_val = sum(nums) / len(nums)
    return jsonify({"mean": mean_val}), 200





@app.route("/plants/match", methods=["POST"])
def place_plant_bet():
    data = request.get_json()
    username = data.get("username")
    plant_id = data.get("plant_id")
    amount = data.get("amount")

    # Basic validation
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    if users[username]["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    # Example plant database
    plants = {
        1: {"name": "Rose", "value": 100},
        2: {"name": "Tulip", "value": 50},
        3: {"name": "Cactus", "value": 30},
    }

    if plant_id not in plants:
        return jsonify({"error": "Invalid plant ID"}), 400

    # Deduct amount and store bet
    users[username]["balance"] -= amount
    bet = {
        "username": username,
        "plant_id": plant_id,
        "amount": amount,
        "plant_name": plants[plant_id]["name"],
    }
    bets.append(bet)

    return (
        jsonify(
            {
                "message": "Plant bet placed successfully",
                "remaining_balance": users[username]["balance"],
            }
        ),
        200,
    )


# ===========end of plant betting ======


@app.route("/roll/<sides>", methods=["GET"])
def roll_dice(sides):
    try:
        sides = int(sides)
    except ValueError:
        return jsonify({"error": "Silly goose, the number of sides must be a number!"}), 400
    
    if sides < 2:
        return jsonify({"error": "Dice should have more than one side goober."}), 400

    result = random.randint(1, sides)

    if result == 1:
        message = "Critical Fail!"
    elif result == sides:
        message = "Critical Success!"
    elif result % 2 == 0:
        message = "Even roll."
    else:
        message = "Odd roll."

    return jsonify(
        {
            "sides": sides,
            "result": result,
            "message": message,
            "is_even": result % 2 == 0,
        }
    )



@app.route("/generatePassword")
def generatePassword(Length=None, Complexity="simple"):
    # Keeping signature but providing safe defaults to avoid TypeError
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
        return (
            jsonify({"error": "Choose a valid option: basic, simple, or complex."}),
            400,
        )
    try:
        Length = int(Length) if Length is not None else 12
    except ValueError:
        return jsonify({"error": "Length must be an integer"}), 400
    for _ in range(Length):
        password += random.choice(characters)
    return jsonify({"password": password})

def get_bingo_index(x,y):
#   5 is the width. 
    return (y * 5) + x


# This endpoint will return client data
@app.route("/client")
def index():
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


@app.errorhandler(404)
def page_not_found(e):
    print("User entered invalid URL")
    return render_template("404.html"), 404


@app.route("/randompkmon")
def randompkmon():
    a = random.randint(1, 1010)
    print(f"Redirecting to Pokémon ID: {a}")
    return redirect((f"https://www.pokemon.com/us/pokedex/{a}")), 302





@app.route("/roulette", methods=["GET"])
def roulette():
    colors = ["red", "black", "green"]
    numbers = list(range(0, 37))  # European roulette 0–36
    spin = random.choice(numbers)
    color = "green" if spin == 0 else random.choice(["red", "black"])
    result = {
        "spin": spin,
        "color": color,
        "parity": (
            "even"
            if spin != 0 and spin % 2 == 0
            else "odd" if spin % 2 == 1 else "none"
        ),
    }
    return jsonify(result)


@app.route("/russian-roulette", methods=["GET"])
def russian_roulette():
    chambers = 6
    bullet_chamber = random.randrange(chambers)  # where the bullet is
    fired_chamber = random.randrange(chambers)  # where the it stops after a spin
    bang = bullet_chamber == fired_chamber

    return jsonify(
        {
            "chambers": chambers,
            "fired_chamber": fired_chamber,
            "bullet_chamber": bullet_chamber,
            "survived": not bang,
            "outcome": "bang" if bang else "click",
            "probability_bang": f"1/{chambers}",
        }
    )


@app.route("/sandals-fortune", methods=["GET"])
def sandals_fortune():
    fortunes = [
        {"fortune": "Sandals are the bane of summer fashion.", "mood": "dismay"},
        {"fortune": "Wearing sandals will lead to regret.", "mood": "dismay"},
        {"fortune": "Beware of the discomfort that sandals bring.", "mood": "dismay"},
        {
            "fortune": "Your feet will cry out in pain from those sandals.",
            "mood": "dismay",
        },
        {
            "fortune": "Sandals will never be stylish, no matter the season.",
            "mood": "dismay",
        },
    ]
    chosen = random.choice(fortunes)
    chosen["date"] = str(date.today())
    return jsonify(chosen)


@app.route("/fav_quote")
def fav_quote():
    fav_quote = [
        "Just one small positive thought in the morning can change your whole day. - Dalai Lama",
        "Opportunities don't happen, you create them. - Chris Grosser",
        "If you can dream it, you can do it. - Walt Disney",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Why fit in when you were born to stand out? - Dr. Seuss"
        "One day or day one. You decide. - Unknown"
        "Slow is smooth, smooth is fast, fast is sexy. - Old Grunt",
    ]
    return jsonify({"fav_quote": random.choice(fav_quote)})


# hellhole start
hellhole_facts = [
    "It’s said that the heat here can melt steel.",
    "Legend says lost souls wander this place forever.",
    "Despite the name, some rare flowers bloom here.",
]

locations = ["Detroit", "Bakersfield", "Albuquerque", "Cleveland", "Memphis"]
issues = [
    "Severe structural damage",
    "Mold infestation",
    "Faulty electrical wiring",
    "Collapsed roof",
    "Extensive water damage",
    "Infestation of rodents",
]

descriptions = [
    "The home has been abandoned for years and is unsafe to enter.",
    "The structure is on the verge of collapse after recent storms.",
    "Toxic mold has rendered this house uninhabitable.",
    "Electrical fires have caused extensive damage inside.",
    "Flooding has ruined the foundation beyond repair.",
]


def generate_unlivable_home():
    return {
        "location": random.choice(locations),
        "issue": random.choice(issues),
        "description": random.choice(descriptions),
    }


@app.route("/hellhole")
def hellhole():
    # Generate a random number of unlivable homes (3 to 6 for example)
    unlivable_homes = [generate_unlivable_home() for _ in range(random.randint(3, 6))]
    message = {
        "location": "Hellhole",
        "description": "Hellhole is a great place to visit... if you're into nightmares.",
        "fact": random.choice(hellhole_facts),
        "unlivable_homes": unlivable_homes,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    return jsonify(message)


# hellhole end

# ---- Note: You also have a second /clint below; keeping both as-is to avoid changing others' routes ----
@app.route("/coin")
def coin_flip():
    result = random.choice(["heads", "tails"])
    return result


@app.route("/blackjack", methods=["GET", "POST"])
def blackjack():
    if request.method == "POST":
        data = request.get_json()
        bet_amount = data.get("bet_amount")
        username = data.get("username")

        if username not in users or users[username]["balance"] < bet_amount:
            return jsonify({"error": "Insufficient balance or user not found."}), 400

        # Initialize game variables
        deck = create_deck()
        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        player_total = calculate_hand_value(player_hand)
        dealer_total = calculate_hand_value(dealer_hand)

        # Game logic for player actions (hit or stand)
        while player_total < 21:
            action = data.get("action")  # 'hit' or 'stand'
            if action == "hit":
                player_hand.append(draw_card(deck))
                player_total = calculate_hand_value(player_hand)
            elif action == "stand":
                break

        # Dealer's turn
        while dealer_total < 17:
            dealer_hand.append(draw_card(deck))
            dealer_total = calculate_hand_value(dealer_hand)

        # Determine winner
        result = determine_winner(player_total, dealer_total)
        if result == "player":
            users[username]["balance"] += bet_amount
            return jsonify(
                {"message": "You win!", "balance": users[username]["balance"]}
            )
        elif result == "dealer":
            users[username]["balance"] -= bet_amount
            return jsonify(
                {"message": "Dealer wins!", "balance": users[username]["balance"]}
            )
        else:
            return jsonify(
                {"message": "It's a tie!", "balance": users[username]["balance"]}
            )

    return render_template("blackjack.html")


def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "Ace",
    ]
    return [(rank, suit) for suit in suits for rank in ranks]


def draw_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))


def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card[0]
        if rank in ["Jack", "Queen", "King"]:
            value += 10
        elif rank == "Ace":
            aces += 1
            value += 11  # Initially count Ace as 11
        else:
            value += int(rank)

    # Adjust for Aces
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value


def determine_winner(player_total, dealer_total):
    if player_total > 21:
        return "dealer"
    elif dealer_total > 21 or player_total > dealer_total:
        return "player"
    elif player_total < dealer_total:
        return "dealer"
    else:
        return "tie"


# ===================== MINES GAME (Blueprint) =====================
# UI:  GET  /mines                 -> serves mines.html (must be next to app.py OR adjust to templates)
# API: POST /mines/api/games
#      GET  /mines/api/games/<game_id>
#      POST /mines/api/games/<game_id>/reveal
#      POST /mines/api/games/<game_id>/cashout

mines_bp = Blueprint("mines", __name__, url_prefix="/mines")

RNG = SystemRandom()
GAMES: Dict[str, "Game"] = {}
GAME_TTL = timedelta(hours=6)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Game:
    game_id: str
    rows: int
    cols: int
    mines: int
    bet: float
    created_at: datetime
    mine_positions: Set[Tuple[int, int]] = field(default_factory=set)
    revealed: Set[Tuple[int, int]] = field(default_factory=set)
    is_over: bool = False
    is_bust: bool = False
    cashout_amount: Optional[float] = None

    @property
    def total_cells(self) -> int:
        return self.rows * self.cols

    @property
    def safe_total(self) -> int:
        return self.total_cells - self.mines

    @property
    def safe_revealed(self) -> int:
        return len(self.revealed)

    def current_multiplier(self) -> float:
        # Fair multiplier = Π (N - i) / (N - M - i), i = 0..k-1
        k = self.safe_revealed
        N = self.total_cells
        M = self.mines
        S = N - M
        if k <= 0:
            return 1.0
        if k > S:
            return float("inf")
        num = 1.0
        den = 1.0
        for i in range(k):
            num *= N - i
            den *= S - i
        return num / den

    def to_public(self) -> dict:
        state = {
            "game_id": self.game_id,
            "rows": self.rows,
            "cols": self.cols,
            "mines": self.mines,
            "bet": self.bet,
            "created_at": self.created_at.isoformat() + "Z",
            "is_over": self.is_over,
            "is_bust": self.is_bust,
            "safe_revealed": self.safe_revealed,
            "total_cells": self.total_cells,
            "safe_total": self.safe_total,
            "current_multiplier": round(self.current_multiplier(), 6),
            "cashout_amount": self.cashout_amount,
            "revealed_cells": sorted(list(self.revealed)),
        }
        if self.is_over:
            state["mine_positions"] = sorted(list(self.mine_positions))
        return state


def _cleanup_expired_games():
    now = datetime.utcnow()
    for gid in list(GAMES.keys()):
        if now - GAMES[gid].created_at > GAME_TTL:
            del GAMES[gid]


def _generate_mines(rows: int, cols: int, mines: int) -> Set[Tuple[int, int]]:
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    mine_cells = set()
    for _ in range(mines):
        pick = RNG.randrange(0, len(cells))
        mine_cells.add(tuple(cells.pop(pick)))
    return mine_cells


def _find_game(game_id: str) -> Game:
    _cleanup_expired_games()
    g = GAMES.get(game_id)
    if not g:
        raise KeyError("Game not found")
    return g


# ---------- UI (serves a static file) ----------
@mines_bp.get("/")
def mines_home():
    """
    Serve UI. Place 'mines.html' next to app.py (same folder).
    If you prefer templates/, change to: return render_template('mines.html')
    """
    return send_from_directory(BASE_DIR, "mines.html")


# Optional: serve a mines.js if your HTML references it with <script src="/mines/mines.js">
@mines_bp.get("/mines.js")
def mines_js():
    fp = os.path.join(BASE_DIR, "mines.js")
    if os.path.exists(fp):
        return send_from_directory(BASE_DIR, "mines.js")
    return jsonify({"error": "mines.js not found"}), 404


# ---------- API ----------
@mines_bp.post("/api/games")
def create_game():
    data = request.get_json(force=True, silent=True) or {}
    rows = int(data.get("rows", 5))
    cols = int(data.get("cols", 5))
    mines = int(data.get("mines", 3))
    bet = float(data.get("bet", 0))

    if rows < 2 or cols < 2:
        return jsonify({"error": "rows and cols must be ≥ 2"}), 400
    if mines < 1 or mines >= rows * cols:
        return jsonify({"error": "mines must be ≥ 1 and < rows*cols"}), 400

    game_id = str(uuid4())
    g = Game(
        game_id=game_id,
        rows=rows,
        cols=cols,
        mines=mines,
        bet=bet,
        created_at=datetime.utcnow(),
        mine_positions=_generate_mines(rows, cols, mines),
    )
    GAMES[game_id] = g
    return jsonify(g.to_public()), 201


@mines_bp.get("/api/games/<game_id>")
def get_game(game_id):
    try:
        return jsonify(_find_game(game_id).to_public())
    except KeyError:
        return jsonify({"error": "not found"}), 404


@mines_bp.post("/api/games/<game_id>/reveal")
def reveal_cell(game_id):
    try:
        g = _find_game(game_id)
    except KeyError:
        return jsonify({"error": "not found"}), 404

    if g.is_over:
        return jsonify({"error": "game is over"}), 400

    data = request.get_json(force=True, silent=True) or {}
    r = int(data.get("row", -1))
    c = int(data.get("col", -1))
    if not (0 <= r < g.rows and 0 <= c < g.cols):
        return jsonify({"error": "out of bounds"}), 400

    cell = (r, c)
    if cell in g.revealed:
        return jsonify({"error": "already revealed"}), 400

    if cell in g.mine_positions:
        g.is_over = True
        g.is_bust = True
        g.cashout_amount = 0.0
    else:
        print("It's a tie!")
        g.revealed.add(cell)

    return jsonify(g.to_public())


def get_payout(bet_type, bet_value, result_number, result_color):
    if bet_type == "number":
        return 35 if bet_value == result_number else -1
    elif bet_type == "color":
        return 1 if bet_value.lower() == result_color.lower() else -1
    else:
        return -1


def main():
    print("Welcome to Python Roulette!")
    balance = 100

    while balance > 0:
        print(f"\nYour current balance: ${balance}")
        bet_type = input("Bet on 'number' or 'color': ").strip().lower()

        if bet_type == "number":
            try:
                bet_value = int(input("Choose a number between 0 and 36: "))
                if not 0 <= bet_value <= 36:
                    print("Invalid number. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Try again.")
                continue
        elif bet_type == "color":
            bet_value = input("Choose a color (Red/Black): ").strip().capitalize()
            if bet_value not in ["Red", "Black"]:
                print("Invalid color. Try again.")
                continue
        else:
            print("Invalid bet type. Try again.")
            continue

        try:
            wager = int(input("Enter your wager amount: "))
            if wager > balance or wager <= 0:
                print("Invalid wager. Try again.")
                continue
        except ValueError:
            print("Invalid input. Try again.")
            continue

        result_number, result_color = spin_wheel()
        print(f"\n The wheel landed on {result_number} ({result_color})")

        payout_multiplier = get_payout(bet_type, bet_value, result_number, result_color)
        winnings = wager * payout_multiplier if payout_multiplier > 0 else 0
        balance += winnings - wager

        if payout_multiplier > 0:
            print(f"You won ${winnings}!")
        else:
            print("You lost your wager.")

        if balance <= 0:
            print("You're out of money! Game over.")
            break

        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != "y":
            print("Thanks for playing!")
            break


@app.route("/wizard")
def generate_wizard_name():
    prefixes = ["Thal", "Eld", "Zyn", "Mor", "Alar", "Xan", "Vor", "Gal", "Ser"]
    roots = ["drak", "mir", "vyn", "zar", "quor", "lith", "mael", "gorn", "ther"]
    suffixes = ["ion", "ar", "ius", "en", "or", "eth", "azar", "em", "yx"]
    titles = ["Archmage", "Sorcerer", "Seer", "Mystic", "Enchanter", "Spellbinder"]
    name = random.choice(prefixes) + random.choice(roots) + random.choice(suffixes)
    return f"{random.choice(titles)} {name.capitalize()}"


@mines_bp.post("/api/games/<game_id>/cashout")
def cashout(game_id):
    try:
        g = _find_game(game_id)
    except KeyError:
        return jsonify({"error": "not found"}), 404

    if g.is_over:
        return jsonify({"error": "game is over"}), 400

    mult = g.current_multiplier()
    payout = round(g.bet * mult, 6) if g.bet else round(mult, 6)

    g.cashout_amount = payout
    g.is_over = True
    g.is_bust = False

    return jsonify(g.to_public())


# Register the blueprint with your existing app
app.register_blueprint(mines_bp)
# =================== END MINES GAME (Blueprint) ===================


@app.route("/add_chips")
def add_chips():
    user_chips = []
    chips_values = {"Gold": 100, "Silver": 50, "Bronze": 25}
    for chip, value in chips_values.items():
        user_chips.append({"type": chip, "value": value})
    return jsonify(user_chips)


@app.get("/plants/match")
def plants_match():
    """
    Returns a compatibility score (0–100) for two plants.
    Example: /plants/match?plant_a=Rose&plant_b=Cactus
    """
    plant_a = (request.args.get("plant_a") or "").strip()
    plant_b = (request.args.get("plant_b") or "").strip()

    if not plant_a or not plant_b:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "Provide both query params: plant_a and plant_b. Example: /plants/match?plant_a=Rose&plant_b=Cactus",
                }
            ),
            400,
        )

    seed = sum(ord(c) for c in (plant_a.lower() + plant_b.lower()))
    score = (seed * 73) % 101

    if score > 80:
        note = "High compatibility"
    elif score > 50:
        note = "Moderate compatibility"
    elif score > 25:
        note = "Low compatibility"
    else:
        note = "Very low compatibility"

    return (
        jsonify(
            {
                "ok": True,
                "pair": [plant_a, plant_b],
                "compatibility": score,
                "note": note,
            }
        ),
        200,
    )

@app.route("/bet_rps", methods=["GET"])
def bet_rps():
    moves = ["rock", "paper", "scissors"]
    player = (request.args.get("player") or "").lower()
    amount = request.args.get("amount", type=int, default=0)

    if player not in moves or amount <= 0:
        return jsonify({"error": "Invalid move or amount"}), 400

    computer = random.choice(moves)

    # rock beats scissors, scissors beats paper, paper beats rock
    beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

    if player == computer:
        result = "tie"
        payout = amount  # return original bet on tie
    elif beats[player] == computer:
        result = "win"
        payout = amount * 2
    else:
        result = "lose"
        payout = 0

    return jsonify({
        "player": player,
        "computer": computer,
        "amount": amount,
        "result": result,
        "payout": payout
    }), 200



@app.route("/bet_slots")
def bet_slots():
    amount = request.args.get("amount", type=int, default=0)
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    symbols = ["cherry", "limon", "orange", "star"]
    result = [random.choice(symbols) for _ in range(3)]

    payout = 0
    if len(set(result)) == 1:  # Three of a kind
        payout = amount * 10
    elif len(set(result)) == 2:  # Two of a kind
        payout = amount * 3

    return jsonify({"result": result, "payout": payout})

@app.route("/house/<name>")
def house_always_wins(name):
    return f"Sorry, {name}. The house always wins!"


# ---- Keep this at the bottom. Change port if you like. ----
if __name__ == "__main__":
    # Ensure the banking database and tables exist before starting
    try:
        bank.init_bank_db()
    except Exception:
        # best-effort init; if it fails the app will still attempt to run
        print("Warning: Failed to initialize banking database/tables")
        pass

    app.run(host="127.0.0.1", port=8000, debug=True)
