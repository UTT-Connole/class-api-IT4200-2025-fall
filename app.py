from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/bryson')
def bryson():
	return 'bingus'

if __name__ == '__main__':
	app.run(debug=True)
