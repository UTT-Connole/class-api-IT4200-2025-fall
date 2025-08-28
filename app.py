from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/dallin')
def home():
	return 'You are lost!'

@app.route('/brayden')
def brayden():
	return 'SupDudes'

@app.route('/bryson')
def bryson():
	return 'bingus'

if __name__ == '__main__':
	app.run(debug=True)
