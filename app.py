from flask import Flask, render_template, request, jsonify
import random
import json
from user_agents import parse
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html'), 200

@app.route('/kasen')
def kasen():
	return render_template('kasen.html'), 200

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

@app.route('/aaron')
def home5():
	return 'What?'

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
	

if __name__ == '__main__':
	app.run(debug=True)