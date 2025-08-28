from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'
@app.route('/clint')
def home():
	return 'Hello, Clint!'
if __name__ == '__main__':
	app.run(debug=True)
