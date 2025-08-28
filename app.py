from flask import Flask

app = Flask(__name__)

@app.route('/gill')
def home():
	return 'test test'

if __name__ == '__main__':
	app.run(debug=True)
