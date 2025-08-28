from flask import Flask
import random

app = Flask(__name__)

adjectives = ['Fluffy', 'Silly', 'Happy', 'Sleepy', 'Grumpy', 'Bouncy', 'Lazy', 'Sweet']
nouns = ['Paws', 'Whiskers', 'Shadow', 'Bean', 'Muffin', 'Cookie', 'Nugget', 'Pickle']


@app.route('/')
def home():
	return 'test test'


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



if __name__ == '__main__':
	app.run(debug=True)
