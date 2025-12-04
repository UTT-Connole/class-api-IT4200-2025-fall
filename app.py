from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    jsonify,
    send_from_directory,
    redirect,
    Blueprint,
    send_file
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
from flask_cors import CORS

def create_app():

    app = Flask(__name__) 
    app.register_blueprint(bank_bp)

    @app.route("/")
    def home():
        return render_template("index.html"), 200

    @app.route("/pokemon")
    def pokemon():
        return jsonify({"pokemon": "Jigglypuff"})

    @app.route("/high_low", methods=["GET"])
    def high_low():
        guess = (request.args.get("guess") or "").lower()

        if guess not in ["higher", "lower"]:
            return jsonify({"error": "Guess must be 'higher' or 'lower'"}), 400

        cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        values = {r: i + 2 for i, r in enumerate(cards)}

        first = random.choice(cards)
        second = random.choice(cards)

        if first == second:
            outcome = "lose"
        elif (guess == "higher" and values[second] > values[first]) or (
            guess == "lower" and values[second] < values[first]
        ):
            outcome = "win"
        else:
            outcome = "lose"

        return jsonify({
            "first_card": first,
            "second_card": second,
            "guess": guess,
            "outcome": outcome
        }), 200

    @app.get("/system-info")
    def system_info():
        import platform, socket, shutil, multiprocessing

        
        try:
            du = shutil.disk_usage("/")
            disk_total_gb = round(du.total / (1024**3), 2)
            disk_free_gb = round(du.free / (1024**3), 2)
        except Exception:
            disk_total_gb = disk_free_gb = None

        info = {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "cpu_count": multiprocessing.cpu_count(),
            "disk_total_gb": disk_total_gb,
            "disk_free_gb": disk_free_gb
            }

        return jsonify(info), 200
    
    @app.route('/music')
    def play_m4a():
        audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "wip.m4a")
        return send_file(audio_path, mimetype='audio/mp4')

    @app.route('/gatcha')
    def gatcha():
        rarities = ['C', 'R', 'SR', 'SSR']
        weights = [70, 20, 9, 1]
        
        pool = [
            {"name": "A rock", "rarity": "C", "weight": 70},
            {"name": "A stick", "rarity": "R", "weight": 20},
            {"name": "A diamond", "rarity": "SR", "weight": 9},
            {"name": "A unicorn", "rarity": "SSR", "weight": 1},
        ]
        
       
        pulled_rarity = random.choices(rarities, weights=weights, k=1)[0]
        pulled_item = next(item for item in pool if item["rarity"] == pulled_rarity)
        
        return jsonify({
            "pool": pool, 
            "rarities": rarities, 
            "weights": weights,
            "last_pull": pulled_item
        })

    @app.route("/api/coinflip", methods=["POST"])
    def coinflip():
        """Flip a coin and bet on heads or tails."""
        data = request.get_json()
        choice = (data.get("choice") or "").lower()
        bet = float(data.get("bet", 0))

        if choice not in ["heads", "tails"]:
            return jsonify({"error": "Choice must be 'heads' or 'tails'"}), 400
        if bet <= 0:
            return jsonify({"error": "Bet must be greater than zero"}), 400

        result = random.choice(["heads", "tails"])
        win = result == choice
        winnings = bet * 2 if win else 0

        return jsonify({
            "choice": choice,
            "result": result,
            "outcome": "win" if win else "lose",
            "winnings": winnings
        })


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
        unique_count = len(set(result))

      
        probabilities = {
            "yahtzee": 0.0007716,     
            "four_kind": 0.01929,      
            "full_house": 0.03858,    
            "three_kind": 0.15432,     
            "two_pairs": 0.23148,     
            "one_pair": 0.46296,       
            "all_different": 0.09259  
        }
        
        message = "No special combination."
        rarity = round(probabilities["all_different"] * 100, 3) 
        
        if unique_count == 1:
            message = "Yatzy! All five dice match."
            rarity = round(probabilities["yahtzee"] * 100, 3)
        elif unique_count == 2:
            counts = [result.count(x) for x in set(result)]
            if 4 in counts:
                message = "Four of a kind!"
                rarity = round(probabilities["four_kind"] * 100, 3)
            else:
                message = "Full House! Three of a kind and a pair."
                rarity = round(probabilities["full_house"] * 100, 3)
        elif unique_count == 3:
            counts = [result.count(x) for x in set(result)]
            if 3 in counts:
                message = "Three of a kind!"
                rarity = round(probabilities["three_kind"] * 100, 3)
            else:
                message = "Two pairs!"
                rarity = round(probabilities["two_pairs"] * 100, 3)
        elif unique_count == 4:
            message = "One pair!"
            rarity = round(probabilities["one_pair"] * 100, 3)
        else:
            message = "No special combination."
            rarity = round(probabilities["all_different"] * 100, 3)

        return jsonify({
            "stats": {
                "dice_rolls": result,
                "total": sum(result),
                "max_roll": max(result),
            },
            "summary": message,
            "rarity": f"{rarity}%"
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
        data = request.get_json(silent=True) or {}
        try:
            bet = float(data.get("bet", 0))
        except (TypeError, ValueError):
            return jsonify({"error": "Bet must be a number"}), 400

        if bet <= 0:
            return jsonify({"error": "Bet must be greater than zero"}), 400

        try:
            multiplier = float(data.get("payout_multiplier", 2))
        except (TypeError, ValueError):
            return jsonify({"error": "payout_multiplier must be a number"}), 400
        if multiplier <= 1:
            return jsonify({"error": "payout_multiplier must be greater than 1"}), 400

        force = (data.get("force_result") or "").strip().lower()
        if force not in ("", "win", "lose"):
            return jsonify({"error": "force_result must be 'win' or 'lose'"}), 400

        if force:
            did_win = (force == "win")
        else:
            did_win = random.choice([True, False])

        result = "win" if did_win else "lose"
        winnings = bet * multiplier if did_win else 0

        return jsonify({
            "result": result,
            "original_bet": bet,
            "winnings": winnings,
            "multiplier": multiplier
        }), 200
   
    @app.route('/drawCard', methods=['GET'])
    def drawCard():
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        card = {
            "rank": random.choice(ranks),
            "suit": random.choice(suits)
        }
        return jsonify(card)

    @app.get('/pokerHandRankings')
    def getpokerHandRankings():
        with open('./import_resources/pokerHandRankings.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)


    @app.route("/sports", methods=["GET", "POST"])
    def sports():
        nfl_afc_teams = [
            "Bills", "Dolphins", "Patriots", "Jets",
            "Ravens", "Bengals", "Browns", "Steelers",
            "Texans", "Colts", "Jaguars", "Titans",
            "Broncos", "Chiefs", "Raiders", "Chargers"
        ]

        nfl_nfc_teams = [
            "Cowboys", "Giants", "Eagles", "Commanders",
            "Bears", "Lions", "Packers", "Vikings",
            "Falcons", "Panthers", "Saints", "Buccaneers",
            "Cardinals", "Rams", "49ers", "Seahawks"
        ]

        nba_east_teams = [
            "Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavaliers",
            "Heat", "Bucks", "Knicks", "Magic", "76ers", "Raptors",
            "Wizards", "Pacers", "Pistons", "Hawks"
        ]

        nba_west_teams = [
            "Mavericks", "Nuggets", "Warriors", "Rockets", "Clippers", "Lakers",
            "Grizzlies", "Timberwolves", "Pelicans", "Thunder", "Suns",
            "Trail Blazers", "Kings", "Spurs", "Jazz"
        ]

        league = request.args.get("league") or request.form.get("league") or "NFL"
        conference = request.args.get("conference") or request.form.get("conference")

        if league.upper() == "NBA":
            if conference and conference.upper() == "EAST":
                league_teams = nba_east_teams
            elif conference and conference.upper() == "WEST":
                league_teams = nba_west_teams
            else:
                league_teams = nba_east_teams + nba_west_teams
        else:
            if conference and conference.upper() == "AFC":
                league_teams = nfl_afc_teams
            elif conference and conference.upper() == "NFC":
                league_teams = nfl_nfc_teams
            else:
                league_teams = nfl_afc_teams + nfl_nfc_teams

        if request.method == "GET" and request.args.get("reset") == "true":
            team1, team2 = random.sample(league_teams, 2)
            winner = random.choice([team1, team2])
            return render_template("sports.html", team1=team1, team2=team2, winner=winner, bet=None, won_bet=None, league=league, conference=conference)

        if request.method == "GET":
            team1, team2 = random.sample(league_teams, 2)
            winner = random.choice([team1, team2])
            return render_template("sports.html", team1=team1, team2=team2, winner=winner, bet=None, won_bet=None, league=league, conference=conference)

        team1 = (request.form.get("team1") or "").strip()
        team2 = (request.form.get("team2") or "").strip()
        winner = (request.form.get("winner") or "").strip()

        if not team1 or not team2 or team1 not in league_teams or team2 not in league_teams or team1 == team2:
            team1, team2 = random.sample(league_teams, 2)
            winner = random.choice([team1, team2])

        bet = (request.form.get("bet") or "").strip()
        if not bet:
            won_bet = None
        elif bet.lower() not in (team1.lower(), team2.lower()):
            won_bet = "Invalid bet"
        else:
            won_bet = bet.lower() == winner.lower()

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
            league=league,
            conference=conference,
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

       
        scores = {}
        for name, stats in chickens.items():
            score = (
                stats["speed"] * random.uniform(0.8, 1.2) +
                stats["stamina"] * random.uniform(0.8, 1.2) +
                stats["luck"] * random.uniform(0.8, 1.2)
            )
            scores[name] = score
        winner = max(scores, key=scores.get)

       
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

    @app.route("/race/stats", methods=["GET"])
    def chicken_stats():
        chickens = {
            "Colonel Sanders Revenge": {"speed": 7, "stamina": 6, "luck": 4},
            "McNugget Sprint": {"speed": 8, "stamina": 5, "luck": 6},
            "Free Range Fury": {"speed": 6, "stamina": 8, "luck": 5},
            "Scrambled Lightning": {"speed": 9, "stamina": 4, "luck": 7},
            "Hen Solo": {"speed": 7, "stamina": 7, "luck": 5},
            "Clucky Balboa": {"speed": 6, "stamina": 9, "luck": 3},
            "Cluck Norris": {"speed": 9, "stamina": 6, "luck": 8},
            "Eggward Scissorbeak": {"speed": 8, "stamina": 6, "luck": 6},
        }

        total = len(chickens)
        avg_speed = sum(c["speed"] for c in chickens.values()) / total
        avg_stamina = sum(c["stamina"] for c in chickens.values()) / total
        avg_luck = sum(c["luck"] for c in chickens.values()) / total

        top_speed = max(chickens, key=lambda c: chickens[c]["speed"])
        top_stamina = max(chickens, key=lambda c: chickens[c]["stamina"])
        top_luck = max(chickens, key=lambda c: chickens[c]["luck"])
        best_payout = max(chickens, key=lambda c: eval(chickens[c]["odds"]) if "odds" in chickens[c] else 0)

        predicted_winner = max(chickens, key=lambda c: chickens[c]["speed"] + chickens[c]["stamina"] + chickens[c]["luck"])

        stats = {
            "total_chickens": total,
            "average_speed": round(avg_speed, 2),
            "average_stamina": round(avg_stamina, 2),
            "average_luck": round(avg_luck, 2),
            "top_speed": top_speed,
            "top_stamina": top_stamina,
            "top_luck": top_luck,
            "best_payout": best_payout,
            "predicted_winner": predicted_winner
        }

        return render_template("racestats.html", stats=stats)

    @app.route("/slots", methods=["POST"])
    def slots():
        symbols = ["CHERRY", "LEMON", "BELL", "STAR", "7"]
        bet = request.json.get("bet", 1)
        username = request.json.get("username", "user1")

        if bet <= 0:
            return jsonify({"error": "Bet must be positive."}), 400

        if username not in users or users[username]["balance"] < bet:
            return jsonify({"error": "Insufficient balance or user not found."}), 400

        
        result = [random.choice(symbols) for _ in range(3)]

       
        if result.count(result[0]) == 3:
            payout = bet * 10  
            message = "Jackpot! All symbols match."
        elif len(set(result)) == 2:
            payout = bet * 2 
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

    @app.route("/five_card_stud")
    def five_card_stud():  
        def make_deck():
            deck = []
            for i in range(52):
                suit = i // 13
                rank = i % 13
                deck.append((suit, rank))
            return deck

        def deal_hand(deck):
            hand = random.sample(deck, 5)
            hand.sort(key=lambda card: card[1])
            return hand

        def get_values(hand):
            return [card[1] for card in hand]

        def is_flush(hand):
            suits = [card[0] for card in hand]
            return len(set(suits)) == 1 

        def is_straight(hand):
            card_values = get_values(hand)
            if card_values == [0, 9, 10, 11, 12]:
                return True    
            for i in range(4):
                if card_values[i + 1] != (card_values[i] + 1):
                    return False
            return True

        def count(hand):
            card_values = get_values(hand)
            counts = {}
            for value in card_values:
                counts[value] = counts.get(value, 0) + 1
            return counts

        def pairs_kinds(hand):
            counts = count(hand)
            count_values = list(counts.values())
            count_values.sort(reverse=True)
            pair = count_values.count(2)
            three = count_values.count(3)
            four = count_values.count(4)
            return pair, three, four

        def check_hand(hand):
            pair, three, four = pairs_kinds(hand)
            flush = is_flush(hand)
            straight = is_straight(hand)
            ranks = get_values(hand)

            if flush and ranks == [0, 9, 10, 11, 12]:
                return "Royal Flush"
            if flush and straight:
                return "Straight Flush"
            if four == 1:
                return "Four of a Kind"
            if three == 1 and pair == 1:
                return "Full House"
            if flush:
                return "Flush"
            if straight:
                return "Straight"
            if three == 1:
                return "Three of a Kind"
            if pair == 2:
                return "Two Pair"
            if pair == 1:
                return "Pair"
            return "High Card"
    
        deck = make_deck()
        return jsonify(check_hand(deal_hand(deck)))


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
           
            if rule.endpoint == "static":
                continue
           
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
        
        rarity_bonus = 0
        if plant_stats[chosen_plant]["rarity"] == "Rare" and won:
            rarity_bonus = int(bet * 0.5) 
            winnings += rarity_bonus

        chosen_stats = plant_stats[chosen_plant]
        winner_stats = plant_stats[winner]

        if chosen_plant == winner:
            message = f"{chosen_plant} basked in radiant sunlight and triumphed gloriously!"
        else:
            if chosen_stats["attack"] > winner_stats["attack"]:
                message = f"{chosen_plant} fought valiantly but eventually wilted in defeat."
            else:
                message = f"{chosen_plant} was overwhelmed by {winner}'s ferocity!"

        environment = random.choice(["Greenhouse", "Jungle", "Desert", "Swamp", "Backyard"])
        weather = random_weather()

        return jsonify({
            "plants": plants,
            "chosen_plant": chosen_plant,
            "winner": winner,
            "bet": bet,
            "result": "win" if won else "lose",
            "winnings": winnings,
            "message": message,
            "battle_environment": environment,
            "weather": weather["condition"],
            "chosen_stats": chosen_stats,
            "winner_stats": winner_stats,
        })

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
            {"title": "Vibrations", "artist": "Peach Fur", "genre": "Reggae Rock", "year": 2015}
        ]

        genre_filter = request.args.get("genre")
        if genre_filter:
            filtered = [s for s in songs if s["genre"].lower() == genre_filter.lower()]
            if not filtered:
                return jsonify({"success": False, "error": "No songs found for that genre"}), 404
            songs = filtered

        year_filter = request.args.get("year")
        if year_filter:
            try:
                year_filter = int(year_filter)
            except ValueError:
                return jsonify({"success": False, "error": "Year must be a number"}), 400

            filtered = [s for s in songs if s["year"] == year_filter]
            if not filtered:
                return jsonify({"success": False, "error": "No songs found for that year"}), 404
            songs = filtered

        song = random.choice(songs)
        return jsonify({"success": True, "song": song})
    
    @app.route("/add_chips")
    def add_chips():
        user_chips = []
        chips_values = {"Gold": 100, "Silver": 50, "Bronze": 25}
        for chip, value in chips_values.items():
            user_chips.append({"type": chip, "value": value})
        return jsonify(user_chips)
    
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
    
    return app  



app = create_app()  



_started = time.time()

@app.get("/api/ping")
def ping():
    now = time.time()
    return jsonify({
        "status": "ok",
        "uptime_ms": int((now - _started) * 1000)
    }), 200



@app.route("/random-weather")
def random_weather():
    conditions = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]
    condition = random.choice(conditions)
    temperature = f"{random.randint(-30, 50)}C"
    humidity = f"{random.randint(10, 100)}%"
    weather = {"condition": condition, "temperature": temperature, "humidity": humidity}
    return weather

@app.route("/hazardous-conditions")
def hazardous_conditions():
    weather_data = random_weather()
    
    condition = weather_data["condition"]
    temperature = int(weather_data["temperature"].replace("C", ""))
    humidity = int(weather_data["humidity"].replace("%", ""))

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

    hazardous_conditions = {
        "condition": condition,
        "temperature": weather_data["temperature"],
        "humidity": weather_data["humidity"],
        "hazardous_condition": hazard,
        "severity": severity,
        }
    return hazardous_conditions

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



def extract_teams(results):
    teams = set()
    for result in results:
        parts = result.split(" - ")
        team1_info = parts[0].rsplit(" ", 1)[0]  
        team2_info = parts[1].split(" ", 1)[1]   
        teams.add(team1_info)
        teams.add(team2_info)
    return teams

@app.route("/hockey_teams", methods=['GET'])
def get_teams():
    all_teams = extract_teams(hockey_results1).union(extract_teams(hockey_results2))
    return jsonify({"teams": sorted(list(all_teams))})



@app.route("/hockey_matchup", methods=["GET"])
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



users = {
    "alice": {"balance": 100},
    "bob": {"balance": 50},
}
bets = []

@app.route("/stats/mean", methods=["GET"])
def stats_mean():
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

    digits = request.args.get("round", type=int)
    if digits is not None:
        if digits < 0 or digits > 10:
            return jsonify({"error": "round must be between 0 and 10"}), 400
        mean_val = round(mean_val, digits)

    return jsonify({"mean": mean_val}), 200



@app.route("/plants/match", methods=["POST"])
def place_plant_bet():
    data = request.get_json()
    username = data.get("username")
    plant_id = data.get("plant_id")
    amount = data.get("amount")


    if username not in users:
        return jsonify({"error": "User not found"}), 404
    if users[username]["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

   
    plants = {
        1: {"name": "Rose", "value": 100},
        2: {"name": "Tulip", "value": 50},
        3: {"name": "Cactus", "value": 30},
    }

    if plant_id not in plants:
        return jsonify({"error": "Invalid plant ID"}), 400

    
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




@app.route("/generatePassword", methods=["GET"])
def generatePassword():
    Length = request.args.get("Length", 12)
    Complexity = request.args.get("Complexity", "simple")

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
 
    return (y * 5) + x

@app.route("/bingo/check", methods=["POST"])
def check_bingo():
    data = request.get_json()
    card = data.get("card")

    if not card or len(card) != 25:
        return jsonify({"error": "Invalid card"}), 400

    
    r = 0
    for i in range(5):
        rows = [r,r+1,r+2,r+3,r+4]
        row_bingo = True
        for j in rows:
            if card[j]['marked'] == False:
                row_bingo = False
        if row_bingo == True:
            return jsonify({"bingo": True}), 200
        r += 5
        
    
    c = 0
    for i in range(5):
        columns = [c,c+5,c+10,c+15,c+20]
        column_bingo = True
        for j in columns:
            if card[j]['marked'] == False:
                column_bingo = False
        if column_bingo == True:
            return jsonify({"bingo": True}), 200
        c += 1
        
    
    down_diagonal = [0,6,12,18,24]
    down_bingo = True
    up_diagonal = [4,8,12,16,20]
    up_bingo = True
    
    for i in down_diagonal:
        if card[i]['marked'] == False:
            down_bingo = False
    if down_bingo == True:
        return jsonify({"bingo": True}), 200
    
    for i in up_diagonal:
        if card[i]['marked'] == False:
            up_bingo = False
    if up_bingo == True:
        return jsonify({"bingo": True}), 200

    return jsonify({"bingo": False}), 200


@app.route('/double_or_nothing', methods=['GET'])
def double_or_nothing():
    amount = request.args.get('amount', default=None, type=float)
    if amount is None or amount <= 0:
        return jsonify({
            "error": "You must bet a positive number amount, e.g. /double_or_nothing?amount=50"
        }), 400

    result = random.choice(["win", "lose"])
    if result == "win":
        new_balance = amount * 2
        message = random.choice([
            "You doubled it! Luck is on your side (for now).",
            "Winner winner, chicken dinner!",
            "You actually won? The odds tremble before you!"
        ])
    else:
        new_balance = 0
        message = random.choice([
            "Oof. You lost everything. Again.",
            "The house always wins.",
            "Better luck next refresh."
        ])

    return jsonify({
        "bet": amount,
        "outcome": result,
        "new_balance": new_balance,
        "message": message
    })

def generate_minesweeper_grid(difficulty):
    if difficulty == 'beginner':
        rows = 9
        columns = 9
        mines = 10
    elif difficulty == 'intermediate':
        rows = 16
        columns = 16
        mines = 40
    elif difficulty == 'expert':
        rows = 16
        columns = 30
        mines = 99
    else:
        return 'Error: invalid difficulty argument. Use "beginner", "intermediate", or "expert" difficulty'
    
    grid = [[0 for _ in range(columns)] for _ in range(rows)]

    mine_positions = set()
    while len(mine_positions) < mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, columns - 1)
        mine_positions.add((r, c))

    for (r, c) in mine_positions:
        grid[r][c] = -1

    for (r, c) in mine_positions:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if (dr == 0 and dc == 0) or not (0 <= nr < rows and 0 <= nc < columns):
                    continue
                if grid[nr][nc] != -1:
                    grid[nr][nc] += 1
    return grid

@app.route("/minesweeper", methods=['GET'])
def minesweeper_grid():
    difficulty = request.args.get('difficulty', default='expert')
    return jsonify({"grid":generate_minesweeper_grid(difficulty)})


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


@app.route("/random_pokemon")
def random_pokemon():
    a = random.randint(1, 1010)
    print(f"Redirecting to Pokémon ID: {a}")
    return redirect((f"https://www.pokemon.com/us/pokedex/{a}")), 302





@app.route('/roulette', methods=['GET'])
def roulette():
    """
    GET /roulette
      Optional query params:
        - force_spin: int(0..36) for deterministic spin (useful in tests)
        - bet: 'red' | 'black' | 'green' | '0'..'36'
        - amount: positive integer wager

      Always returns base spin result. If bet/amount provided, also returns outcome and payout.
    """
    force_spin = request.args.get("force_spin", type=int)
    if force_spin is not None:
        if force_spin < 0 or force_spin > 36:
            return jsonify({"error": "force_spin must be between 0 and 36"}), 400
        spin = force_spin
    else:
        numbers = list(range(0, 37))  
        spin = random.choice(numbers)

    red_set = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    if spin == 0:
        color = 'green'
    else:
        if force_spin is not None:
            color = 'red' if spin in red_set else 'black'
        else:
            color = 'green' if spin == 0 else random.choice(['red', 'black'])

    result = {
        "spin": spin,
        "color": color,
        "parity": "even" if spin != 0 and spin % 2 == 0 else "odd" if spin % 2 == 1 else "none"
    }

    bet = request.args.get("bet")
    amount = request.args.get("amount", type=int)

    if bet is None and amount is None:
        return jsonify(result), 200

    if bet is None or amount is None:
        return jsonify({"error": "bet and amount are both required when betting"}), 400
    if amount <= 0:
        return jsonify({"error": "amount must be a positive integer"}), 400

    bet = bet.strip().lower()
    payout = 0
    outcome = "lose"

    if bet in {"red", "black", "green"}:
        if bet == color:
            if bet in {"red", "black"}:
                payout = amount * 2     
            else:
                payout = amount * 35    
            outcome = "win"
    else:
        try:
            bet_num = int(bet)
            if 0 <= bet_num <= 36:
                if bet_num == spin:
                    payout = amount * 35
                    outcome = "win"
            else:
                return jsonify({"error": "number bet must be between 0 and 36"}), 400
        except ValueError:
            return jsonify({"error": "bet must be 'red'|'black'|'green' or integer 0..36"}), 400

    result.update({
        "bet": bet,
        "amount": amount,
        "outcome": outcome,
        "payout": payout
    })
    return jsonify(result), 200



@app.route("/russian-roulette", methods=["GET"])
def russian_roulette():
    chambers = 6
    bullet_chamber = random.randrange(chambers)  
    fired_chamber = random.randrange(chambers)  
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
    unlivable_homes = [generate_unlivable_home() for _ in range(random.randint(3, 6))]
    message = {
        "location": "Hellhole",
        "description": "Hellhole is a great place to visit... if you're into nightmares.",
        "fact": random.choice(hellhole_facts),
        "unlivable_homes": unlivable_homes,
        "timestamp": str(datetime.now()) + "Z",
    }
    return jsonify(message)




@app.route("/blackjack", methods=["GET", "POST"])
def blackjack():
    if request.method == "POST":
        data = request.get_json()
        bet_amount = data.get("bet_amount")
        username = data.get("username")

        if username not in users or users[username]["balance"] < bet_amount:
            return jsonify({"error": "Insufficient balance or user not found."}), 400

        deck = create_deck()
        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        player_total = calculate_hand_value(player_hand)
        dealer_total = calculate_hand_value(dealer_hand)

        while player_total < 21:
            action = data.get("action")  
            if action == "hit":
                player_hand.append(draw_card(deck))
                player_total = calculate_hand_value(player_hand)
            elif action == "stand":
                break

        while dealer_total < 17:
            dealer_hand.append(draw_card(deck))
            dealer_total = calculate_hand_value(dealer_hand)

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
            value += 11  
        else:
            value += int(rank)


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




mines_bp = Blueprint("mines", __name__, url_prefix="/mines")

CORS(mines_bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

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


@mines_bp.get("/")
def mines_home():
    """
    Serve UI. Place 'mines.html' next to app.py (same folder).
    If you prefer templates/, change to: return render_template('mines.html')
    """
    return send_from_directory(BASE_DIR, "templates/mines.html")


@mines_bp.get("/mines.js")
def mines_js():
    fp = os.path.join(BASE_DIR, "js/mines.js")
    if os.path.exists(fp):
        return send_from_directory(BASE_DIR, "js/mines.js")
    return jsonify({"error": "mines.js not found"}), 404


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


app.register_blueprint(mines_bp)

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

    beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

    if player == computer:
        result = "tie"
        payout = amount  
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



 
@app.route("/house/<name>")
def house_always_wins(name):
    return f"Sorry, {name}. The house always wins!"

@app.get("/color")
def color():
    """Return either 'black' or 'red' at random."""
    choice = random.choice(["black", "red"])
    return jsonify({"color": choice}), 200

@app.route("/stats/median", methods=["GET"])
def stats_median():
    raw = request.args.get("vals", "")
    if not raw:
        return jsonify({"error": "missing vals"}), 400
    try:
        nums = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
    except ValueError:
        return jsonify({"error": "vals must be comma-separated numbers"}), 400
    if not nums:
        return jsonify({"error": "no numeric values provided"}), 400

    nums.sort()
    n = len(nums)
    mid = n // 2
    if n % 2 == 1:
        med = nums[mid]
    else:
        med = (nums[mid - 1] + nums[mid]) / 2.0

    return jsonify({"median": med}), 200

@app.route("print")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    try:
        bank.init_bank_db()
    except Exception:
        print("Warning: Failed to initialize banking database/tables")
        pass

    app.run(host="127.0.0.1", port=8000, debug=True)
