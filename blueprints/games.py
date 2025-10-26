from flask import Blueprint, render_template, request, jsonify
import random
import bank

games_bp = Blueprint("games", __name__)


@games_bp.route("/sports", methods=["GET", "POST"])
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


@games_bp.route("/plant-battle", methods=["GET"])
def plant_battle():
    # Available plant roster
    plants = ["Cactus", "Venus Flytrap", "Sunflower", "Bamboo", "Poison Ivy"]

    # Each plant’s base stats
    plant_stats = {
        "Cactus": {"attack": 7, "defense": 9, "rarity": "Common"},
        "Venus Flytrap": {"attack": 9, "defense": 6, "rarity": "Rare"},
        "Sunflower": {"attack": 5, "defense": 8, "rarity": "Uncommon"},
        "Bamboo": {"attack": 6, "defense": 7, "rarity": "Common"},
        "Poison Ivy": {"attack": 8, "defense": 5, "rarity": "Rare"},
    }

    bet = request.args.get("bet", default=10, type=int)
    chosen_plant = request.args.get("plant", default=random.choice(plants))

    # Validate bet and input
    if bet <= 0:
        return jsonify({"error": "Bet must be a positive integer"}), 400
    if chosen_plant not in plants:
        return jsonify({"error": f"Plant must be one of {plants}"}), 400

    # Randomly determine winner
    winner = random.choice(plants)
    won = chosen_plant == winner
    winnings = bet * 2 if won else 0

    chosen_stats = plant_stats[chosen_plant]
    winner_stats = plant_stats[winner]

    # Battle narrative
    if chosen_plant == winner:
        message = f"{chosen_plant} absorbed sunlight and claimed a glorious victory!"
    else:
        if chosen_stats["attack"] > winner_stats["attack"]:
            message = f"{chosen_plant} fought valiantly but eventually wilted in defeat."
        else:
            message = f"{chosen_plant} was overwhelmed by {winner}'s ferocity!"

    # Dynamic conditions
    environment = random.choice(["Greenhouse", "Jungle", "Desert", "Swamp", "Backyard"])
    weather = random.choice(["Sunny", "Rainy", "Windy", "Cloudy"])

    # Final JSON response
    return jsonify({
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
    })
