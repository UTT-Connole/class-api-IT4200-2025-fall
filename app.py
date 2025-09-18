from flask import Flask, render_template, request, jsonify
import random
import json
import os
import requests
from user_agents import parse
from datetime import date

app = Flask(__name__)
OWM_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


@app.route('/')
def home():
	return render_template('index.html'), 200


@app.route('/pokemon')
def pokemon():
	return jsonify({"pokemon": "Jigglypuff"})

@app.route('/kasen')
def kasen():
	return 'please work'


@app.route('/kasen')
def kasen():
	return 'please work'
adjectives = ['Fluffy', 'Silly', 'Happy', 'Sleepy', 'Grumpy', 'Bouncy', 'Lazy', 'Sweet']
nouns = ['Paws', 'Whiskers', 'Shadow', 'Bean', 'Muffin', 'Cookie', 'Nugget', 'Pickle']


@app.route('/clint')
def home1():
	return 'Hello, Clint!'

@app.route('/gill')
def home2():
    user_input = input('What is your quest?')
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
def home3():
	return 'Please dont erase me'

#realized that I didn't follow the instructions. Here's a random weather conditions generator
@app.route('/weather')
def weather():
	conditions = [
		{"condition": "Sunny", "temperature": "25°C", "humidity": "40%"},
		{"condition": "Rainy", "temperature": "18°C", "humidity": "85%"},
		{"condition": "Windy", "temperature": "20°C", "humidity": "50%"},
		{"condition": "Cloudy", "temperature": "22°C", "humidity": "60%"},
		{"condition": "Snowy", "temperature": "-5°C", "humidity": "70%"}
	]
	return random.choice(conditions)

@app.route('/aaron')
def home():
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



@app.route('/gill')
def home4():
	return 'my test app'

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


@app.route('/cam')
def cam():
	return 'Play Oneshot!'
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

restaurants = [
    "Chipotle",
    "Chick-fil-A",
    "Subway",
    "Olive Garden",
    "Five Guys",
    "Panera Bread"
]

@app.route('/randomRestaurant')
def choose():
    restaurant = random.choice(restaurants)
    return jsonify({"restaurant": restaurant})


@app.route('/campus-locations')
def campus_locations(): 
	locs = ["Holland", "Smith", "HPC", "General Education Building", "Gardner Center"]
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
	

@app.route('/aaron')
def aaron():
	return 'Skoden'

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




if __name__ == '__main__':
	app.run(debug=True)

@app.route('/dadJokeGenerator')
def dad_joke_generator():
	jokes = [
		"Why don't scientists trust atoms? Because they make up everything!",
		"What do you call fake spaghetti? An impasta!",
		"Why did the scarecrow win an award? Because he was outstanding in his field!",
		"I'm on a whiskey diet. I've lost three days already!",
		"Why don't skeletons fight each other? They don't have the guts."
	]
	return jsonify({"joke": random.choice(jokes)})

@app.route('/clint')
def spin_wheel():
    number = random.randint(0, 36)
    color = 'Green' if number == 0 else ('Red' if number % 2 == 0 else 'Black')
    return number, color

def get_payout(bet_type, bet_value, result_number, result_color):
    if bet_type == 'number':
        return 35 if bet_value == result_number else -1
    elif bet_type == 'color':
        return 1 if bet_value.lower() == result_color.lower() else -1
    else:
        return -1

def main():
    print("🎲 Welcome to Python Roulette!")
    balance = 100

    while balance > 0:
        print(f"\nYour current balance: ${balance}")
        bet_type = input("Bet on 'number' or 'color': ").strip().lower()

        if bet_type == 'number':
            try:
                bet_value = int(input("Choose a number between 0 and 36: "))
                if not 0 <= bet_value <= 36:
                    print("Invalid number. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Try again.")
                continue
        elif bet_type == 'color':
            bet_value = input("Choose a color (Red/Black): ").strip().capitalize()
            if bet_value not in ['Red', 'Black']:
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
        print(f"\n🎡 The wheel landed on {result_number} ({result_color})")

        payout_multiplier = get_payout(bet_type, bet_value, result_number, result_color)
        winnings = wager * payout_multiplier if payout_multiplier > 0 else 0
        balance += winnings - wager

        if payout_multiplier > 0:
            print(f"🎉 You won ${winnings}!")
        else:
            print("😢 You lost your wager.")

        if balance <= 0:
            print("💸 You're out of money! Game over.")
            break

        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()


