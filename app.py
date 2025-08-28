from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

@app.route('/Skylands')
def home():
	user_input = input('Enter somthing: ')
	if user_input == 'Conquretron':
		return 'K. A. O. S.'
	else:
		return 'Wrong Answer'

if __name__ == '__main__':
	app.run(debug=True)
