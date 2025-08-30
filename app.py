from flask import Flask
import random
import json

app = Flask(__name__)



@app.route('/kasen')
def kasen():
	return 'please work'

adjectives = ['Fluffy', 'Silly', 'Happy', 'Sleepy', 'Grumpy', 'Bouncy', 'Lazy', 'Sweet']
nouns = ['Paws', 'Whiskers', 'Shadow', 'Bean', 'Muffin', 'Cookie', 'Nugget', 'Pickle']




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


@app.route('/pet-name')
def generate_pet_name():
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    return f'{adj} {noun}'


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

@app.route('/braydens')
def brayden():
	return 'Sup Dude'

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
>>>>>>> origin/main


@app.route('/campus-locations')
def campus_locations(): 
	locs = ["Holland", "Smith", "HPC"]
	choice = random.choice(locs)
	res = json.dumps({"location": choice})
	return res

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