from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/brayden')
def brayden():
	return 'Sup Dudes'

@app.route('/braydens')
def brayden():
	return 'Sup Dude'

if __name__ == '__main__':
	app.run(debug=True)
