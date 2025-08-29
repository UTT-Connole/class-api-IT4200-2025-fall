from flask import Flask, render_template, request, jsonify
import random
import json
from user_agents import parse

app = Flask(__name__)



@app.route('/kasen')
def kasen():
	return 'please work'

adjectives = ['Fluffy', 'Silly', 'Happy', 'Sleepy', 'Grumpy', 'Bouncy', 'Lazy', 'Sweet']
nouns = ['Paws', 'Whiskers', 'Shadow', 'Bean', 'Muffin', 'Cookie', 'Nugget', 'Pickle']


@app.route('/clint')
def home():
	return 'Hello, Clint!'

@app.route('/gill')
def home():
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
	return 'Please dont erase me'

@app.route('/brayden')
def brayden():
	return 'SupDudes'


@app.route('/bryson')
def bryson():
	return 'bingus'

@app.route('/gill')
def home():
	return 'my test app'

@app.route('/aaron')
def home():
	return 'What?'

@app.route('/brayden')
def brayden():
	return 'Sup Dudes'

@app.route('/Skylands')
def home():
	user_input = input('Enter somthing: ')
	if user_input == 'Conquretron':
		return 'K. A. O. S.'
	else:
		return 'Wrong Answer'

@app.route('/porter')
def home():
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
def home():
	return 'Sup Dawwg!'

@app.route('breyton')
def breyton():
	return 'yo'

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