from flask import Flask

app = Flask(__name__)

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

<<<<<<< HEAD
@app.route('/porter')
def home():
	return 'Dope'
=======
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

@app.route('/rf')
def home():
	return 'Sup Dawg!'

if __name__ == '__main__':
	app.run(debug=True)
