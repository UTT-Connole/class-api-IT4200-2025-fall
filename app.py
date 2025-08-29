from flask import Flask, render_template, request, jsonify
from user_agents import parse

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, Flask!'

#This endpoint will return client data
@app.route('/client')
def index():
	user_agent_string = request.headers.get('User-Agent')
	user_agent = parse(user_agent_string)
	return jsonify({
		"Browser": user_agent.browser.family,
		"Version": user_agent.browser.version_string,
		"OS": user_agent.os.family,
		"OS Version": user_agent.os.version_string
	})

@app.errorhandler(404)
def page_not_found(e):
	print("User entered invalid URL")
	return render_template('404.html'), 404
	

if __name__ == '__main__':
	app.run(debug=True)
