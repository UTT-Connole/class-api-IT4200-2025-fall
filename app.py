from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/rf')
def home():
	return 'Sup Dawg!'

if __name__ == '__main__':
	app.run(debug=True)
