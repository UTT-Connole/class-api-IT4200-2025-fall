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
def home():
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

@app.route('/roll/<int:sides>', methods=['GET'])
def roll_dice(sides):
        if sides < 2:
                return jsonify({"error": "Number of sides must be 2 or greater"}), 400
        result = random.randint(1,sides)
        return jsonify({
                "sides": sides,
                "result":result
        })

@app.route('/gill')
def home4():
	return 'my test app'

	return 'Hello, Flask!'

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

