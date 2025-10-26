from flask import Blueprint, jsonify, request, render_template
import random

gambling_bp = Blueprint("gambling", __name__)


@gambling_bp.route("/api/gamble", methods=["POST"])
def gamble():
    """Simple gambling endpoint"""
    data = request.get_json() or {}
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


@gambling_bp.route("/bet_rps", methods=["GET"])
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
        "payout": payout,
    }), 200


@gambling_bp.route("/bet_slots")
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


@gambling_bp.route("/slots", methods=["POST"])
def slots():
    """POST /slots - legacy slots endpoint that expects JSON with 'bet' and 'username'"""
    data = request.get_json() or {}
    bet = data.get("bet", 1)
    username = data.get("username", "user1")

    # Import users dict from app at runtime to avoid circular imports
    try:
        from app import users
    except Exception:
        users = {}

    if username not in users or users[username]["balance"] < bet:
        return jsonify({"error": "Insufficient balance or user not found."}), 400

    symbols = ["CHERRY", "LEMON", "BELL", "STAR", "7"]
    result = [random.choice(symbols) for _ in range(3)]

    # Determine payout
    if result.count(result[0]) == 3:
        payout = bet * 10  # Jackpot
        message = "Jackpot! All symbols match."
    elif len(set(result)) == 2:
        payout = bet * 2
        message = "Two symbols match! Small win."
    else:
        payout = 0
        message = "No match. Try again!"

    users[username]["balance"] += payout - bet

    return jsonify({
        "result": result,
        "message": message,
        "payout": payout,
        "balance": users[username]["balance"],
    })


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


@gambling_bp.route("/blackjack", methods=["GET", "POST"])
def blackjack():
    if request.method == "POST":
        data = request.get_json() or {}
        bet_amount = data.get("bet_amount")
        username = data.get("username")

        try:
            from app import users
        except Exception:
            users = {}

        if username not in users or users[username]["balance"] < bet_amount:
            return jsonify({"error": "Insufficient balance or user not found."}), 400

        deck = create_deck()
        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        player_total = calculate_hand_value(player_hand)
        dealer_total = calculate_hand_value(dealer_hand)

        # Basic stand/hit loop driven by provided action (simple)
        while player_total < 21:
            action = data.get("action")
            if action == "hit":
                player_hand.append(draw_card(deck))
                player_total = calculate_hand_value(player_hand)
            elif action == "stand":
                break
            else:
                break

        while dealer_total < 17:
            dealer_hand.append(draw_card(deck))
            dealer_total = calculate_hand_value(dealer_hand)

        result = determine_winner(player_total, dealer_total)
        if result == "player":
            users[username]["balance"] += bet_amount
            return jsonify({"message": "You win!", "balance": users[username]["balance"]})
        elif result == "dealer":
            users[username]["balance"] -= bet_amount
            return jsonify({"message": "Dealer wins!", "balance": users[username]["balance"]})
        else:
            return jsonify({"message": "It's a tie!", "balance": users[username]["balance"]})

    return render_template("blackjack.html")


@gambling_bp.route("/craps")
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


@gambling_bp.route("/roulette", methods=["GET"])
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


@gambling_bp.route("/russian-roulette", methods=["GET"])
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
