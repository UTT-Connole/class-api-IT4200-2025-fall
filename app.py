from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/dallin')
def home():
	return 'Please dont erase me'

if __name__ == '__main__':
	app.run(debug=True)