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

@app.route("/print")
def hello_world():
    return "Hello, Beebo!"

if __name__ == "__main__":
    try:
        bank.init_bank_db()
    except Exception:
        print("Warning: Failed to initialize banking database/tables")
        pass

    app.run(host="127.0.0.1", port=8000, debug=True)
    
# pylint: disable=useless-suppression
# KUNG FU PANDA
#
#
#
# Written By
#
# Jonathan Aibel & Glenn Berger
#
#
#
#
# FINAL DRAFT
# June 3, 2008
#
# 1.
#
#
# EXT. VALLEY -- DAY
#
# A MYSTERIOUS WARRIOR treks across the rugged landscape.
#
# NARRATOR (V.O.)
# Legend tells of a legendary warrior
# whose Kung Fu skills were the stuff
# of legend.
#
# The warrior, his identity hidden beneath his flowing robe and
# wide-brimmed hat, gnaws on a staff of bamboo.
#
# NARRATOR (V.O.) (CONT'D)
# He traveled the land in search of
# worthy foes.
#
# CUT TO:
#
#
# INT. BAR
#
# The warrior sits at a table drinking tea and gnawing on his
# bamboo. The door BLASTS open. The MANCHU GANG rushes in and
# surrounds him.
#
# GANG BOSS
# (to warrior)
# I see you like to CHEW!
# (beat)
# Maybe you should chew on my FIST!!
#
# The Boss punches the table.
#
# NARRATOR (V.O.)
# The warrior said nothing for his
# mouth was full. Then, he swallowed.
#
# He swallows.
#
# NARRATOR (V.O.) (CONT'D)
# And then, he spoke.
#
# WARRIOR
# (dubbed hero voice)
# Enough talk. Let's FIGHT!
# SHASHABOOEY!
#
# WHAM! The warrior delivers a punch and the whole gang goes
# flying.
#
# NARRATOR (V.O.)
# He was so deadly in fact that his
# enemies would go blind from
# overexposure to pure awesomeness.
#
# 2.
#
#
# The gang members blindly flail about.
#
# NINJA CAT
# MY EYES!
#
# GATOR
# HE'S TOO AWESOME!
#
# ONLOOKERS swoon.
#
# SMITTEN BUNNY
# And ATTRACTIVE!
#
# GRATEFUL BUNNY
# How can we repay you??
#
# WARRIOR
# There is no charge for awesomeness,
# or attractiveness.
#
# ONE HUNDRED ASSASSINS appear and surround the warrior.
#
# CUT TO:
#
#
# EXT. BAR - CONTINUOUS
#
# The entire bar swells, packed to the rafters with ninjas.
#
# WARRIOR
# KABLOOEY!
#
# CUT TO:
#
#
# EXT. BAR - CONTINUOUS
#
# The roof EXPLODES and a cloud of ninjas erupts into the sky.
# Like a tornado, the warrior spins and knocks them all down.
#
# NARRATOR (V.O.)
# It mattered not how many foes he
# faced. They were no match for his
# bodacity.
#
# The warrior beats up a thousand ninjas, delivering his final
# blow while doing a split between two trees.
#
# The warrior stands amongst a field of vanquished foes as god-
# rays shine down upon him.
#
# NARRATOR (V.O.) (CONT'D)
# Never before had a panda been so
# feared... and so loved.
# (MORE)
#
# 3.
# NARRATOR (V.O.) (CONT'D)
# Even the most heroic heroes in all
# of China, the Furious Five, bowed
# in respect to this great master.
#
# MONKEY
# We should hang out.
#
# WARRIOR
# Agreed.
#
# As the Five salute the warrior, he turns to see more bandits
# approaching. The Five strike an attack pose. The warrior
# brandishes a shiny green sword and leaps off the mountain
# into the sea of bandits.
#
# NARRATOR (V.O.)
# But hanging out would have to wait.
# `Cause when you're facing the ten
# thousand demons of Demon Mountain,
# there's only one thing that
# matters. And that's--
#
# In mid air, the Five talk to the warrior in a strange voice.
#
# MONKEY
# Po! Get up!
#
# TIGRESS
# You'll be late for work!
#
# PO
# Whu?
#
#
# INT. PO'S ROOM - DAY
#
# Po lands hard on the floor. He tries to clear his head and
# wake up.
#
# PO'S DAD (O.S.)
# Po! Get up!
#
# We see his room is filled with various kung fu posters
# (including a poster featuring all of the Five) and souvenirs,
# and a wooden version of the Sword of Heroes (the green
# sword).
#
# Po SIGHS.
#
# He attempts to kick himself to his feet but alas, his belly
# is too worthy a foe.
#
# PO'S DAD (O.S.) (CONT'D)
# Po! What are you doing up there?
#
# 4.
#
#
# PO
# Uh, nothing!
#
# Po hops to his feet, imitating his Kung Fu action figures.
#
# PO (CONT'D)
# Monkey! Mantis! Crane! Viper!
# Tigress! Rowrrrr...
#
# OUTSIDE on the balcony of the neighboring house, a pig
# watering flowers stares at Po. Po tries to play it cool and
# then quickly ducks out of sight.
#
# PO'S DAD (O.S.)
# Po! Let's go! You're late for work!
#
# PO
# Coming!
#
# He takes a ninja star from his floor and chucks it at the
# wall. It bounces off.
#
# He throws the star again, but it bounces off again. He picks
# it up and heads downstairs. He trips and falls the rest of
# the way.
#
#
# INT. KITCHEN - DAY
#
# Po falls flat on his face on the kitchen floor. A panda-
# shaped shadow looms over Po.
#
# PO
# Sorry, Dad.
#
# PO'S DAD
# Sorry doesn't make the noodles.
#
# Reveal that the shadow is actually caused by a basket being
# carried by a small DUCK. This is PO'S DAD. Po gets to work,
# which is not easy since the kitchen's not really made for a
# panda his size.
#
# PO'S DAD (CONT'D)
# What were you doing up there? All
# that noise.
#
# PO
# Oh, nothing. Just had a crazy
# dream.
#
# He gets back to work.
#
# 5.
#
#
# PO'S DAD
# About what?
#
# PO
# Huh?
#
# PO'S DAD
# The dream. What were you dreaming
# about?
#
# PO
# What was I... eh, I was dreaming
# about uh... heh...
#
# Push in on Po -- is he going to admit his dream? He hides his
# throwing star behind his back.
#
# PO (CONT'D)
# Noodles.
#
# THOK. Dad stops chopping vegetables.
#
# PO'S DAD
# Noodles. You were really dreaming
# about noodles?
#
# PO
# Uh, yeah. What else would I be
# dreaming about?
#
# Po hands a noodle bowl to a customer, then realizes his
# throwing star is sitting in it.
#
# PO (CONT'D)
# (to customer)
# Careful, that soup is... sharp!
#
# PO'S DAD
# Oh, happy day! My son, finally
# having the noodle dream!
#
# He throws his arms around Po.
#
# PO'S DAD (CONT'D)
# You don't know how long I have been
# waiting for this moment.
#
# When Dad pulls out of the hug, Po is now wearing a noodle
# apron.
#
# PO'S DAD (CONT'D)
# This is a sign, Po!
#
# 6.
#
#
# Po looks at the apron nervously -- what has he gotten himself
# into?
#
# PO
# Uh...a sign of what?
#
# PO'S DAD
# You are almost ready to be
# entrusted with the secret
# ingredient of my "Secret Ingredient
# Soup." And then you will fulfill
# your destiny and take over the
# restaurant, just as I took it over
# from my father, who took it over
# from his father, who won it from a
# friend in a game of mahjong.
#
# PO
# Dad Dad Dad, it was just a dream.
#
# PO'S DAD
# No, it was the dream. We are noodle
# folk. Broth runs through our veins.
#
# PO
# But Dad, didn't you ever, I dunno,
# want to do something else?
# Something besides noodles?
#
# PO'S DAD
# Actually...
#
# Po looks surprised.
#
# PO'S DAD (CONT'D)
# When I was young and crazy...
#
# Dad gets a wistful look in his eyes.
#
# PO'S DAD (CONT'D)
# I thought about running away and
# learning how to make tofu.
#
# PO
# So why didn't you?!
#
# PO'S DAD
# Oh, because it was a stupid dream.
# Can you imagine, me making tofu?
# (laughs at the thought)
# No. We all have our place in this
# world. Mine is here. And yours is--
#
# 7.
#
#
# PO
# I know. Is here.
#
# PO'S DAD
# No, it's at tables two, five,
# seven, and twelve.
#
# He loads Po's arms with bowls of soup.
#
# PO'S DAD (CONT'D)
# Service with a smile!
#
# A GONG sounds in the distance. Po looks out the window at the
# distant JADE PALACE.
#
#
# EXT. JADE PALACE - DAY
#
# SLAM ZOOM in towards Palace.
#
# End next to palace on an old red panda (SHIFU) playing a
# FLUTE. He is surrounded by the bushes and trees that nestle
# between the Palace buildings.
#
# Wider: We dolly around from behind the bushes. Stealthy dark
# shapes move in the foreground.
#
# Back on Shifu, still playing. He seems oblivious.
#
# Five figures explode from the undergrowth simultaneously,
# diving on Shifu.
#
# Shifu moves like lightning - the flute now wielded like a
# staff - he deflects, blocks, dodges, parries - the attackers
# go flying -
#
# They roll and pick themselves up, turning to face Shifu, who
# is now standing - poised - ready for their next move.
#
# SHIFU
# Well done, students... if you were
# trying to disappoint me.
#
# He uses his flute to correct the Five's technique.
#
# SHIFU (CONT'D)
# Tigress, you need more ferocity.
# Monkey, greater speed.
#
# Each of the Five bows respectfully as their name is
# mentioned.
#
# 8.
#
#
# SHIFU (CONT'D)
# Crane - height. Viper - subtlety.
# Mantis--
#
# Shifu suddenly points the flute at a scared PALACE GOOSE.
#
# ZENG
# Master Shifu!
#
# SHIFU
# (impatiently)
# What?!
#
# ZENG
# (startled)
# Aah! It's Master Oogway. He wants
# to see you.
#
# Shifu looks up, concerned.
#
#
# INT. HALLWAY
#
# Shifu strides purposefully down the hallway, which is lined
# with palace geese.
#
#
# INT. SCROLL ROOM - DAY
#
# Candles, incense, and smoke fill the room. The door bursts
# open, the candles flicker. Shifu enters.
#
# SHIFU
# Master Oogway? You summoned me.
#
# He bows. Then looks up without unbowing.
#
# SHIFU (CONT'D)
# Is something wrong?
#
# Reveal Master Oogway... a wise, old tortoise.
#
# OOGWAY
# Why must something be wrong for me
# to want to see my old friend?
#
# SHIFU
# So... nothing's wrong?
#
# OOGWAY
# Well, I didn't say that.
#
# Shifu looks up, concerned. Oogway opens his mouth... and
# blows out a candle. And another candle. And another.
#
# 9.
#
#
# Finally, Shifu uses his Kung Fu to blow them all out. Oogway
# smiles knowingly.
#
# SHIFU
# You were saying?
#
# OOGWAY
# I have had a vision... Tai Lung
# will return.
#
# Shifu looks stricken.
#
#
# FLASHBACK - INT. SCROLL ROOM
#
# Quick, impressionistic images of Shifu battling a large,
# shadowy figure (Tai Lung).
#
#
# PRESENT - INT. SCROLL ROOM
#
# Shifu is rattled. He looks at the claw marks that still scar
# the wall and quickly looks away. But he regains his
# composure.
#
# SHIFU
# That is impossible. He is in
# prison.
#
# OOGWAY
# Nothing is impossible.
#
# Shifu makes a split decision.
#
# SHIFU
# Zeng!
#
# He comes flying in. Shifu gets in his face.
#
# SHIFU (CONT'D)
# Fly to Chogun Prison and tell them
# to double the guards, double their
# weapons. Double everything! Tai
# Lung does not leave that prison!
#
# ZENG
# Yes, Master Shifu.
#
# The goose flies off, but... SMACK! He hits a column. Then he
# is off. Back on Oogway, as he walks toward camera, away from
# Shifu.
#
# 10.
#
#
# OOGWAY
# One often meets his destiny on the
# road he takes to avoid it.
#
# SHIFU
# We have to do something. We can't
# just let him march on the valley,
# and take his revenge! He'll, he'll--
#
# Oogway looks into the water of the moon pool.
#
# OOGWAY
# Your mind is like this water, my
# friend. When it is agitated, it
# becomes difficult to see. But if
# you allow it to settle, the answer
# becomes clear.
#
# Shifu and Oogway stare into the pool. Oogway settles the
# water, revealing the reflection of an intricately carved
# dragon clutching a SCROLL in its mouth.
#
# SHIFU
# The Dragon Scroll...
#
# OOGWAY
# It is time.
#
# SHIFU
# But who? Who is worthy to be
# trusted with the secret to
# limitless power? To become...the
# Dragon Warrior?!
#
# Dramatic music as we push in on Oogway's face. Then...
#
# OOGWAY
# I don't know.
#
#
# INT. NOODLE SHOP - DAY
#
# Po is serving customers, but has trouble squeezing between
# tables.
#
# PO
# Oop...sorry.
#
# ANGRY PATRON
# Hey! Watch it, Po!
#
# PO
# Sorry. Suck it up.
#
# 11.
#
#
# He sucks his belly in, but this causes his butt to interfere
# with a bunny family's meal.
#
# DISGUSTED PATRON
# Ugh!
#
# PO
# Oop! Sorry! A thousand pardons.
#
# A couple palace geese put up a poster on the wall and a
# palace pig hits a tiny gong. This gets Po's attention. He
# rushes up to the poster.
#
# PO (CONT'D)
# What?! Master Oogway's choosing the
# Dragon Warrior! Today!
#
# Customers jump up excitedly.
#
# PO (CONT'D)
# Everyone! Everyone! Go! Get to the
# Jade Palace!
#
# Po urges the villagers out the restaurant.
#
# PO (CONT'D)
# One of the Five is gonna get the
# Dragon Scroll!
#
# Customers rush to finish their food.
#
# PO (CONT'D)
# We've been waiting a thousand years
# for this! Just take the bowl!
#
# Other customers are finishing their soup.
#
# One old lady customer slowly counts out coins and puts them
# on the table.
#
# PO (CONT'D)
# This is the greatest day in Kung Fu
# history! Don't worry about it, just
# go!
#
# He starts to run.
#
# PO'S DAD
# Po! Where are you going?
#
# Po stops dead in his tracks, busted.
#
# PO
# To the...Jade Palace?
#
# 12.
#
#
# PO'S DAD
# But you're forgetting your noodle
# cart! The whole valley will be
# there, and you'll sell noodles to
# all of them.
#
# PO
# Selling noodles? But Dad, you know,
# I was kinda thinking maybe I...
#
# PO'S DAD
# Yeah?
#
# PO
# I was kinda thinking maybe I...
#
# PO'S DAD
# Uh huh?
#
# Po wants to say something to his dad, but he loses his nerve.
#
# PO
# ...Could also sell the bean buns.
# They are about to go bad.
#
# PO'S DAD
# That's my boy! I told you that
# dream was a sign!
#
# PO
# Yeah, ha ha, glad I had it.
#
#
# EXT. VALLEY SQUARE - DAY
#
# Throngs of Villagers are streaming into the arena. A couple
# BUNNY KIDS run by.
#
# BUNNY FAN #1
# Yippee!
#
# BUNNY FAN #2
# I'm a Kung Fu warrior!
#
# BUNNY FAN #1
# Me too!
#
# Where's Po?
#
# PAN DOWN a long, long, long, long flight of stairs. Po stands
# at the bottom with his noodle cart, looking up at the
# daunting task before him.
#
# Po struggles to pull his noodle cart up the stairs.
#
# 13.
#
#
# The sun beats down on Po, but he presses forward. Climbing.
# Climbing.
#
# DISSOLVE TO:
#
#
# EXT. VALLEY SQUARE - LATER
#
# Po is still struggling up the stairs.
#
# PO
# Come on! Come on, ya-- Almost
# there...
#
# He stops, flopping onto his back to catch his breath.
#
# WIDEN TO REVEAL he's only made it up seven steps.
#
# PO (CONT'D)
# What? No! Oh No!
#
# Two Pigs pass by.
#
# KG SHAW
# Sorry, Po.
#
# JR SHAW
# We'll bring you back a souvenir.
#
# Po watches as they run up the stairs. His eyes narrow. This
# is his heroic moment.
#
# PO
# No. I'll bring me back a souvenir.
#
# Po tosses off his hat and apron and begins his ascent up the
# stairs.
#
#
# EXT. JADE PALACE - ARENA PLATFORM
#
# Oogway reaches the bottom of the palace stairs and a Palace
# Pig bangs a gong.
#
# SHIFU
# It is an historic day, isn't it,
# Master Oogway?
#
# OOGWAY
# Yes, and one I feared I would not
# live to see. Are your students
# ready?
#
# 14.
#
#
# SHIFU
# Yes, Master Oogway.
#
# OOGWAY
# Now know this, old friend. Whomever
# I choose will not only bring peace
# to the Valley, but also to you.
#
# As Shifu contemplates what this could mean, Oogway starts
# walking off. Shifu quickly joins Oogway as they head towards
# the roaring crowd below. The pig bangs the gong.
#
# ANNOUNCER
# Let the tournament begin!
#
#
# EXT. VALLEY SQUARE - DAY
#
# Throngs of Villagers are streaming into the arena.
#
#
# EXT. TOP OF STAIRS - DAY
#
# Po gasps for air as he hoists himself over the last step,
# laughing victoriously.
#
# PO
# (out of breath)
# Yeah!
#
# The doors to the palace arena begin to close.
#
# PO (CONT'D)
# Oh no! No no no! Wait! I'm coming!
#
# Po runs to the entrance and proceeds to bang on the door.
#
# PO (CONT'D)
# Hey! Open the door!
#
# DRUMS inside drown out Po's pounding. He yells.
#
# PO (CONT'D)
# Let me in!
#
# Inside, spectators' screams drown out Po's yelling.
#
# Po panics for a beat and then finds a window. He jumps and
# weakly struggles to pull himself up.
#
# Po struggles to peek through the window.
#
# 15.
#
#
# INT. PALACE ARENA - CONTINUOUS
#
# SHIFU
# Citizens of the Valley of Peace! It
# is my great honor to present to
# you... Tigress! Viper! Crane!
# Monkey! Mantis! The Furious Five!
#
# The Five jump into the middle of the ring.
#
# PO
# The Furious Five!
#
# Po manages a brief glimpse of the Five before a gust of wind
# knocks Po to the ground and shuts the window.
#
# SHIFU
# Warriors prepare!
#
# Po runs over to a crack in the wall.
#
# PO
# Peeky-hole!
#
# SHIFU
# Ready for battle!
#
# Inside the arena, Po catches a glimpse of Crane as he spreads
# his wings.
#
# PO
# Yeah! Woo! The Thousand Tongues of
# Fire!
#
# One of the spectators walks in front of Po, cutting off his
# view.
#
# PIG FAN
# Whoa! Look at that.
#
# PO
# Hey, get out of the way!
#
# Po backs up to get a better look at Crane in the sky and
# accidentally falls down the stairs.
#
# Po climbs back up and drops his head -- he missed it.
#
# MONTAGE:
#
# Po tries karate chopping the door open...to no avail. He
# slumps to the ground.
#
# 16.
#
#
# PO (CONT'D)
# Ow...
#
# Po attempts a pole vault, but falls on his back. The pole
# whips around and hits him into the arena wall.
#
# Po rigs a catapult, only to get clobbered by it. The crowd
# CHEERS.
#
# Po sits atop the stairs. Alone.
#
# SHIFU
# And finally...Master Tigress!
#
# Po snaps to attention.
#
# Po pulls on a rope tied to a tree.
#
# SHIFU (O.S.) (CONT'D)
# And believe me citizens, you have
# not seen anything yet!
#
# PO
# I KNOW!!
#
# SHIFU (O.S.)
# Master Tigress! Face Iron Ox and
# his Blades of Death!
#
# Tigress sets up to deliver her move.
#
# Po launches himself up above the fence, gets a peek at
# Tigress, then falls out of view just as she does her move.
#
# Po lands outside the arena in a fireworks tent.
#
#
# INT. TOURNAMENT RING - DAY
#
# Oogway senses something. He raises his hand and the crowd
# hushes.
#
# OOGWAY
# I sense the Dragon Warrior is among
# us.
#
# Shifu motions for the Five to gather in the center of the
# ring.
#
# SHIFU
# Citizens of the Valley of Peace!
# Master Oogway will now choose...
# the Dragon Warrior!
#
# 17.
#
#
# EXT. TOURNAMENT RING - DAY
#
# Po comes to.
#
# PO
# Huh? Oh no! Wait!
#
# He sees the fireworks and has an idea.
#
# PO (CONT'D)
# Yeah!
#
#
# INT. TOURNAMENT RING - DAY
#
# Oogway closes his eyes and raises his hand as ceremonial
# DRUMS start to play.
#
#
# EXT. TOURNAMENT RING - DAY
#
# Po struggles with something, his back turned to us. Reveal he
# has tied a load of fireworks to a chair. He hops on and
# lights the fuse.
#
# PO'S DAD (O.S.)
# Po?!
#
# Po's Dad rushes over and tries to blow out the fuse.
#
# PO'S DAD (CONT'D)
# What are you doing?
#
# PO
# What does it look like I'm doing?
# Stop! Stop! I'm going to see the
# Dragon Warrior!
#
# PO'S DAD
# But I don't understand. You finally
# had the noodle dream.
#
# Po looks uneasy.
#
# PO
# I lied. I don't dream about
# noodles, Dad!
#
# He looks at the fuse... almost all gone... Po holds onto the
# chair for dear life, closes his eyes, and braces himself for
# liftoff.
#
# PO (CONT'D)
# I love kung fuuuuuuuuuuuuuuuuu-
#
# 18.
#
#
# Po finally opens his eyes...
#
# He's still on the ground. The fuse was a dud. Po falls face
# first into the dirt. He looks away, embarrassed. Po's Dad
# holds out his apron.
#
# PO'S DAD
# Come on, son. Let's get back to
# work.
#
# PO
# Okay.
#
# Po sighs, starts to reach for the apron, then-- BOOM! The
# rockets ignite, propelling Po into the stadium wall.
#
# PO'S DAD
# Oh! Come back!
#
# Po's rocket chair blasts him into the sky amid a shower of
# fireworks.
#
# CROWD
# Oooh! Aaahh!
#
# Po climbs up and up...until the rockets die out and the chair
# loses power...
#
# PO
# Uh oh...
#
# Oogway's arm sweeps down the line of the expectant Five... Po
# falls towards the center of the ring...
#
# The tension builds as the Five wait to see who will be
# picked. Then... SMASH!
#
# Po lands and kicks up a huge dirt cloud, obscuring the ring.
#
#
# INT. ARENA
#
# PO POV: He sees the Five looking down at him, appalled. Po
# comes round slowly, getting his bearings. He looks around and
# sees Oogway. Strangely, the old turtle is smiling.
#
# PO
# What's going on? Where...uh? What
# are you pointing--?
#
# He looks up. An awful realization starts to dawn. Po GULPS.
# He is desperately embarrassed.
#
# 19.
#
#
# PO (CONT'D)
# Oh. Okay. Sorry. I just wanted to
# see who the Dragon Warrior was.
#
# He tries to shuffle his butt out of there, mumbling
# apologies.
#
# OOGWAY
# How interesting.
#
# TIGRESS
# Master, are you pointing at...me?
#
# OOGWAY
# Him.
#
# PO
# Who--?
#
# Po tries moving out of the way of Oogway's finger, but it
# keeps following him.
#
# OOGWAY
# You.
#
# PO
# Me?
#
# Oogway grabs Po's hand and holds it up for all to see.
#
# OOGWAY
# The universe has brought us the
# Dragon Warrior!
#
# QUICK CUTS:
#
# PO
# What?
#
# FURIOUS FIVE
# What??
#
# SHIFU
# What???
#
# PO'S DAD
# WHAT????
#
# The pig bangs the gong.
#
# The crowd goes wild! They cheer! They scream! Confetti falls!
# A palanquin is carried past Shifu.
#
# 20.
#
#
# SHIFU
# Stop! Wait! Who told you to--?
#
# Po stands there, utterly stunned, his mouth hanging open. He
# is abruptly lifted up out of shot.
#
# Cut to the Palace Geese straining.
#
# Po is being lifted with great effort on the palanquin. He is
# carried off. Shifu elbows his way urgently through the
# thronging crowd to get to Oogway.
#
# SHIFU (CONT'D)
# Master Oogway, wait! That flabby
# panda can't possibly be the answer
# to... our problem. You were about
# to point at Tigress. That thing
# fell in front of her. That was just
# an accident!
#
# OOGWAY
# There are no accidents.
#
# Oogway smiles benignly as we hear an off-screen CRASH!
#
# The camera adjusts to reveal the palanquin has collapsed
# under Po.
#
# Shifu looks at Oogway. Oogway just smiles.
#
# A squad of burly pigs rushes in and hoists Po, the palanquin,
# and the Geese onto their shoulders, and they head off for the
# Jade Palace. Stunned, Shifu watches them go.
#
# Behind him, the Five approach and bow.
#
# TIGRESS
# Forgive us, Master. We have failed
# you.
#
# Shifu spins around.
#
# SHIFU
# No. If the panda has not quit by
# morning, then I will have failed
# you.
#
# Confetti flutters through the air as the celebration
# continues around them.
#
# CUT TO:
#
# 21.
#
#
# EXT. PRISON -- NIGHT
#
# A huge prison is carved into the side of a frozen mountain.
# Fifteen stories of iron and rock. No windows. One door --
# locked, bolted and sealed tight. Rhinoceros guards in armor
# patrol the perimeter.
#
# Zeng, the palace goose, flies into frame and a Rhino Sentry
# spots him in the distance. He lands, sliding on the ice and
# crashing into the gate. The rhinos point their spears at him.
#
# ZENG
# Wait wait wait! I bring a message
# from Master Shifu.
#
# CLANG! The doors creak open. The terrified goose peers in.
#
# CUT TO:
#
#
# INT. PRISON -- A MOMENT LATER
#
# COMMANDER
# What?!?!
# (reading)
# "Double the guard?! Extra
# precautions?! Your prison may not
# be adequate!"
#
# The Goose is quaking in fear. Stern Rhinos surround him,
# staring daggers at him. The Commander snaps the scroll shut.
#
# COMMANDER (CONT'D)
# You doubt my prison's security?
#
# ZENG
# Absolutely not.
# (then)
# Shifu does. I'm just the messenger.
#
# COMMANDER
# I'll give you a message for your
# Master Shifu.
#
#
# ON A BRIDGE
#
# COMMANDER
# Escape from Chogun Prison is
# impossible!
#
# The Goose is awed by the cavernous prison.
#
# 22.
#
#
# ZENG
# Whoa.
#
# The goose looks over the bridge's edge. The prison goes down
# a long ways. The commander hits the goose on the back.
#
# COMMANDER
# Impressive, isn't it?
#
# A feather from the goose drifts down the prison.
#
# ZENG
# Yes, very impressive. It's VERY
# impressive.
#
# COMMANDER
# One way in, one way out, one
# thousand guards, and one prisoner.
#
# ZENG
# Yes, except that prisoner is Tai
# Lung...
#
#
# AT THE ELEVATOR
#
# COMMANDER
# Take us down.
#
# Several guard rhinos winch the goose and the commander down.
# The commander grabs the chain and shakes the elevator, trying
# to scare the goose.
#
# ZENG
# What are you doing?!
#
# The commander just laughs. The elevator finally lands,
# sending an echo throughout the prison.
#
# AT DOORS -
#
# A number of doors unlock, one after the other. Finally, a
# drawbridge is lowered out onto an island.
#
# ZENG (CONT'D)
# Oh my...
#
# COMMANDER
# Behold, Tai Lung.
#
# ZENG
# I'll um...I'm just gonna wait right
# here.
#
# 23.
#
#
# COMMANDER
# It's nothing to worry about. It's
# perfectly safe.
#
# He shoves the goose out ahead of him.
#
# ZENG
# Oof!
#
# COMMANDER
# Crossbows! At the ready!
#
# ZENG
# Crossbows?!
#
# They approach TAI LUNG, a giant, muscular snow leopard bound
# in a giant piece of tortoise shell armor and chains. He
# barely registers signs of life. The commander walks right up
# to him.
#
# COMMANDER
# Hey, tough guy, did you hear?
# Oogway's finally gonna give someone
# the Dragon Scroll and it's not
# gonna be you!
#
# The goose can't believe it.
#
# ZENG
# What are you doing?! Don't get him
# mad.
#
# COMMANDER
# What's he gonna do about it? I've
# got him completely immobilized.
#
# The Commander stomps on Tai Lung's tail. We hear a crunch.
# The goose flinches. But Tai Lung does not react.
#
# COMMANDER (CONT'D)
# Awww. Did I step on the witty
# kitty's tail? Awww.
#
# Tai Lung doesn't move. His eyes stare coldly straight ahead.
#
# ZENG
# I'm good. I've seen enough. I'm
# gonna tell Shifu he's got nothing
# to worry about.
#
# COMMANDER
# No, he doesn't.
#
# 24.
#
#
# ZENG
# Okay, I'll tell him that. Can we
# please go now?
#
# The Commander starts to walk back to the elevator. The goose
# hurries after him.
#
# The goose's feather flutters into frame. We follow the
# feather as it lands right in front of Tai Lung.
#
# HIS EYES OPEN. Tai Lung grabs the feather with his tail.
#
#
# INT. JADE PALACE - HALLWAY
#
# The palace doors open to reveal Po on the palanquin, hundreds
# of villagers behind him.
#
# CROWD
# (chanting)
# Dragon Warrior! Dragon Warrior!
#
# Po is ushered in and the doors close. He is alone. He runs
# back to the closed palace doors.
#
# PO
# Wait a second! Hello? Uh...I think
# there's been a slight mistake.
# Everyone seems to think that I'm,
# uh...
#
# Po finally realizes where he is.
#
# PO (CONT'D)
# Whoa. The Sacred Hall of Warriors.
# No way! Would you look at this
# place!
#
# He rushes up to a display of armor.
#
# PO (CONT'D)
# (GASP)
# Master Flying Rhino's Armor! With
# authentic battle damage!
#
# He rushes up to a green sword, making sure not to touch it.
#
# PO (CONT'D)
# (GASP)
# The Sword of Heroes! Said to be so
# sharp you can cut yourself just by
# looking-- OW!
#
# He stares at a black sopt on the wall.
#
# 25.
#
#
# PO (CONT'D)
# (GASP)
# The Invisible Trident of Destiny!?
#
# He admires a painting.
#
# PO (CONT'D)
# (GASP)
# I've only seen paintings of that
# painting...
#
# Po runs around the room, amazed by all the ancient kung fu
# artifacts. Something special catches Po's eye.
#
# PO (CONT'D)
# (loudly)
# Nooo! Ohhhh!
#
# He runs over to it.
#
# PO (CONT'D)
# The legendary Urn of Whispering
# Warriors! Said to contain the souls
# of the entire Tenshu army.
# (calling into vase)
# Hellooo?
#
# SHIFU
# Have you finished sight-seeing?
#
# Po GASPS.
#
# PO
# (to vase)
# Sorry. I should've come to see you
# first.
#
# SHIFU
# My patience is wearing thin.
#
# PO
# (to vase)
# Oh. Well, I mean, it's not like you
# were going anywhere.
#
# SHIFU
# Would you turn around?
#
# PO
# Sure.
#
# Po turns and sees Shifu.
#
# 26.
#
#
# PO (CONT'D)
# Hey, how's it going?
#
# Po turns back to the vase.
#
# PO (CONT'D)
# (to vase)
# Now how do you get five thousand--
# (cutting himself off)
# Master Shifu!
#
# Po bumps the vase which falls and BREAKS.
#
# PO (CONT'D)
# Someone...broke that. But I'm gonna
# fix it. Do you have some glue?
#
# The vase debris screams as Po tries to pick up the pieces.
#
# PO (CONT'D)
# Ow! Ooh. Splinter.
#
# Po fumbles around. Shifu looks irked.
#
# SHIFU
# So you're the legendary Dragon
# Warrior. Hmmm?
#
# PO
# Uh...I guess so?
#
# Shifu smiles and shakes his head.
#
# SHIFU
# Wrong! You are not the Dragon
# Warrior. You will never be the
# Dragon Warrior until you have
# learned the secret of the Dragon
# Scroll.
#
# He points to a dragon on the ceiling with a single scroll in
# its mouth.
#
# PO
# (in awe)
# Whoa.
# (then)
# So how does this work? You have a
# ladder or trampoline or...?
#
# SHIFU
# You think it's that easy? That I am
# just going to hand you the secret
# to limitless power?
#
# 27.
#
#
# PO
# No, I...
#
# SHIFU
# One must first master the highest
# level of kung fu. And that is
# clearly impossible if that one is
# someone like you.
#
# PO
# Someone like me?
#
# Shifu walks around Po - pointing out his weaknesses.
#
# SHIFU
# Yes. Look at you...this fat butt.
#
# Shifu HITS Po on the butt with his staff.
#
# SHIFU (CONT'D)
# Flabby arms...
#
# PO
# Those are sensitive in the flabby
# parts.
#
# Shifu SWATS Po on the arm with his staff.
#
# SHIFU
# And this ridiculous belly.
#
# Shifu HITS Po in the belly with his staff.
#
# PO
# Hey...
#
# SHIFU
# --and utter disregard for personal
# hygiene.
#
# PO
# (pointing at Shifu)
# Now wait a minute. That's a little
# uncalled-for.
#
# SHIFU
# Don't stand that close...I can
# smell your breath.
#
# PO
# Listen...Oogway said that I was the-
#
# Shifu pinches Po's outstretched digit.
#
# 28.
#
#
# PO (CONT'D)
# (gasp)
# The Wuxi Finger Hold?! Not the Wuxi
# Finger Hold!
#
# SHIFU
# (sly)
# Oh, you know this hold?
#
# PO
# DevelopedbyMasterWuxiInTheThirdDyna
# sty-- YES.
#
# SHIFU
# Oh, then you must know what happens
# when I flex my pinky.
#
# Po nervously eyes his finger locked in Shifu's grip and nods
# quickly.
#
# PO
# No no no!
#
# SHIFU
# You know the hardest part of this?
# The hardest part is cleaning up
# afterwards...
#
# PO
# Okay! Okay! Take it easy...
#
# SHIFU
# Now listen closely, panda. Oogway
# may have picked you, but when I'm
# through with you, I promise you,
# you're going to wish he hadn't. Are
# we clear?
#
# PO
# Yeah, we're clear. We're clear. We
# are so clear.
#
# SHIFU
# Good. I can't wait to get started.
#
#
# INT. TRAINING HALL
#
# The doors open, revealing Po nursing his wounded finger.
# Shifu steps out of the way and Po's face goes into shock. The
# Five are performing death-defying kung fu moves in the
# training hall. Tigress smashes a swinging, spiked ball of
# wood. ANGLE ON AN AWESTRUCK PO, as shards of wood blast into
# his face. Po is intimidated and overwhelmed.
#
# 29.
#
#
# Shifu scowls at Po.
#
# SHIFU
# Let's begin.
#
# He gestures to the gauntlet. Po's eyes go wide.
#
# PO
# Wait wait wait...What? Now?
#
# SHIFU
# Yes...now. Unless you think the
# great Oogway was wrong, and you are
# not the Dragon Warrior.
#
# PO
# Oh, okay. Well-- I don't know if I
# can do all of those moves.
#
# Shifu walks away and Po half-heartedly follows.
#
# SHIFU
# Well, if we don't try, we'll never
# know will we?
#
# PO
# Uh, yeah. It's just, maybe we can
# find something more suited to my
# level.
#
# SHIFU
# And what level is that?
#
# PO
# Well, ya know...I'm not a master,
# but uh, let's just start at zero,
# level zero.
#
# SHIFU
# There is no such thing as level
# zero.
#
# PO
# Hey! Maybe I can start with that.
#
# Po points at a rather friendly-looking dummy.
#
# SHIFU
# That? We use that for training
# children. And for propping the door
# open when it's hot. But if you
# insist...
#
# Relieved, Po turns to the dummy. The Five gather around him.
#
# 30.
#
#
# PO
# Whoa. The Furious Five. You're so
# much bigger than your action
# figures -- except for you, Mantis.
# You're about the same.
#
# Mantis gives him a look.
#
# SHIFU
# Go ahead, panda. Show us what you
# can do.
#
# PO
# Um, are they gonna watch? Or should
# I just wait until they get back to
# work or something...
#
# SHIFU
# Hit it.
#
# PO
# Ok. I mean, I just ate. So I'm
# still digesting... So my kung fu
# might not be as good as later on.
#
# SHIFU
# Just hit it.
#
# Po psyches himself up, doing some Jack Fu.
#
# PO
# Alright. Whatcha got? You got
# nothing cause I got it right here.
# You picking on my friends? Get
# ready to feel the thunder. I'm
# comin' at him with the crazy feet.
# Whatcha gonna do about my crazy
# feet? I'm a blur. I'm a blur. You
# never seen bear style, you only
# seen praying Mantis! OR... I could
# come at you Monkey style. OR... I'm
# comin' at ya snikity-snake.
#
# Shifu and the Five stare at Po, perplexed.
#
# SHIFU
# Would you hit it!
#
# PO
# Alright...alright.
#
# Po lightly hits the dummy and it rocks back into place.
#
# 31.
#
#
# SHIFU
# Why don't you try again?   A little
# harder...
#
# Po punches it again, knocking it all the way backwards. He
# turns to Shifu, smug.
#
# PO
# How's tha--
#
# WHAP! The dummy rights itself and smacks Po. Totally dazed,
# Po trips and stumbles his way through the obstacle course.
# The Five instinctively step forward to help Po, but Shifu
# holds up his hand to stop them.
#
#
# BACK ON PO
#
# PO (CONT'D)
# Ow, that hurts.
#
# A spiky tethered ball sends Po flying into the jade turtle
# exercise, where it rattles him around.
#
# SHIFU
# (to the Five)
# This'll be easier than I thought.
#
# Back to Po in the turtle bowl.
#
# PO
# Feeling a little nauseous.
#
# The turtle spills him out and he stumbles into the army of
# wooden dummies.
#
# PO (CONT'D)
# Ow, those are hard! Ooh! I think
# I...
#
# The last dummy whaps him in the crotch and everything becomes
# still.
#
# PO (CONT'D)
# Oooohoohoo...my tenders.
#
# He struggles to get on his feet, takes one step and reaches
# out to a dummy arm...and immediately gets pummeled all over
# again. Po comes out the other side battered and bruised and
# finds he is standing on the floor that shoots out bursts of
# flame. We see reflections of fire on the Five and Shifu as Po
# gets singed. He comes crawling into frame.
#
# 32.
#
#
# PO (CONT'D)
# How did I do?
#
# SHIFU
# There is now a level zero.
#
# CUT TO:
#
#
# EXT. BUNKHOUSE - NIGHT
#
# The Five are walking to the bunkhouse, which sits high on a
# hill.
#
# MANTIS
# There's no words.
#
# CRANE
# No denying that.
#
# VIPER
# I don't understand what Master
# Oogway was thinking. The poor guy's
# just gonna get himself killed.
#
# CRANE
# (mocking)
# He is so mighty! The Dragon Warrior
# fell out of the sky on a ball of
# fire.
#
# MANTIS
# When he walks, the very ground
# shakes!
#
# TIGRESS
# One would think that Master Oogway
# would choose someone who actually
# knew Kung Fu.
#
# CRANE
# Yeah, or could at least touch his
# toes.
#
# MONKEY
# Or even see his toes.
#
# As the others walk off, we reveal Po, who unbeknownst to them
# has been walking behind them this whole time, hearing
# everything.
#
# He attempts to look at his toes but just sees gut. He lifts
# up his stomach, leans forward... leans... leans... and falls
# over.
#
# 33.
#
#
# He gets up and watches them go inside. He sighs.
#
#
# INT. BUNKHOUSE
#
# Po peeks around the corner.
#
# PO
# Okay.
#
# He tip-toes into the hall.
#
# SQUEAK. The floorboards strain beneath him. SQUEAK.
#
# PO (CONT'D)
# (whispering)
# Great.
#
# Po takes a gentle step. CRE-E-E-A-AA--CHUNK! Po's foot goes
# through the floor. Po tries to recover. SQUEAK-SQUEAK-SQUEAK!
# THUNK! Po rolls his ankle and stumbles through a bedroom
# door.
#
# Crane is staring back at him.
#
# PO (CONT'D)
# Oh hey...hi. You're up.
#
# CRANE
# Am now.
#
# PO
# I was just uh... Some day huh?
# That kung fu stuff is hard work,
# right? Your biceps sore?
#
# Crane looks at his wing.
#
# CRANE
# Um...I've had a long and rather
# disappointing day, so uh...yeah, I
# should probably get to sleep now.
#
# PO
# Yeah yeah yeah, of course.
#
# CRANE
# (relieved)
# Okay, thanks.
#
# PO
# It's just...I'm such a big fan.
#
# 34.
#
#
# CRANE
# Oop.
#
# PO
# You guys were totally amazing at
# the Battle of Weeping River.
# Outnumbered a thousand to one, but
# you didn't stop, and then you
# just... HI-YAH!
#
# Po does a spastic series of Kung Fu moves. We hear a RIP, and
# reveal that he's kicked his foot through the paper wall.
#
# PO (CONT'D)
# Ooo, sorry about that.
#
# CRANE
# Look, you don't belong here.
#
# Po looks stung to be hearing this from one of his heroes.
#
# PO
# I know. I know. You're right. I
# just - my whole life I've dreamed
# of-
#
# Crane stops Po before he embarrasses himself even more.
#
# CRANE
# No no no... I meant you don't
# belong here. I mean, in this room.
# This is my room. Property of Crane.
#
# Po is mortified, but covers.
#
# PO
# Oh, okay. Right right. Yeah, you
# want to get to sleep.
#
# CRANE
# Yeah.
#
# PO
# I'm keepin' you up. We got big
# things tomorrow. Alright. You're
# awesome. Last thing I'm gonna say.
# Okay. Bye bye.
#
# Po shuts the door. Crane sighs. The door flies open. Po
# enters with an eager smile.
#
# PO (CONT'D)
# What was that?
#
# 35.
#
#
# CRANE
# I didn't say anything.
#
# PO
# Okay. Alright. Goodnight. Sleep
# well.
#
# Po backs out into the hall and closes the door.
#
# PO (CONT'D)
# Seemed a little bit awkward.
#
# Po turns and walks down the hall to find a vacant room. CREAK-
# CREAK.
#
# Tigress opens the door behind him. Po winces.
#
# PO (CONT'D)
# Master Tigress! Didn't mean to wake
# you. Just uh...
#
# TIGRESS
# You don't belong here.
#
# PO
# Uh, yeah, yeah. Of course. This is
# your room.
#
# TIGRESS
# I mean...you don't belong in the
# Jade Palace. You're a disgrace to
# Kung Fu, and if you have any
# respect for who we are and what we
# do, you will be gone by morning.
#
# She closes the door on Po, who slumps sadly.
#
# PO
# Big fan...
#
#
# EXT. JADE PALACE - NIGHT
#
# A dejected Po stands under a peach tree in the moonlight.
# Oogway approaches.
#
# OOGWAY
# I see you have found the Sacred
# Peach Tree of Heavenly Wisdom.
#
# Po spins around, his face dripping with peach juice.
#
# 36.
#
#
# PO
# (mouth full)
# Is that what this is? I am so
# sorry. I thought it was just a
# regular peach tree.
#
# OOGWAY
# I understand. You eat when you are
# upset.
#
# PO
# Upset? I'm not upset. What makes
# you think I'm upset?
#
# OOGWAY
# So why are you upset?
#
# Po sighs, there's no use trying to lie to Oogway.
#
# PO
# I probably sucked more today than
# anyone in the history of kung fu,
# in the history of China, in the
# history of sucking.
#
# OOGWAY
# Probably.
#
# PO
# And the Five... man, you should
# have seen them, they totally hate
# me.
#
# OOGWAY
# Totally.
#
# PO
# How's Shifu ever going to turn me
# into the Dragon Warrior? I mean,
# I'm not like The Five. I've got no
# claws, no wings, no venom. Even
# Mantis has those...
# (he imitates a mantis'
# front legs)
# ...thingies. Maybe I should just
# quit and go back to making noodles.
#
# OOGWAY
# Quit, don't quit. Noodles, don't
# noodles.
#
# Po looks confused.
#
# 37.
#
#
# OOGWAY (CONT'D)
# You are too concerned with what was
# and what will be. There is a
# saying: Yesterday is history,
# tomorrow is a mystery, but today is
# a gift. That is why it is called
# the present.
#
# Oogway hits the tree with his staff as he walks away and a
# peach falls into Po's open hand.
#
#
# INT. PRISON -- NIGHT
#
# Using the goose's feather to pick the lock, Tai Lung BURSTS
# free from his armor.
#
# An ALARM RINGS OUT!
#
# The Commander runs to the ledge, the Goose right behind him.
#
# ZENG
# What's happening?!
#
# The Goose looks over the edge and sees Tai Lung at the bottom
# of the pit.
#
# Tai Lung struggles with his shackles.
#
# COMMANDER
# Fire Crossbows!
#
# Tai Lung uses the incoming spears to break his shackles and
# then manages to kick the spears back up into the walls,
# creating a makeshift staircase.
#
# ZENG
# Tai Lung is free! I must warn
# Shifu!
#
# The Commander shuts the Goose up.
#
# COMMANDER
# You're not going anywhere. And
# neither is he.
#
# ZENG
# Let go of me!
#
# COMMANDER
# (to guards)
# Bring it up!
#
# 38.
#
#
# The winch turns and the elevator starts to rise. A rhino
# guard tries to reach it, but just misses.
#
# RHINO GUARD #1
# Wait! Bring it back!
#
# ZENG
# He's coming this way!
#
# COMMANDER
# He won't get far.
# (to guards)
# Archers!
#
# Leaping across the spears, Tai Lung catches the elevator as
# the volley of arrows flies down past him.
#
# The guards cut the rope and the elevator crashes back down to
# the bottom of the pit.
#
# Tai Lung swings up from the bottom of the elevator house and
# catches the guards by surprise. He grabs the chain and jumps
# over the edge and swings around, launching himself up to the
# next tier, disappearing into the shadows.
#
# Tai Lung lands on a bridge, fights his way through, finally
# reaching the top tier where the Commander and the rest of the
# Rhino army await.
#
# ZENG
# We're dead. So very, very dead.
#
# The Commander hushes the Goose.
#
# COMMANDER
# (to Goose)
# Heh heh...not yet we're not! Now!
#
# Archers set off charges on the ceiling. Massive stalactites
# crash down and the bridge begins to crumble. Tai Lung leaps
# across the crumbling debris and attempts one last huge jump
# towards the Commander. But he falls short, claws scraping and
# sparking against the rock wall. The Commander laughs
# maniacally.
#
# On his way down, Tai Lung looks up and sees a fuse burning
# down to the last group of explosives. He leaps across the
# raining debris up to the ceiling of the cavern.
#
# Grabbing a hold of the dynamite, Tai Lung falls and slings it
# ahead of him at the guards.
#
# ZENG
# Can we run now?
#
# 39.
#
#
# COMMANDER
# Yes.
#
#
# EXT. PRISON
#
# KA-THOOM! The door blasts open and Rhinos go flying
# everywhere.
#
# WHUMP. The Goose hits the ground. The commander's horn
# prosthetic falls in front of him.
#
# ZENG
# Nuuu... Urggg...
#
# Tai Lung picks up the Goose by the throat.
#
# ZENG (CONT'D)
# URRK!
#
# TAI LUNG
# I'm glad Shifu sent you. I was
# beginning to think I had been
# forgotten.
#
# With a creepy tenderness, Tai Lung smooths the Goose's
# ruffled feathers.
#
# TAI LUNG (CONT'D)
# Fly back there and tell them...the
# real Dragon Warrior is coming home.
#
# Tai Lung throws the Goose into the air and he flutters off.
# Lightning strikes.
#
# CUT TO:
#
#
# EXT. BUNKHOUSE - MORNING
#
# CLOSE-UP of a gong being struck.
#
#
# INT. BUNKHOUSE - CONTINUOUS
#
# Shifu enters the hallway of the bunkhouse. The Five burst out
# of their rooms and land, ready for inspection.
#
# FURIOUS FIVE
# Good morning master!
#
# One door remains closed.
#
# 40.
#
#
# SHIFU
# Panda! Panda, wake up!
#
# He slides open Po's door. The room is empty.
#
# SHIFU (CONT'D)
# (satisfied)
# Hmm. He's quit.
#
#
# EXT. TRAINING HALL - MOMENTS LATER
#
# Shifu walks with a bit more energy.
#
# VIPER
# What do we do now, Master? With the
# panda gone, who will be the Dragon
# Warrior?
#
# SHIFU
# All we can do is resume our
# training and trust that in time,
# the true Dragon Warrior will be
# revealed.
#
#
# INT. JADE PALACE - MOMENTS LATER
#
# Shifu enters the training hall, only to find himself face-to-
# face with Po's butt. Shifu and the Five are taken aback.
#
# SHIFU
# What are you doing here?!
#
# Reveal Po is in the middle of the floor, his legs spread wide
# apart. Po looks back over his shoulder to see Shifu and the
# Five enter the hall.
#
# PO
# Hey! Huh... Good morning, Master! I
# thought I'd warm up a little.
#
# SHIFU
# You're stuck.
#
# PO
# Stuck?! Whaa? Pfft... stuck...
# Yeah, I'm stuck.
#
# SHIFU
# (to Crane)
# Help him.
#
# Crane approaches Po.
#
# 41.
#
#
# CRANE
# Oh dear.
#
# Crane gingerly grabs Po's waistband and attempts to pull him
# up by flapping his wings.
#
# PO
# Maybe on three. One. Two-
#
# Crane pulls him up and Po flops onto his back.
#
# PO (CONT'D)
# Threeeee. Thank you.
#
# CRANE
# Don't mention it.
#
# PO
# No really, I appreci--
#
# CRANE
# --EVER.
#
# SHIFU
# You actually thought you could
# learn to do a full split in one
# night? It takes years to develop
# one's flexibility and years longer
# to apply it in combat.
#
# Shifu flings two boards into the air. Instantly, Tigress
# leaps up and executes a perfect split kick. Po is awestruck.
# As Tigress lands, the broken chunks of board land all around
# Po, knocking him on the head.
#
# Po collects a piece of splintered board as a souvenir. Shifu
# notices and steps forward.
#
# SHIFU (CONT'D)
# Put that down! The only souvenirs
# we collect here are bloody knuckles
# and broken bones.
#
# PO
# Yeah, excellent!
#
# He laughs excitedly and salutes Shifu.
#
# SHIFU
# Let's get started.
#
# CUT TO:
#
# 42.
#
#
# MONTAGE
#
# Shifu snaps his fingers. Viper and Po face off.
#
# VIPER
# Are you ready?
#
# PO
# I was born ready--
#
# Viper lashes her tail around Po's wrist, wrenches his arm
# back, flings him into the air and brings him crashing back
# down on his head.
#
# PO (CONT'D)
# Eaghhh...
#
# VIPER
# I'm sorry, brother! I thought you
# said you were ready!
#
# PO
# That was awesome! Let's go again.
# (salutes)
#
# Shifu snaps.
#
# Monkey twirls a bamboo staff. He lunges at Po who takes a
# comical beating.
#
# Shifu snaps.
#
# Po and Crane prepare to spar atop the turtle bowl. CRASH. Po
# falls in and is tossed around like a sack of soup.
#
# Shifu snaps.
#
# We see a series of shots of Po falling on his face at the
# hands of some invisible opponent, who turns out to be...
# Mantis.
#
# Shifu smiles. Flat on his back, Po manages a salute. Shifu
# has had it.
#
# SHIFU
# I've been taking it easy on you,
# panda, but no more! Your next
# opponent... will be me.
#
# Po looks excited.
#
# PO
# Alright! Let's go!
#
# 43.
#
#
# The Five exchange worried looks.
#
# SHIFU
# (to Po)
# Step forth.
#
# Po doesn't even finish the step as Shifu whirls him around
# and throws him to the floor pinning his arm behind him.
#
# SHIFU (CONT'D)
# The true path to victory is to find
# your opponent's weakness and make
# him suffer for it.
#
# PO
# (delighted)
# Oh, yeah!
#
# Shifu whips Po around again.
#
# SHIFU
# To take his strength and use it
# against him.
#
# Again, this time Shifu holds Po by the nose.
#
# SHIFU (CONT'D)
# --until he finally falls, or quits.
#
# Po is totally inspired.
#
# PO
# But a real warrior never quits.
# Don't worry, Master, I will never
# quit!
#
# At his breaking point, Shifu flings Po into the air and then
# leaps at him with a flying kick.
#
# CUT TO:
#
#
# EXT. TRAINING HALL - CONTINUOUS
#
# Po crashes out of the door and tumbles down the steps.
#
# The Five watch him fall.
#
# TIGRESS
# If he's smart, he won't come back
# up those steps.
#
# MONKEY
# But he will.
#
# 44.
#
#
# VIPER
# He's not gonna quit, is he?
#
# MANTIS
# He's not gonna quit bouncin', I'll
# tell ya that.
#
# Cut WIDE as Po continues to tumble.
#
#
# INT. BUNKHOUSE - EVENING
#
# Close on Po, who grimaces.
#
# PO (O.S.)
# Aaaoo...whoohoo...EEEee...hee-
# hee... I thought you said
# acupuncture would make me feel
# better.
#
# Mantis pops up from behind Po holding a handful of needles
# and sticks Po again.
#
# MANTIS
# Trust me, it will. It's just not
# easy finding the right nerve points
# under all this--
#
# PO
# Fat?
#
# MANTIS
# Fur, I was gonna say fur.
#
# PO
# Sure you were.
#
# MANTIS
# Who am I to judge a warrior based
# on his size? I mean -- look at me.
#
# Po looks for Mantis...
#
# MANTIS (O.C.) (CONT'D)
# I'm over here.
#
# ...But Mantis is now on his other shoulder. He jabs another
# needle into Po.
#
# PO
# Ow!
#
# 45.
#
#
# VIPER
# Maybe you should take a look at
# this again.
#
# Viper is holding a diagram of acupuncture meridians (onto
# which someone has overlaid a drawing of a panda.)
#
# MANTIS
# (re: diagram)
# Oh! Okay.
#
# Quick cuts to Monkey meditating in his room and Crane doing
# calligraphy in his. Po's yelps distract them.
#
# PO
# Ow! Don't...
# (laughing)
# Stop it, stop-- Yow! I know Master
# Shifu's trying to inspire me and
# all, but if I didn't know any
# better, I'd say he was trying to
# get rid of me.
#
# Po chuckles. The others look at each other and chuckle
# awkwardly.
#
# MANTIS
# I know he can seem kind of
# heartless--
#
# He violently jabs another needle in Po.
#
# MANTIS (CONT'D)
# But, ya know, he wasn't always like
# that.
#
# VIPER
# According to legend, there was once
# a time when Master Shifu actually
# used to smile.
#
# PO
# No.
#
# MANTIS
# Yes.
#
# Cut to Tigress out in the hallway. She can hear them talking.
#
# VIPER
# But that was before...
#
# PO
# Before what?
#
# 46.
#
#
# Tigress enters.
#
# TIGRESS
# Before Tai Lung.
#
# Crane's shadow is silhouetted on the wall.
#
# CRANE
# Uh yeah, we're not really supposed
# to talk about him.
#
# TIGRESS
# Well, if he's going to stay here,
# he should know.
#
# PO
# (trying to ease the
# tension)
# Guys, guys. I know about Tai Lung.
#
# Tigress turns to Po.
#
# PO (CONT'D)
# He was a student, the first ever to
# master the thousand...
#
# Tigress approaches Po and leans in towards him.
#
# PO (CONT'D)
# (nervously trailing off)
# ...scrolls of... kung fu... and...
# then he turned bad... and now he's
# in jail.
#
# Tigress shakes her head at the panda's ignorance.
#
# TIGRESS
# He wasn't just a student.
#
# DISSOLVE TO:
#
#
# EXT. TRAINING HALL
#
# FLASHBACK. Shifu peeks out of the Training Hall and finds a
# baby leopard cub on the steps.
#
# TIGRESS (V.O.)
# Shifu found him as a cub. And he
# raised him as a son.
#
# Baby Tai Lung pulls on Shifu's whiskers.
#
# 47.
#
#
# TIGRESS (V.O.) (CONT'D)
# ...and when the boy showed talent
# in Kung Fu...
#
# Baby Tai Lung punches the training dummy across the floor.
#
# TIGRESS (V.O.) (CONT'D)
# ...Shifu trained him.
#
# Shifu teaches Baby Tai Lung how to punch.
#
# TIGRESS (V.O.) (CONT'D)
# He believed in him. He told him he
# was destined for greatness.
#
# Hard cut to a full-grown Tai Lung demolishing a training
# dummy.
#
# TIGRESS (V.O.) (CONT'D)
# It was never enough for Tai Lung.
# He wanted the Dragon Scroll. But
# Oogway saw darkness in his heart
# and refused. Outraged, Tai Lung
# laid waste to the valley. He tried
# to take the scroll by force. And
# Shifu had to destroy what he had
# created.
#
# Tai Lung ransacks a village on his way up to the Jade Palace.
# He crashes through the doors, running towards a waiting Shifu
# and Oogway.
#
# Shifu leaps at Tai Lung to deliver a kick.
#
# TIGRESS (V.O.) (CONT'D)
# But how could he?
#
# Seeing only baby Tai Lung running towards him, Shifu pulls
# his kick short. Tai Lung counters with a devastating strike
# and Shifu crashes to the ground holding his broken leg.
#
# Tai Lung leaps for the scroll, but Oogway stops him with
# strikes at his pressure points. He falls to the ground in a
# heap.
#
# TIGRESS (V.O.) (CONT'D)
# Shifu loved Tai Lung like he'd
# never loved anyone before...
#
# Young Tigress in the training hall strikes the dummy in the
# same manner as Tai Lung. Shifu corrects her form. Nothing
# more. Young Tigress looks crestfallen.
#
# 48.
#
#
# TIGRESS (V.O.) (CONT'D)
# ...or since.
#
# The sad, young Tigress cross-dissolves to adult Tigress.
#
#
# INT. BUNKHOUSE - EVENING
#
# Everyone is quiet in the moment.
#
# TIGRESS
# And now he has a chance to make
# things right, to train the true
# Dragon Warrior. And he's stuck with
# you: a big, fat panda who treats it
# like a joke.
#
# Po makes a googly-eyed face.
#
# PO
# Doieeeee...
#
# TIGRESS
# (charging at Po)
# Oh! That is it!
#
# Mantis pops up and halts Tigress.
#
# MANTIS
# Wait! My fault! I accidentally
# tweaked his facial nerve.
#
# Po falls face first to the floor, revealing his back is
# covered with needles.
#
# MANTIS (CONT'D)
# And may have also stopped his
# heart.
#
#
# INT. TRAINING HALL - NIGHT
#
# Shifu is sitting in meditation, fidgeting incessantly.
#
# SHIFU
# Inner peace. Inner peace. Inner
# peace.
#
# He finally opens one eye.
#
# SHIFU (CONT'D)
# Would whoever is making that
# flapping sound, quiet down!
#
# 49.
#
#
# Satisfied with the silence, Shifu nods and resumes his
# meditation.
#
# SHIFU (CONT'D)
# Inner...
#
# BOOM. Zeng drops in from the ceiling.
#
# SHIFU (CONT'D)
# Oh, Zeng. Excellent. I could use
# some good news right now.
#
# ZENG
# Uh...
#
# CUT TO:
#
#
# EXT. JADE PALACE GROUNDS - EVENING
#
# Oogway stands under the peach tree, deep in thought. Shifu
# rushes in, emerging from the mist, extremely agitated.
#
# SHIFU
# Master! Master!
#
# OOGWAY
# Hmmm?
#
# SHIFU
# (out of breath)
# I have-- it's-- it's very bad news.
#
# OOGWAY
# Ah, Shifu. There is just news.
# There is no good or bad.
#
# SHIFU
# Master, your vision...your vision
# was right. Tai Lung has broken out
# of prison. He's on his way!
#
# OOGWAY
# That is bad news...
#
# He turns to face Shifu and stares at him, eyebrow raised.
#
# OOGWAY (CONT'D)
# ...If you do not believe that the
# Dragon Warrior can stop him.
#
# SHIFU
# The panda? Master, that panda is
# not the Dragon Warrior.
# (MORE)
#
# 50.
# SHIFU (CONT'D)
# He wasn't even meant to be here --
# it was an accident!
#
# OOGWAY
# There are no accidents.
#
# SHIFU
# Yes, I know. You've said that
# already. Twice.
#
# OOGWAY
# Well, that was no accident either.
#
# SHIFU
# Thrice.
#
# OOGWAY
# My old friend, the panda will never
# fulfill his destiny, nor you yours,
# until you let go of the illusion of
# control.
#
# SHIFU
# Illusion?
#
# OOGWAY
# Yeah. Look at this tree, Shifu. I
# cannot make it blossom when it
# suits me, nor make it bear fruit
# before its time.
#
# SHIFU
# But there are things we can
# control.
#
# Shifu kicks the tree and a peach falls to his feet.
#
# SHIFU (CONT'D)
# I can control when the fruit will
# fall.
#
# A peach falls on his head and Oogway chuckles. Shifu tosses
# the peach in the air, leaps up, and splits it with a chop.
#
# SHIFU (CONT'D)
# And I can control--
#
# Shifu punches the ground, creating a hole and places the seed
# in it.
#
# SHIFU (CONT'D)
# --where to plant the seed. That is
# no illusion, Master.
#
# 51.
#
#
# OOGWAY
# Ah, yes. But no matter what you do,
# that seed will grow to be a peach
# tree. You may wish for an apple, or
# an orange... but you will get a
# peach.
#
# SHIFU
# But a peach cannot defeat Tai Lung!
#
# OOGWAY
# Maybe it can. If you are willing to
# guide it, to nurture it. To believe
# in it.
#
# Oogway covers the seed with dirt.
#
# SHIFU
# But how? How? I need your help,
# Master.
#
# OOGWAY
# No, you just need to believe.
# Promise me, Shifu. Promise me you
# will believe.
#
# SHIFU
# I... I will try.
#
# Oogway smiles, then glances up at the sky, then back down to
# Shifu.
#
# OOGWAY
# Good. My time has come. You must
# continue your journey without me.
#
# He hands his staff to a confused Shifu.
#
# SHIFU
# What... what are you..?
#
# Oogway backs away into the swirling fog.
#
# SHIFU (CONT'D)
# Master, you can't leave me!
#
# The petals surround Oogway as he approaches the cliff's edge.
#
# OOGWAY
# You must believe.
#
# SHIFU
# Master!
#
# 52.
#
#
# Shifu runs after him. Oogway is engulfed by peach blossoms.
# As the winds settle, Shifu is revealed standing at the edge
# of a cliff.
#
# Oogway is gone.
#
# We pan across to the bunkhouse.
#
# PO (O.S.)
# ...So I'm like, fine, you may be a
# wolf, you may be the scariest
# bandit in Haijin Province...
#
#
# INT. KITCHEN -- NIGHT
#
# Reveal Po is cooking for the Five.   He chops some veggies mid-
# air.
#
# PO
# ...but you're a lousy tipper.
#
# CRANE
# (incredulous)
# Really? So... how'd you get out of
# there alive?
#
# PO
# I mean, I didn't actually say that,
# but I thought it... in my mind.
#
# Po flips some bowls and expertly lines them up on his arm. He
# ladles soup into them.
#
# PO (CONT'D)
# (covering)
# If he... could read my mind, he'd
# have been like, "What?"
# (then)
# Order up!
#
# Po looks around expectantly and the Five (minus Tigress) dig
# in.
#
# PO (CONT'D)
# Hope you like it.
#
# MANTIS
# This is really good.
#
# PO
# (bashful)
# No, c'mon.
# (MORE)
#
# 53.
# PO (CONT'D)
# You should try my dad's secret
# ingredient soup. He actually knows
# the secret ingredient.
#
# VIPER
# What are you talking about? This is
# amazing.
#
# CRANE
# Wow, you're a really good cook.
#
# MANTIS
# I wish my mouth was bigger.
#
# The others laugh. But not Tigress.
#
# MONKEY
# Tigress, you gotta try this.
#
# Tigress looks up from her meal.
#
# TIGRESS
# It is said that the Dragon Warrior
# can survive for months at a time on
# nothing but the dew of a single
# gingko leaf and the energy of the
# universe.
#
# On the others for a beat. Then Po shrugs.
#
# PO
# I guess my body doesn't know it's
# the Dragon Warrior yet. I'm gonna
# need a lot more than dew. And, uh,
# universe juice.
#
# Po laughs. He picks up his bowl and takes a giant gulp. When
# he lowers the bowl, we see a noodle hanging from his face --
# it looks like a moustache. Mantis snickers.
#
# PO (CONT'D)
# What?
#
# MANTIS
# Oh, nothing... Master Shifu!
#
# The rest start laughing. Po realizes he's wearing a noodle
# moustache. He plays it up.
#
# 54.
#
#
# PO
# (imitating Shifu)
# You will never be the Dragon
# Warrior, unless you lose five
# hundred pounds and brush your
# teeth!
#
# The Five LAUGH.
#
# PO (CONT'D)
# (imitating Shifu)
# What is that noise you're making?
# Laughter? I never heard of it!
#
# The Five keep LAUGHING. Po reaches over and grabs two empty
# bowls and holds them up like ears.
#
# PO (CONT'D)
# (imitating Shifu)
# Work hard, Panda. And maybe,
# someday... you will have ears like
# mine.
#
# As the rest of the Five laugh, Tigress sneaks a moment to
# smell Po's soup. Leaning towards the bowl, she suddenly looks
# up and stops. The Five also look up and stop laughing.
#
# Reveal Shifu has entered behind Po. He is holding Oogway's
# staff.
#
# PO (CONT'D)
# (normal)
# Ears. It's not working for you? I
# thought they were pretty good.
#
# Po looks at the stone-faced Five. Tigress jumps to her feet.
#
# MONKEY
# It's Shifu.
#
# PO
# Of course it's Shifu. What do you
# think I'm doing?
#
# He finally notices Shifu standing there, doing a slow burn.
# Embarrassed, he places the soup bowls on his chest like a
# bra.
#
# PO (CONT'D)
# Ooh! Master Shifu!
#
# Po slurps up the noodle moustache. Monkey can't help but
# snicker.
#
# 55.
#
#
# SHIFU
# You think this is funny? Tai Lung
# has escaped from prison and you're
# acting like children!
#
# PO
# What?
#
# SHIFU
# He is coming for the Dragon Scroll,
# and you are the only one who can
# stop him.
#
# The bowls fall off. A beat as this sinks in... then Po starts
# to laugh.
#
# PO
# And here I am saying you got no
# sense of humor. I'm gonna stop
# Tai...
#
# Shifu just stares at him, deadly serious.
#
# PO (CONT'D)
# What? You're serious? And I have to--
# uh, Master Oogway will stop him! He
# did it before, he'll do it again.
#
# SHIFU
# Oogway cannot, not anymore.
#
# They notice Shifu holding Oogway's staff. They know what this
# means. They are saddened by the news.
#
# SHIFU (CONT'D)
# Our only hope is the Dragon
# Warrior.
#
# TIGRESS
# The panda?
#
# SHIFU
# Yes, the panda!
#
# TIGRESS
# Master, please. Let us stop Tai
# Lung. This is what you've trained
# us for.
#
# SHIFU
# No! It is not your destiny to
# defeat Tai Lung. It is his.
#
# He dramatically points at Po... but Po is gone.
#
# 56.
#
#
# SHIFU (CONT'D)
# Where'd he go?
#
# Shifu throws up his hands in frustration and heads after Po.
#
# CUT TO:
#
#
# EXT. BUNKHOUSE � DAY
#
# Super wide shot as Po runs away from the compound. Closer as
# he continues running. He checks over his shoulder, turns
# back... Shifu lands right in front of him.
#
# SHIFU
# You cannot leave! A real warrior
# never quits!
#
# PO
# Watch me!
#
# He tries to maneuver around Shifu, but is redirected back.
#
# PO (CONT'D)
# Come on! How am I supposed to beat
# Tai Lung? I can't even beat you to
# the stairs.
#
# SHIFU
# You will beat him because you are
# the Dragon Warrior!
#
# He pushes Po back with the staff.
#
# PO
# Ow! You don't believe that! You
# never believed that! From the first
# moment I got here, you've been
# trying to get rid of me.
#
# Shifu pokes him again, this time causing Po to fall on his
# back.
#
# SHIFU
# Yes. I was. But now I ask you to
# trust in your master as I have come
# to trust in mine.
#
# PO
# You're not my master. And I'm not
# the Dragon Warrior.
#
# Po shoves the staff away and gets up.
#
# 57.
#
#
# SHIFU
# Then why didn't you quit? You knew
# I was trying to get rid of you, and
# yet you stayed.
#
# PO
# Yeah, I stayed. I stayed because
# every time you threw a brick at my
# head or said I smelled, it hurt.
# But it could never hurt more than
# it did every day of my life just
# being me.
#
# Po looks down at the Valley, then turns back to Shifu.
#
# PO (CONT'D)
# I stayed because I thought if
# anyone could change me, could make
# me... not me, it was you. The
# greatest kung fu teacher in all of
# China.
#
# SHIFU
# But I can change you! I can turn
# you into the Dragon Warrior! And I
# will!
#
# PO
# C'mon, Tai Lung is on his way here
# right now. And even if it takes him
# a hundred years to get here, how
# are you gonna change this...
# (indicate belly)
# ...into the Dragon Warrior? How?
# How? How?!
#
# In frustration, Shifu yells out the answer.
#
# SHIFU
# I don't know!!!
# (then, resigned)
# I don't know.
#
# PO
# That's what I thought.
#
# Shifu walks away, leaving the path open to Po.
#
#
# EXT. JADE PALACE - NIGHT
#
# Tigress stands in the moonlight outside the palace. She has
# seen what just transpired between Shifu and Po.
#
# 58.
#
#
# She turns away, a look of resolve on her face... and LEAPS.
#
# She flies through the air, finally landing on a rooftop in
# the valley below. She looks back up at the palace.
#
# TIGRESS
# This is what you trained me for.
#
# She takes off running.
#
# The other four are right behind her.
#
# VIPER
# Tigress!
#
# She keeps going and they give chase.
#
# TIGRESS
# Don't try and stop me!
#
# The chase continues through the village.
#
# VIPER
# We're not trying to stop you!
#
# TIGRESS
# What?
#
# VIPER
# We're coming with you!
#
# Then...the others join her. Tigress smiles. They leap off
# into the night.
#
#
# EXT. JADE PALACE - EVENING
#
# Night dissolves to dawn. Shifu sits under the peach tree. He
# stirs, hearing KUNG FU NOISES from the training hall. He goes
# to investigate.
#
# CUT TO:
#
#
# INT. TRAINING HALL - DAWN
#
# Shifu looks inside -- it's empty. The NOISES continue from
# somewhere else -- the bunkhouse.
#
# CUT TO:
#
# 59.
#
#
# INT. KITCHEN - DAWN
#
# As Shifu turns the corner he sees Po's shadow as he performs
# some amazing Kung Fu.
#
# Entering the kitchen, Shifu finds Po is stuffing his face
# with food. Seeing Shifu, he stops mid-munch.
#
# In silence they eye each other. Shifu surveys the room --
# broken lock, smashed doors, unhinged cabinets. Po belches.
#
# PO
# (mouth full)
# What? I eat when I'm upset, okay?
#
# Shifu gets a glimmer in his eye. He has an idea.
#
# SHIFU
# Oh, no need to explain. I just
# thought you might be Monkey -- he
# hides his almond cookies on the top
# shelf.
#
# Shifu calmly exits and hides just outside the doorway,
# waiting to see if his hunch is correct.
#
# KLUMP! KLONK! THUNK! Shifu peeks back inside and finds Po
# perched atop the high shelves jamming more cookies into his
# mouth. Po notices Shifu walking back in.
#
# PO
# (mouth full)
# Don't tell Monkey.
#
# He glances back down at Shifu, whose disbelief turns to a
# wise smile.
#
# SHIFU
# Look at you.
#
# PO
# Yeah, I know. I disgust you.
#
# SHIFU
# No no, I mean... how did you get up
# there?
#
# PO
# I don't know. I guess I-- I don't
# know. I was getting a cookie...
#
# He looks at the cookie and then can't help but eat it.
#
# 60.
#
#
# SHIFU
# And yet you are ten feet off the
# ground and have done a perfect
# split.
#
# PO
# No, this... this is just an
# accident.
#
# He and Po stare at each other for a beat. Then... WHOOMP! Po
# slips and crashes to the kitchen floor. A cookie rolls over
# to Shifu. He picks it up.
#
# SHIFU
# There are no accidents. Come with
# me.
#
#
# EXT. MOUNTAINS - DAWN
#
# Shifu leads Po through the mountains.
#
# PO
# I know you're trying to be all
# mystical and kung fu-y, but could
# you at least tell me where we're
# going?
#
# Shifu just continues walking.
#
# CUT TO:
#
#
# EXT. MOUNTAINS - LATER
#
# Shifu is sitting beneath a tree. Winded and wheezing, Po
# slowly works his way up the hill.
#
# Po sets his gear down and looks around. Shifu breathes in the
# morning mist as Po approaches.
#
# PO
# You dragged me all the way out here
# for a bath?!
#
# Po begins to pat his armpits with water.
#
# SHIFU
# Panda, we do not wash our pits in
# The Pool of Sacred Tears.
#
# Po quickly stops. Realizing.
#
# 61.
#
#
# PO
# (in awe)
# The pool of...
#
# SHIFU
# This is where Oogway unravelled the
# mysteries of harmony and focus.
# This is the birthplace of Kung Fu.
#
# The camera cranes up to reveal they are standing on rock
# shapes that resemble a yin yang symbol.
#
# As the camera pulls further out, it pulls back through a
# vision of Oogway doing Kung Fu moves.
#
# FLASH FRAME -- Shifu leaps atop one of the rocks and looks
# down at Po.
#
# SHIFU (CONT'D)
# Do you want to learn Kung Fu?
#
# PO
# (awestruck)
# Yeah...
#
# SHIFU
# Then I am your master!
#
# PO
# Okay!
#
# Tears of joy well up in Po's eyes.
#
# SHIFU
# Don't cry.
#
# PO
# Okay.
#
# Po sniffs the tears back and smiles.
#
#
# EXT. FIELD - LATER
#
# Shifu leads Po out into an open field.
#
# SHIFU
# When you focus on Kung Fu, when you
# concentrate...you stink.
#
# Po scowls.
#
# 62.
#
#
# SHIFU (CONT'D)
# But perhaps that is my fault. I
# cannot train you the way I have
# trained the Five. I now see that
# the way to get through to you is
# with this!
#
# Shifu produces a bowl of dumplings.
#
# PO
# Oh great, `cause I'm hungry.
#
# SHIFU
# Good. When you have been trained,
# you may eat. Let us begin.
#
#
# EXT. FIELD - LATER
#
# Po's training unfolds -- deep breathing exercises, balance
# tests, push ups, sit ups, climbing, etc. Through it all, he
# never gets to eat, although he does indeed learn kung fu.
#
#
# EXT. CLEARING - A MOMENT LATER
#
# Shifu sets a bowl of dumplings on a boulder.
#
# SHIFU
# After you, panda.
#
# Po stops short, suspicious.
#
# PO
# Just like that? No situps? No ten
# mile hike?
#
# SHIFU
# I vowed to train you... and you
# have been trained. You are free to
# eat.
#
# Po grabs one of the dumplings in his chopsticks.
#
# SHIFU (CONT'D)
# Enjoy.
#
# Po raises the dumpling to his mouth. WHOOSH! Shifu snatches
# the dumpling away and eats it himself.
#
# PO
# Hey!
#
# 63.
#
#
# SHIFU
# I said you are free to eat. Have a
# dumpling.
#
# Po reaches again as Shifu leaps across the table and kicks
# the dumpling into the air.
#
# PO
# Hey!
#
# Shifu eats it and Po scowls.
#
# SHIFU
# You are free to eat!
#
# PO
# (upset)
# Am I?
#
# SHIFU
# (challenging)
# Are you?!
#
# Po and Shifu ready their chopsticks. Po slams the table and
# sends the bowl of dumplings airborne. Back and forth, Po and
# Shifu spar, vying for the dumplings. Until there is only one
# left.
#
# Shifu tries every trick to keep the dumpling away from Po. He
# hides it underneath one of the bowls. He uses his chopsticks
# as weapons to smack Po's chopsticks away. He attacks Po with
# his bamboo staff.
#
# But Po skillfully manages to best Shifu for the final
# dumpling.
#
# Shifu smiles. Po has passed the final test.
#
# But then Po tosses the dumpling into Shifu's open hand.
#
# PO
# I'm not hungry... master.
#
# Master and pupil bow to each other.
#
# CUT TO:
#
#
# EXT. MOUNTAIN PASS
#
# The Five race toward a rope bridge stretched between mountain
# peaks.
#
# 64.
#
#
# Tai Lung appears at the other end of the bridge. He ROARS and
# races toward them.
#
# TIGRESS
# Cut it!
#
# The others slash at the ropes securing the bridge to the
# mountain. Tai Lung is almost upon them when Tigress cuts the
# final rope. But Tai Lung is too close -- Tigress must launch
# herself into him. The two cats end up in the middle of the
# bridge just as it starts to tumble into the canyon below. The
# Five grab support ropes and hold on for dear life.
#
# TAI LUNG
# Where's the Dragon Warrior?
#
# TIGRESS
# How do you know you're not looking
# at her?
#
# Tai Lung laughs. It echoes off the mountain walls.
#
# TAI LUNG
# You think I'm a fool? I know you're
# not the Dragon Warrior. None of
# you!
#
# The Five exchange quick, worried looks.
#
# TAI LUNG (CONT'D)
# (nodding confidently)
# I heard how he fell out of the sky
# on a ball of fire, that he's a
# warrior unlike anything the world
# has ever seen.
#
# The Five exchange quick, confused looks.
#
# MONKEY
# Po?
#
# TAI LUNG
# So that is his name -- Po. Finally,
# a worthy opponent. Our battle will
# be legendary!
#
# Tigress charges at him. The battle begins. Tigress punches
# Tai Lung as he hangs from the bridge. But Tai Lung counters
# with a maneuver that sends Tigress slamming backwards through
# the bridge's wooden slats. Then Tigress gets choked by the
# bridge's ropes. Monkey turns to Crane and Viper.
#
# MONKEY
# We've got this. Help her!
#
# 65.
#
#
# Viper grabs Tai Lung, which causes him to let go of the
# ropes. Tigress plummets down into the gorge... but Crane
# manages to catch her. Viper punches Tai Lung repeatedly with
# his own fist. Tai Lung manages to get a paw around Viper's
# "throat".
#
# VIPER
# Monkey!
#
# ANGLE ON MANTIS AND MONKEY. Mantis is straining to hold the
# rope by himself.
#
# MANTIS
# Go!
# (then)
# Ack! What was I thinking?!
#
# Monkey leaps into action, kicking Tai Lung in the chest and
# sending him crashing through the slats of the bridge. He gets
# back to his feet and starts running back to them on a single
# strand of rope.
#
# TIGRESS
# Mantis!
#
# Mantis whips his end of the rope, sending a sine wave
# shooting toward Tai Lung. The rope whips Tai Lung in the face
# and he gets tangled up. The Five see their chance.
#
# TIGRESS (CONT'D)
# Now!
#
# Working as a team, the Five kick Tai Lung's butt every which
# way. Tigress finally slashes the last rope holding up Tai
# Lung. He plummets down... down... disappearing into the mist.
# Mantis whips his end of the rope, returning his buddies
# safely to the mountain.
#
# The Five look relieved. But the relief is short-lived...
#
# Tigress notices that the other end of the bridge is circling
# the far mountain peak. Her eyes go wide with dread. The rope
# whips up. But Tai Lung isn't there.
#
# With a crash, he suddenly appears behind the Five.
#
# TAI LUNG
# Shifu taught you well...
#
# Tai Lung jabs a finger at Monkey, who instantly freezes.
#
# TAI LUNG (CONT'D)
# But he didn't teach you everything.
#
# 66.
#
#
# Tai lung lunges toward the rest.
#
#
# EXT. TRAINING HALL - EVENING
#
# Shifu and Po walk through the palace courtyard. Po has an
# easy spring in his step.
#
# SHIFU
# You have done well, Panda.
#
# PO
# Done well? Done well?! I've done
# awesome!
#
# He swings his belly around and knocks Shifu off balance.
#
# Shifu staggers back, regaining his dignity.
#
# SHIFU
# The mark of a true hero is
# humility!
#
# After a moment's thought, though, he leans toward Po -
#
# SHIFU (CONT'D)
# But yes...you have done awesome.
#
# And he punches him playfully on the arm. Po smiles at him. As
# they LAUGH, an indistinct figure appears in the clouds behind
# them. IT'S CRANE!
#
# Crane carries the five to the palace grounds, crashing in a
# heap.
#
# PO
# Huh? Guys? Guys!
#
# Po throws his backpack aside and runs over to them.
#
# PO (CONT'D)
# They're dead? No, they're
# breathing! They're asleep?! No,
# their eyes are open.
#
# Crane struggles to lift his head.
#
# CRANE
# We were no match for his nerve
# attack.
#
# His head collapses to the ground.
#
# 67.
#
#
# SHIFU
# He has gotten stronger.
#
# PO
# Who? Tai Lung? Stronger?
#
# Shifu starts freeing the Five. First Viper, then Mantis, then
# Monkey releases suddenly from his paralysis -
#
# MONKEY
# He's too fast!
#
# He delivers a Kung Fu punch to Po's head and then slowly
# realizes where he is.
#
# MONKEY (CONT'D)
# Sorry, Po.
#
# Shifu kneels before Tigress and works to free her.
#
# TIGRESS
# I thought we could stop him.
#
# SHIFU
# He could have killed you.
#
# MANTIS
# Why didn't he?
#
# SHIFU
# So you could come back here and
# strike fear into our hearts. But it
# won't work!
#
# PO
# Uh, it might, I mean, a little. I'm
# pretty scared.
#
# SHIFU
# You can defeat him, panda.
#
# PO
# Are you kidding? If they can't--
# They're five masters. I'm just one
# me.
#
# SHIFU
# But you will have the one thing
# that no one else does.
#
# 68.
#
#
# INT. SCROLL ROOM - MOMENTS LATER
#
# CLOSE-UP of the Dragon Scroll. Po stares at Shifu - then
# looks up at the Scroll. Then back at Shifu -
#
# PO
# You really believe I'm ready?
#
# SHIFU
# You are, Po.
#
# They look at each other. This is a big moment.
#
# Oogway's staff hangs in a rack surrounded by candles. As Po
# and The Five stand by, Shifu carries the staff over to the
# reflecting pool. Shifu bows his head, then, eyes still
# closed, he raises the staff up above his head. Po and the
# others watch, expectantly. The peach blossom petals rise in a
# flickering, spinning cloud up from the pool. The gentle
# tornado rises up around the ceiling carving that holds the
# Dragon Scroll. The petals loosen the scroll from the dragon's
# mouth and it falls. At the last second, Shifu reaches out
# with the staff to catch the scroll on the end of it. He turns
# to Po, holding it out.
#
# SHIFU (CONT'D)
# Behold. The Dragon Scroll... It is
# yours.
#
# PO
# Wait, what happens when I read it?
#
# SHIFU
# No one knows, but legend says you
# will be able to hear a butterfly's
# wing-beat.
#
# PO
# Whoa! Really? That's cool.
#
# SHIFU
# Yes. And see light in the deepest
# cave. You will feel the universe in
# motion around you.
#
# PO
# Wow! Can I punch through walls?
# Can I do a quadruple back flip?
# Will I have invisibility--
#
# SHIFU
# Focus. Focus.
#
# 69.
#
#
# PO
# Huh? Oh, yeah... yeah.
#
# SHIFU
# Read it, Po, and fulfill your
# destiny. Read it and become... the
# Dragon Warrior!
#
# PO
# Whooaa!!!
#
# Po takes a deep breath. Then he grasps the tube and tries to
# pull the top off it. It doesn't budge. He strains at it.
#
# PO (CONT'D)
# It's impossible to open.
#
# He strains again. He tries to bite it off...
#
# PO (CONT'D)
# Come on baby. Come on now...
#
# Shifu SIGHS and holds out his hand. Po passes him the tube.
# Shifu pops the end off effortlessly and passes it back to Po.
#
# PO (CONT'D)
# Thank you. I probably loosened it
# up for you though... Okay, here
# goes.
#
# He glances at the Five. They look on in awe. Monkey gives him
# the `thumbs up.' Po starts to unroll the scroll, the golden
# light bathing his face. Across the scroll we see Shifu,
# excited that he is witness to history...
#
# On Po's face as he finishes opening the scroll.
#
# Then -
#
# PO (CONT'D)
# AAAAAAAAAAAAAAAAAAAAAAAAA!
#
# Shifu looks concerned. The Five look concerned. Po looks
# utterly terrified.
#
# PO (CONT'D)
# It's blank!
#
# SHIFU
# What?
#
# PO
# Here! Look!
#
# 70.
#
#
# Po tries to show Shifu the scroll. Shifu covers his eyes and
# turns his head away.
#
# SHIFU
# No! I am forbidden to look upon--
#
# But he can't help himself. He takes a peek. Then he GRABS if
# off Po. He turns it around, then upside down. He closes it
# and opens it again, astonished.
#
# SHIFU (CONT'D)
# Blank? I don't...I don't
# understand.
#
# Shifu turns away, contemplative. What can this mean?
#
# PO
# Okay. So like, Oogway was just a
# crazy old turtle after all?
#
# SHIFU
# No. Oogway was wiser than us all.
#
# Po sits heavily on the floor, dejected.
#
# PO
# Oh, come on! Face it. He picked me
# by accident. Of course I'm not the
# Dragon Warrior. Who am I kidding?
#
# The Five don't argue.
#
# TIGRESS
# But who will stop Tai Lung?
#
# CRANE
# He'll destroy everything...and
# everyone.
#
# Shifu puts the scroll back in its container and seals it. He
# looks oddly calm as he turns around.
#
# SHIFU
# No, evacuate the Valley. You must
# protect the villagers from Tai
# Lung's rage.
#
# TIGRESS
# What about you master?
#
# SHIFU
# I will fight him.
#
# 71.
#
#
# PO
# What?
#
# SHIFU
# I can hold him off long enough for
# everyone to escape.
#
# PO
# But Shifu, he'll kill you.
#
# SHIFU
# Then I will finally have paid for
# my mistake.
#
# The Five and Po look devastated.
#
# SHIFU (CONT'D)
# Listen to me, all of you. It is
# time for you to continue your
# journey without me. I am very proud
# to have been your master.
#
# Shifu salutes them and turns away. Po is heartbroken. Crane
# steps forward and kindly puts a wing around Po, pulling away.
#
# Po resists for a moment, then lets the Five lead him off.
#
# CUT TO:
#
#
# EXT. VALLEY
#
# The Five arrive at the base of the stairs.
#
# TIGRESS
# We've got to get them out safely.
#
# Monkey picks up a small child.
#
# MONKEY
# Come, little one. Let's find your
# mama.
#
# TIGRESS
# Viper, gather the southern farmers.
# Mantis, the north. Crane, light the
# way.
#
# They split up and begin helping the villagers evacuate. Po is
# left by himself.
#
# He makes his way through the bustling town.
#
# 72.
#
#
# JR SHAW
# (skeptically)
# Look, it's the Dragon Warrior.
#
# Po approaches the Noodle Shop.
#
# PO
# Hey, Dad.
#
# PO'S DAD
# Po!
#
# Seeing Po, Po's Dad hurries over and wraps his arms around
# his son. Po bends down to reciprocate the hug, as Po's dad
# pulls away, having fastened an apron around Po's waist.
#
# PO'S DAD (CONT'D)
# Good to have you back, son!
#
# PO
# (listlessly)
# Good to be back.
#
# Po's Dad goes back to packing things up.
#
# PO'S DAD
# Let's go Po. So, for our next shop,
# it's time to face it -- the future
# of noodles is dice-cut vegetables,
# no longer slices.
#
# Dad starts to walk off, unaware that Po isn't following.
#
# PO'S DAD (CONT'D)
# Also, I was thinking, maybe this
# time we'll have a kitchen you can
# actually stand up in. Hmm? You like
# that?
#
# He turns and notices that Po hasn't moved. He walks to Po
# sympathetically.
#
# PO'S DAD (CONT'D)
# Po, I'm sorry things didn't work
# out. It just... wasn't meant to be.
#
# Po slumps against the cart.
#
# PO'S DAD (CONT'D)
# Po, forget everything else. Your
# destiny still awaits. We are noodle
# folk -- broth runs deep through our
# veins.
#
# 73.
#
#
# PO
# I don't know, Dad. Honestly,
# sometimes I can't believe I'm
# actually your son.
#
# Dad is taken aback.
#
# PO'S DAD
# Po, I think it's time I told you
# something I should have told you a
# long time ago...
#
# PO
# Okay.
#
# Dad pauses dramatically.
#
# PO'S DAD
# The secret ingredient of my secret
# ingredient soup!
#
# Po feigns excitement.
#
# PO
# Oh.
#
# PO'S DAD
# C'mere! The secret ingredient is...
# nothing!
#
# PO
# Huh?
#
# PO'S DAD
# You heard me. Nothing. There is no
# secret ingredient!
#
# PO
# Wait wait...it's just plain old
# noodle soup? You don't add some
# kind of special sauce or something?
#
# PO'S DAD
# Don't have to. To make something
# special, you just have to believe
# it's special.
#
# Po looks at his father with dawning realization. He picks up
# the Scroll.
#
# For a moment, Po stares at his reflection on the scroll, then
# he smiles serenely. He gets it now.
#
# 74.
#
#
# PO
# There is no secret ingredient...
#
# Po turns back to look at the palace.
#
# CUT TO:
#
#
# EXT. JADE PALACE - DAWN
#
# At the top of the stairs, Shifu looks upon the Valley,
# awaiting his fate. With a gust of wind, Tai Lung appears
# before him.
#
# TAI LUNG
# I have come home, Master.
#
# SHIFU
# This is no longer your home. And I
# am no longer your master.
#
# TAI LUNG
# Yes. You have a new favorite. So
# where is this...Po? Did I scare him
# off?
#
# SHIFU
# This battle is between you and me.
#
# TAI LUNG
# So. That is how it's going to be?
#
# SHIFU
# That is how it must be.
#
# They fight. At last. Tai Lung punches Shifu clean through the
# doors of the Jade Palace.
#
# Tai Lung enters.
#
# TAI LUNG
# I rotted in jail for twenty years
# because of your weakness!
#
# SHIFU
# Obeying your master is not
# weakness!
#
# TAI LUNG
# You knew I was the Dragon Warrior!
# You always knew...
#
# Dissolve to FLASHBACK.
#
# 75.
#
#
# A young Tai Lung looks expectant. Oogway shakes his head.
#
# TAI LUNG (V.O.) (CONT'D)
# But when Oogway said otherwise,
# what did you do? What did you do?!
#
# Tai Lung looks to Shifu who averts his eyes and the past
# dissolves into the present.
#
# TAI LUNG (CONT'D)
# NOTHING!
#
# Shifu takes a Kung Fu stance.
#
# SHIFU
# You were not meant to be the Dragon
# Warrior! That was not my fault!
#
# TAI LUNG
# NOT YOUR FAULT?!
#
# Enraged, Tai Lung knocks over the Kung Fu artifacts and
# throws them at Shifu.
#
# TAI LUNG (CONT'D)
# WHO FILLED MY HEAD WITH DREAMS?!
# WHO DROVE ME TO TRAIN UNTIL MY
# BONES CRACKED?! WHO DENIED ME MY
# DESTINY?!
#
# Shifu dodges each attack.
#
# SHIFU
# It was never my decision to make!
#
# Tai Lung pulls Oogway's staff from the shrine.
#
# TAI LUNG
# It is now.
#
# They fight. Tai Lung pins Shifu down with the staff.
#
# TAI LUNG (CONT'D)
# Give me the scroll!
#
# SHIFU
# I would rather die.
#
# They struggle for a beat until finally, the staff splinters
# into a hundred pieces. Shifu looks back at the pieces and a
# flutter of peach tree petals fly by. Caught off guard, Shifu
# gets kicked by Tai Lung into a column.
#
# 76.
#
#
# Shifu climbs the column to the rafters. Tai Lung follows and
# sends them both crashing through the roof.
#
# Lightning flash.
#
# Grappling in mid-air, Tai Lung gets his hands around Shifu's
# throat as they crash back through the roof.
#
# They kick apart. Shifu crashes to the floor and lands hard.
# Tai Lung bounces off the wall and throws a lantern to the
# floor. Flames go everywhere. Tai Lung's arms are aflame as he
# charges at Shifu.
#
# TAI LUNG
# All I ever did, I did to make you
# proud! Tell me how proud you are,
# Shifu! Tell me! TELL ME!
#
# THOOM! A fiery punch sends Shifu skidding across the floor
# and crashing against the reflecting pool. The flames
# extinguish and Tai Lung extends his claws.
#
# SHIFU
# (weakly)
# I have always been proud of you.
# From the first moment, I've been
# proud of you. And it was my pride
# that blinded me. I loved you too
# much to see what you were becoming.
# What I was turning you into. I'm...
# sorry.
#
# Tai Lung stops in his tracks. Shifu waits. Tai Lung's
# expression goes cold. He grabs Shifu by the throat.
#
# TAI LUNG
# I don't want your apology. I want
# my scroll!
#
# He holds Shifu up to the ceiling. Looking up, Tai Lung
# bristles when he sees the scroll is missing.
#
# TAI LUNG (CONT'D)
# WHAT? WHERE IS IT?!
#
# Tai Lung slams Shifu to the floor.
#
# SHIFU
# (weakly)
# Dragon Warrior has taken scroll
# halfway across China by now. You
# will never see that scroll, Tai
# Lung. Never. Never...
#
# 77.
#
#
# Tai Lung is furious. He roars, ready to strike Shifu.
# Suddenly...
#
# PO (O.S.)
# Hey!
#
# Tai Lung turns around to find Po standing in the doorway.
#
# PO (CONT'D)
# (out of breath)
# Stairs...
#
# Tai Lung casts Shifu aside.
#
# TAI LUNG
# Who are you?
#
# PO
# Buddy, I am the Dragon Warrior.
# (exhales hard)
# Huhhh...
#
# TAI LUNG
# You?! Him?!
# (to Shifu)
# He's a panda.
# (back to Po)
# You're a panda. What are you gonna
# do, big guy? Sit on me?
#
# PO
# Don't tempt me. Haha. No. I'm gonna
# use this. You want it? Come and get
# it.
#
# Po shows him the Dragon Scroll.
#
# From out of nowhere, Tai Lung appears and punches Po across
# the room, grabbing the scroll knocked from Po's hands.
#
# TAI LUNG
# Finally!
#
# Po bounces off a nearby pillar and slams back into Tai Lung,
# sending him flying into a column. Po puts on a brave face and
# strikes a pose as Tai Lung recovers and charges. Po turns to
# run.
#
# Tai Lung quickly catches up and they both sail off the Palace
# steps.
#
# Po clings to the scroll as Tai Lung delivers a kick and sends
# him crashing onto the theater rooftops below.
#
# 78.
#
#
# Po rolls down off a tree and uses the recoil to whip back and
# smash Tai Lung. He briefly skids across the rooftop and comes
# right back at Po.
#
# TAI LUNG (CONT'D)
# That scroll is mine!
#
# Down the Theater steps, Po and Tai Lung grapple for the
# scroll. Po is oblivious to the effects of crashing down
# stairs and in slow motion, his voluminous butt presses down
# on Tai Lung's head. As they crash through the Gateway the
# scroll is knocked loose. Tai Lung goes for the scroll but Po
# snatches it away using a noodle lasso. The scroll flies
# towards him and bounces off his head. Tai Lung leaps for it,
# but Po grabs his tail and pulls him back down onto a cart
# which see-saws Po into the air. In mid-air, Po slurps the
# noodle.
#
# Up and over the rooftops, Po lands in a grove of bamboo trees
# and into a nearby wok shop. The scroll rolls to a stop in the
# street.
#
# As Tai Lung makes his move on the scroll, Po turns the array
# of overturned woks into a shell game, sliding the woks around
# to hide the scroll.
#
# PO
# Lightning!
#
# Tai Lung knocks the woks away and exposes the scroll as Po
# uses his bamboo stilts to block Tai Lung. The leopard swipes
# out the stilts and brings Po down on top of him as the scroll
# rolls down the steps towards the river.
#
# Po gets thrown into a fireworks booth. As Tai Lung chases
# down the scroll, he turns back to see Po flying through the
# fireworks-filled sky.
#
# Po slams through Tai Lung and crashes into a rock wall. The
# scroll flies out of his hand and lands in the mouth of an
# ornamental rooftop dragon. He looks back at Tai Lung, who
# sees where the scroll has landed. Via the magic of cookie-
# vision, Po effortlessly scales the building. Tai Lung is
# shocked.
#
# TAI LUNG
# The scroll has given him power.
# (then)
# NOOO0!!
#
# He takes a giant leap and kicks the wall. The resulting
# shockwave collapses the building.
#
# 79.
#
#
# Amazingly, Po skips across the falling roof tiles to reach
# the scroll in mid-air as Tai Lung leaps up behind him and
# unleashes a punishing blow that sends Po smashing into the
# ground. As Tai Lung lands, he delivers a final devastating
# punch.
#
# As the dust settles, Tai Lung is looming over Po in the
# impact crater.
#
# TAI LUNG (CONT'D)
# (out of breath)
# Finally... oh yes... the power of
# the Dragon Scroll... is mine!
#
# Tai Lung grabs for the scroll and opens it. His face falls.
#
# TAI LUNG (CONT'D)
# It's NOTHING!!
#
# Po stirs.
#
# PO
# It's okay. I didn't get it the
# first time either.
#
# TAI LUNG
# (disbelief)
# What?
#
# Po gets to his feet.
#
# PO
# There is no secret ingredient. It's
# just you.
#
# Tai Lung snarls and lunges at Po.
#
# TAI LUNG
# RRRAAAH!
#
# PO
# AAAAGGGHH!
#
# Tai Lung attacks Po's nerve points. But Po begins giggling.
#
# PO (CONT'D)
# Stop! Stop it! I'm gonna pee!
# Don't! Don't!
#
# Tai Lung's nerve attack has no effect on Po. Frustrated, he
# delivers a double-fisted punch to Po's belly.
#
# 80.
#
#
# The shockwave ripples through Po's entire body and Po's arms
# come back and strike Tai Lung, sending the leopard crashing
# back into a building. Po looks at his hands, amazed at what
# he just did.
#
# Tai Lung rises from the rubble and runs at Po again. But Po
# strikes back, using an unorthodox panda-style technique, even
# getting Tai Lung to chomp down on his own tail. Po gives Tai
# Lung a butt bump that sends him crashing into a building. Tai
# Lung emerges and attempts one more lunge at Po. But Po
# prepares... and Tai Lung is swiftly met by Po's IRON BELLY!
# He is launched into the air. Po waits... and waits... until
# finally, Tai Lung appears in the sky and crashes to the
# ground.
#
# Tai Lung is battered, but still defiant.
#
# TAI LUNG
# (heavy breathing)
# You... can't defeat me. You're just
# a big, fat panda!
#
# SCHWING! Po grabs Tai Lung's finger. Tai Lung's eyes go wide.
#
# PO
# I'm not a big, fat panda. I'm the
# big, fat panda.
#
# Po's pinky pops up. Tai Lung gasps.
#
# TAI LUNG
# The Wuxi Finger Hold!
#
# PO
# Oh, you know this hold?
#
# TAI LUNG
# You're bluffing. You're bluffing!
# Shifu didn't teach you that.
#
# PO
# Nope. I figured it out.
#
# He flexes his pinky...
#
# PO (CONT'D)
# Skadoosh!
#
# KA-THOOM!
#
# 81.
#
#
# EXT. VALLEY OF PEACE
#
# A mushroom cloud appears over the Valley, sweeping past the
# Furious Five and the fleeing villagers.
#
# DISSOLVE TO:
#
#
# EXT. VALLEY SQUARE - A LITTLE LATER
#
# Villagers emerge from hiding. Po walks out from the mist
# looking very much like the warrior from the opening dream.
#
# KG SHAW
# Look! The Dragon Warrior.
#
# As he nears, we see that his hat is an upside down wok and
# his scarf is a torn apron.
#
# Villagers CHEER the Dragon Warrior. Po's Dad emerges from the
# crowd.
#
# PO'S DAD
# That's my boy. That big, lovely
# kung fu warrior is my son!
#
# PO
# Thanks, Dad.
#
# Po hugs his dad. The wok falls off Po's head and rolls on the
# ground until Mantis appears in frame and stops it. The rest
# of the Five are with him. Po takes notice.
#
# PO (CONT'D)
# Hey, guys.
#
# TIGRESS
# Master.
#
# Tigress bows deeply. The others follow.
#
# FURIOUS FIVE
# Master.
#
# PO
# (modest)
# Master?
# (then, remembering)
# Master Shifu!
#
# Po races toward the Jade Palace. He climbs the steps. Then
# more steps.
#
# 82.
#
#
# INT. PALACE - MOMENTS LATER
#
# Po arrives breathless at the Jade Palace. Shifu is still
# lying in the scroll room, his eyes closed. Po rushes to his
# side.
#
# PO
# Master! Shifu! Shifu! Are you okay?
#
# Shifu weakly opens his eyes.
#
# SHIFU
# Po! You're alive!
# (then, darkly)
# Or we're both dead.
#
# PO
# No, Master, I didn't die. I
# defeated Tai Lung!
#
# SHIFU
# You did?!
#
# Shifu smiles and shakes his head in disbelief.
#
# SHIFU (CONT'D)
# Wow. It is as Oogway foretold --
# You are the Dragon Warrior. You
# have brought peace to this Valley.
# And to me. Thank you. Thank you,
# Po. Thank you...
#
# Shifu closes his eyes. He is still. Po starts freaking out.
#
# PO
# No! Master! No No No! Don't die,
# Shifu. Please...
#
# SHIFU
# (eyes snapping open)
# I'm not dying, you idiot-- ah,
# Dragon Warrior. I'm simply at
# peace. Finally.
#
# PO
# Oh. So, um, I should...stop
# talking?
#
# SHIFU
# If you can.
#
# Po nods reverently as Shifu closes his eyes again. Master and
# pupil lie next to each other. The camera pulls up and back
# away from them. Po tries to remain still, but it's hard.
#
# 83.
#
#
# He's about to say something, but he stops himself. He fidgets
# for a beat, then can't control himself any longer.
#
# PO
# Want to get something to eat?
#
# SHIFU
# (sighs)
# Yeah.
#
# IRIS OUT.
#
# THE END
