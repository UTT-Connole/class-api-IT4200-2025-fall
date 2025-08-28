from flask import Flask
import random

app = Flask(__name__)

adjectives = ['Fluffy', 'Silly', 'Happy', 'Sleepy', 'Grumpy', 'Bouncy', 'Lazy', 'Sweet']
nouns = ['Paws', 'Whiskers', 'Shadow', 'Bean', 'Muffin', 'Cookie', 'Nugget', 'Pickle']


@app.route('/gill')
def home():
    user_input = input('What is your quest?')
    if user_input == 'We seek the Holy Grail':
        return "You may pass"
    else:
	    return 'You are doomed'


@app.route('/dallin')
def home():
	return 'You are lost!'

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

if __name__ == '__main__':
	app.run(debug=True)
