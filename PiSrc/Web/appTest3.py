from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def helloWorld():
	return 'hello world'

@app.route('/name')
def name():
	return '<h1>My Name is Ronaldo</h1>'

@app.route('/age')
def age():
	return '<h1>Ronaldo is 41. but he is still GOAT</h1>'

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
