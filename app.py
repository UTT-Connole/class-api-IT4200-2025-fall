from flask import Flask

app = Flask(__name__)

@app.route('/gill')
def home():
    user_input = input('What is your quest?')
    if user_input == 'We seek the Holy Grail':
        return "You may pass"
    else:
	    return 'You are doomed'

if __name__ == '__main__':
	app.run(debug=True)
