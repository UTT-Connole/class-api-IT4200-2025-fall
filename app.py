from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'test test'

@app.route('/aaron')
def aaron():
	return 'Skoden'

if __name__ == '__main__':
	app.run(debug=True)
