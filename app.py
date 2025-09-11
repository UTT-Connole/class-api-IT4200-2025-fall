from flask import Flask, render_template, request, jsonify
import random
import json
import os
import requests
from user_agents import parse
from datetime import date
import random

app = Flask(__name__)
OWM_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

#Moved global variables to top for organization
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

#Unlivable Realestate Endpoints

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
	humidity = f"{random.randint(10, 100)}%"  # Random humidity between 10% and 100%
	return json.dumps({"condition": condition, "temperature": temperature, "humidity": humidity})

from flask import Flask, request, jsonify

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)



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
        result = random.randint(1,sides)
        return jsonify({
                "sides": sides,
                "result":result
        })


        return 'Hello, Flask!'

@app.route('/dallin')
def home():
	return 'You are lost!'

@app.route('/aaron')
def home():
	return 'What? again what?'

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
	return answers[random.randrange(1,9)]

@app.route('/cam')
def cam():
	return 'Play Oneshot!'

@app.route('/generatePassword')
def generatePassword(Length, Complexity):
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
		print("Choose a valid option: basic, simple, or complex.")
		return -1
	for i in range(Length):
		password += random.choice(characters)
	return jsonify({"password": password})

@app.route('/placeBetPOC') #meant to ba functioning proof of concept. Automating this without input() function can be done later.
def placeBetSimple(betName, betOptions): #options is a list of choices players can bet on. 
	#currently assumes 2 players, but should support more here or on a more automated version.
	bets = [] #stores player bets
	betAmounts = [] #stores amounts players bets
	print("Here are your betting options:") 
	for j in betOptions: #print all options in betOptions
		print(j)
	for i in range(1,3): #loops for 2 players
		loop = True
		while loop == True: #loop until player enters valid betting option
			bet = input(f"player {i}, who are you betting on winning? ")
			if bet in betOptions:
				bets.append(bet)
				print("Bet Stored")
				loop = False
			else:
				print("Try Again. Please enter a valid option listed above.")
		loop = True
		while loop == True: #loop until player enters a number above 0
			betAmount = input(f"player {i}, how much do you bet on {bet}? ")
			if int(betAmount) > 0:
				betAmounts.append(betAmount)			
				print("Bet Amount Stored")
				loop = False
			else:
				print("Please enter a valid number above 0.")
	return jsonify({"BetName": betName, #returns player choice and how much they bet in json
				 "p1Choice": bets[0], 
				 "p1Bet": betAmounts[0],
				 "p2Choice": bets[1],
				 "p2Bet": betAmounts[1]})

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

#This endpoint will return client data
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

@app.route('/aaron')
def aaron():
	return 'Skoden'

@app.route('/music')
def music():
    genres = [
        'Rock',
        'Jazz',
        'Indie',
        'Hip-Hop',
        'Funk',
        'Reggae'
    ]
    return f"You should listen to some: {random.choice(genres)}"


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
        "Pizza",
        "Tacos",
        "Spaghetti",
        "Sushi",
        "Burgers",
        "Salad",
        "Stir Fry",
        "Chicken Alfredo",
        "BBQ Ribs",
        "Vegetable Curry"
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


@app.route('/blackjack')
def get_card_count_value(card):
    if card in [2, 3, 4, 5, 6]:
        return 1
    elif card in [7, 8, 9]:
        return 0
    elif card in [10, 'J', 'Q', 'K', 'A']:
        return -1
    else:
        return 0

def create_deck():

    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    return deck




@app.route('/clint')
def coin_flip():
    result = random.choice(['Heads', 'Tails'])
    print(f"The coin landed on: {result}")
    return result




def calculate_hand_value(hand):
    value = 0
    aces = 0

    for card in hand:
        if card in ['J', 'Q', 'K']:
            value += 10
        elif card == 'A':
            aces += 1
            value += 11  
        else:
            value += card

    
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

def display_hand(hand, name, hide_first_card=False):
    if hide_first_card:
        print(f"{name}'s hand: [?, {hand[1]}]")
    else:
        print(f"{name}'s hand: {hand} (Total: {calculate_hand_value(hand)})")


def blackjack_game():
    print("🃏 Welcome to Blackjack with Card Counting!")

    deck = create_deck()
    running_count = 0

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    for card in player_hand + dealer_hand:
        running_count += get_card_count_value(card)

    display_hand(player_hand, "Player")
    display_hand(dealer_hand, "Dealer", hide_first_card=True)
    print(f"🧮 Running count: {running_count}\n")

    while calculate_hand_value(player_hand) < 21:
        move = input("Hit or stand? (h/s): ").lower()
        if move == 'h':
            card = deck.pop()
            player_hand.append(card)
            running_count += get_card_count_value(card)

            display_hand(player_hand, "Player")
            print(f"🧮 Running count: {running_count}\n")

            if calculate_hand_value(player_hand) > 21:
                print("💥 You busted! Dealer wins.")
                return
        elif move == 's':
            break
        else:
            print("Invalid input. Please enter 'h' or 's'.")

    print("\nDealer's turn:")
    display_hand(dealer_hand, "Dealer")
    while calculate_hand_value(dealer_hand) < 17:
        card = deck.pop()
        dealer_hand.append(card)
        running_count += get_card_count_value(card)
        display_hand(dealer_hand, "Dealer")
        print(f"🧮 Running count: {running_count}\n")

    print("\n🎯 Final Results:")
    display_hand(player_hand, "Player")
    display_hand(dealer_hand, "Dealer")
    print(f"🧮 Final running count: {running_count}\n")

    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)

    if dealer_total > 21:
        print("✅ Dealer busted. You win!")
    elif player_total > dealer_total:
        print("✅ You win!")
    elif player_total < dealer_total:
        print("❌ Dealer wins.")
    else:
        print("🤝 It's a tie!")

blackjack_game()

@app.route('/gatcha')
def gatcha():
    gatcha_balls = {
        "SSR": "Princess Takanuma",
        "R": "Dale",
        "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSR": "Super Ultra Mega Mecha Battle Suit Zeta",
        "C": "Stinky Poo Poo"
    }

    weights = {
        "SSR": 5,  # 5% chance
        "R": 20,   # 20% chance
        "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSR": 1,  # super rare, 1% chance
        "C": 74    # common, 74% chance
    }

    pull = random.choices(
        population=list(gatcha_balls.values()),
        weights=[weights[key] for key in gatcha_balls.keys()],
        k=1
    )[0]

    return pull

if __name__ == '__main__':
	app.run(debug=True)

