from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/kasen')
def kasen():
	return 'please work'

if __name__ == '__main__':
	app.run(debug=True)
