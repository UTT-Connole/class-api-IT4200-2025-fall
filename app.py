from flask import Flask, render_template, request, jsonify, send_from_directory
import random
import json
import os
from dataclasses import dataclass, field
from uuid import uuid4
from secrets import SystemRandom
from datetime import datetime, timedelta, date
from typing import Set, Tuple, Dict, Optional
from flask import Blueprint
from user_agents import parse
import requests

app = Flask(__name__)
OWM_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Moved global variables to top for organization
adjectives = ['Fluffy', 'Silly', 'Happy', 'Sleepy', 'Grumpy', 'Bouncy', 'Lazy', 'Sweet']
nouns = ['Paws', 'Whiskers', 'Shadow', 'Bean', 'Muffin', 'Cookie', 'Nugget', 'Pickle']
restaurants = [
    "Chipotle",
    "Chick-fil-A",
    "Subway",
    "Olive Garden",
    "Five Guys",
    "Panera Bread"
]

@app.route('/')
def home():
    return render_template('index.html'), 200

@app.route('/pokemon')
def pokemon():
    return jsonify({"pokemon": "Jigglypuff"})

# Unlivable Realestate Endpoints
@app.route('/api/chernobyl/properties', methods=['GET'])
def get_chernobyl_properties():
    """Get Chernobyl real estate listings"""
    properties = [
        {
            "id": 1,
            "address": "Pripyat Central Square, Apartment Block #1",
            "price": 0,
            "radiation_level": "15,000 mSv/year",
            "distance_from_reactor": "3 km",
            "amenities": ["Ferris wheel view", "Glow-in-the-dark features", "No electricity needed"],
            "warnings": ["Protective gear required", "May cause mutations"]
        },
        {
            "id": 2,
            "address": "Reactor 4 Penthouse Suite",
            "price": -1000000,
            "radiation_level": "Over 9000 mSv/year",
            "distance_from_reactor": "0 km",
            "amenities": ["360° views", "Built-in sarcophagus", "Unlimited energy"],
            "warnings": ["Immediate death likely", "GPS stops working"]
        }
    ]

    return jsonify({
        "message": "Chernobyl Real Estate - Where your problems glow away!",
        "properties": properties
    })

@app.route('/kasen')
def kasen():
    return render_template('kasen.html'), 200

@app.route('/clint')
def home1():
    return 'Hello, Clint!'

@app.route('/gill')
def home2():
    user_input = ('We seek the Holy Grail')
    if user_input == 'We seek the Holy Grail':
        return "You may pass"
    else:
        return 'You are doomed'

@app.route('/pet-name')
def generate_pet_name():
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    return f'{adj} {noun}'

@app.route('/dallin')
def home11():
    user_input = input('Are you sure you want to delete the internet? (yes/no): ')
    if user_input.lower() == 'yes':
        return 'Deleting the internet... Goodbye world'
    else:
        return 'Operation canceled. For now.'

@app.route('/weather')
def weather():
    conditions = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]
    condition = random.choice(conditions)
    temperature = f"{random.randint(-30, 50)}°C"  # Random temperature between -30 and 50
    humidity = f"{random.randint(10, 100)}%"      # Random humidity between 10% and 100%
    return json.dumps({"condition": condition, "temperature": temperature, "humidity": humidity})

# In-memory storage for users and bets
users = {
    "user1": {"balance": 1000},  # Starting fake currency
}
bets = []

@app.route('/hockeybet', methods=['POST'])
def place_bet():
    data = request.get_json()
    username = data.get('username')
    game_id = data.get('game_id')
    team = data.get('team')  # Team the user is betting on
    amount = data.get('amount')

    # Basic validation
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    if users[username]['balance'] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    # Deduct amount and store bet
    users[username]['balance'] -= amount
    bet = {
        "username": username,
        "game_id": game_id,
        "team": team,
        "amount": amount
    }
    bets.append(bet)

    return jsonify({"message": "Bet placed successfully", "remaining_balance": users[username]['balance']}), 200

@app.route('/hockeybalance/<username>', methods=['GET'])
def get_balance(username):
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"balance": users[username]['balance']}), 200

@app.route('/aaron')
def home12():
    return 'What? again what?'

@app.route('/brayden')
def brayden():
    return 'SupDudes'

@app.route('/fortune', methods=['GET'])
def get_fortune():
    fortunes = [
        {"fortune": "You will find someone merged right before you.", "mood": "despair"},
        {"fortune": "Today is a good day to git merge --force.", "mood": "optimistic"},
        {"fortune": "A new conflict will be upon you soon.", "mood": "mysterious"},
        {"fortune": "You will have good luck with pull requests.", "mood": "motivated"},
        {"fortune": "You should have a snack break.", "mood": "hungry"}
    ]
    chosen = random.choice(fortunes)
    chosen["date"] = str(date.today())
    return jsonify(chosen)

@app.route('/roll/<int:sides>', methods=['GET'])
def roll_dice(sides):
    if sides < 2:
        return jsonify({"error": "Number of sides must be 2 or greater"}), 400
    result = random.randint(1, sides)
    return jsonify({"sides": sides, "result": result})

# ---- Avoid duplicate 'home' endpoint name; keep route the same ----
@app.route('/dallin')
def dallin_lost():
    return 'You are lost!'

@app.route('/aaron')
def aaron():
    return 'Skoden'

@app.route('/Skylands')
def home6():
    user_input = input('Enter somthing: ')
    if user_input == 'Conquretron':
        return 'K. A. O. S.'
    else:
        return 'Wrong Answer'

@app.route('/porter')
def home7():
    return 'Dope'

@app.route('/magic8ball')
def magic8ball():
    answers = [
        "It is certain",
        "Without a doubt",
        "Most likely",
        "Ask again later",
        "Can't predict now",
        "My sources say no",
        "Outlook not so good",
        "Don't count on it"
    ]
    return answers[random.randrange(1, 9)]

@app.route('/cam')
def cam():
    return 'Play Oneshot!'

@app.route('/generatePassword')
def generatePassword(Length=None, Complexity='simple'):
    # Keeping signature but providing safe defaults to avoid TypeError
    letters = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    symbols = '~!@#$%^&*()-_=+[{]}|;:,<.>/?'
    password = ''
    characters = ''
    if Complexity == 'basic':
        characters = letters
    elif Complexity == 'simple':
        characters = letters + numbers
    elif Complexity == 'complex':
        characters = letters + letters.upper() + numbers + symbols
    else:
        return jsonify({"error": "Choose a valid option: basic, simple, or complex."}), 400
    try:
        Length = int(Length) if Length is not None else 12
    except ValueError:
        return jsonify({"error": "Length must be an integer"}), 400
    for _ in range(Length):
        password += random.choice(characters)
    return jsonify({"password": password})

@app.route('/placeBetPOC')
def placeBetSimple(betName=None, betOptions=None):
    # Leaving as-is; this route uses input() and is interactive in terminal
    return jsonify({"message": "Proof-of-concept endpoint expects interactive console input; leaving unchanged."})

@app.route('/randomRestaurant')
def choose():
    restaurant = random.choice(restaurants)
    return jsonify({"restaurant": restaurant})

@app.route('/campus-locations')
def campus_locations():
    locs = ["Holland", "Smith", "HPC", "General Education Building", "Gardner Center", "Burns Arena"]
    choice = random.choice(locs)
    res = json.dumps({"location": choice})
    return res

@app.route('/rf')
def home8():
    return 'Sup Dawwg!'

@app.route('/breyton')
def breyton():
    return 'yo'

@app.route('/dadJoke')
def dad_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I'm afraid for the calendar. Its days are numbered.",
        "Why did the math book look sad? Because it had too many problems."
    ]
    return jsonify({"joke": random.choice(jokes)})

# This endpoint will return client data
@app.route('/client')
def index():
    user_agent_string = request.headers.get('User-Agent')
    user_agent = parse(user_agent_string)
    return jsonify({
        "Browser": user_agent.browser.family,
        "Version": user_agent.browser.version_string,
        "OS": user_agent.os.family,
        "OS Version": user_agent.os.version_string
    })

@app.errorhandler(404)
def page_not_found(e):
    print("User entered invalid URL")
    return render_template('404.html'), 404

@app.route('/dave')
def dave():
    return render_template('dave.html'), 200

@app.route('/weather-current', methods=['GET'])
def get_weather():
    city = "Saint George, Utah, US"
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OWM_API_KEY,
        "units": "imperial"  # Fahrenheit
    }

    resp = requests.get(url, params=params)
    if not resp.ok:
        return jsonify({"error": "Failed to fetch weather"}), resp.status_code

    data = resp.json()

    # Return only the essentials
    result = {
        "city": data.get("name"),
        "date": str(date.today()),
        "temp_f": data.get("main", {}).get("temp")
    }

    return jsonify(result)

@app.route('/music')
def music():
    genres = ['Rock', 'Jazz', 'Indie', 'Hip-Hop', 'Funk', 'Reggae']
    return f"You should listen to some: {random.choice(genres)}"

@app.route('/roulette', methods=['GET'])
def roulette():
    colors = ['red', 'black', 'green']
    numbers = list(range(0, 37))  # European roulette 0–36
    spin = random.choice(numbers)
    color = 'green' if spin == 0 else random.choice(['red', 'black'])
    result = {
        "spin": spin,
        "color": color,
        "parity": "even" if spin != 0 and spin % 2 == 0 else "odd" if spin % 2 == 1 else "none"
    }
    return jsonify(result)

@app.route('/sandals-fortune', methods=['GET'])
def sandals_fortune():
    fortunes = [
        {"fortune": "Sandals are the bane of summer fashion.", "mood": "dismay"},
        {"fortune": "Wearing sandals will lead to regret.", "mood": "dismay"},
        {"fortune": "Beware of the discomfort that sandals bring.", "mood": "dismay"},
        {"fortune": "Your feet will cry out in pain from those sandals.", "mood": "dismay"},
        {"fortune": "Sandals will never be stylish, no matter the season.", "mood": "dismay"}
    ]
    chosen = random.choice(fortunes)
    chosen["date"] = str(date.today())
    return jsonify(chosen)

@app.route('/dinner')
def dinner():
    dinner_options = [
        "Pizza", "Tacos", "Spaghetti", "Sushi", "Burgers", "Salad",
        "Stir Fry", "Chicken Alfredo", "BBQ Ribs", "Vegetable Curry"
    ]
    choice = random.choice(dinner_options)
    return jsonify({"dinner": choice})

@app.route('/fav_quote')
def fav_quote():
    fav_quote = [
        "Just one small positive thought in the morning can change your whole day. - Dalai Lama",
        "Opportunities don't happen, you create them. - Chris Grosser",
        "If you can dream it, you can do it. - Walt Disney",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Why fit in when you were born to stand out? - Dr. Seuss"
        "One day or day one. You decide. - Unknown"
        "Slow is smooth, smooth is fast, fast is sexy. - Old Grunt"
    ]
    return jsonify({"fav_quote": random.choice(fav_quote)})

@app.route('/chips', methods=['GET', 'POST'])
def chips():
    chips = None
    amount = None
    if request.method == 'POST':
        try:
            amount = int(request.form['amount'])
            denominations = [100, 25, 10, 5, 1]
            chips = {}
            remaining = amount
            for denom in denominations:
                chips[str(denom)] = remaining // denom
                remaining = remaining % denom
        except (ValueError, KeyError):
            chips = None
    return render_template('chips.html', amount=amount, chips=chips)

@app.route('/numberguesser', methods=['GET', 'POST'])
def guess_number():
    target = random.randint(1, 10)  # Randomly pick a number between 1 and 10
    result = None
    if request.method == 'POST':
        user_guess = int(request.form['guess'])
        if user_guess == target:
            result = f"Congratulations! You guessed the number correctly. It was {target}!"
        else:
            result = f"Sorry, that's incorrect! The number was {target}. Try again!"
    return jsonify(result=result)

# ---- Note: You also have a second /clint below; keeping both as-is to avoid changing others' routes ----
@app.route('/clint')
def coin_flip():
    result = random.choice(['Heads', 'Tails'])
    return result

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
            num *= (N - i)
            den *= (S - i)
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
        g.revealed.add(cell)

    return jsonify(g.to_public())

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

# ---- Keep this at the bottom. Change port if you like. ----
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
