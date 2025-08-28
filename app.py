from flask import Flask

app = Flask(__name__)

@app.route('/gill')
def home():
	return 'my test app'

@app.route('/brayden')
def brayden():
	return 'Sup Dudes'

@app.route('/braydens')
def brayden():
	return 'Sup Dude'

@app.route('/Skylands')
def home():
	user_input = input('Enter somthing: ')
	if user_input == 'Conquretron':
		return 'K. A. O. S.'
	else:
		return 'Wrong Answer'

@app.route('/cam')
def cam():
	return 'Play Oneshot!'

if __name__ == '__main__':
	app.run(debug=True)
