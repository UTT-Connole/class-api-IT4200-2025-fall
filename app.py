from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/dallin')
def home():
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

if __name__ == '__main__':
	app.run(debug=True)