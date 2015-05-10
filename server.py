import gevent
from flask import Flask, render_template
from flask_sockets import Sockets
import json

app = Flask(
	__name__,
	static_folder="client/static",
	template_folder="client/templates"
)
app.debug = True

sockets = Sockets(app)

@sockets.route('/waiting/<room>')
def command(ws, room):

	while ws is not None:
		# Sleep to prevent *contstant* context-switches.
		gevent.sleep()
		message = ws.receive()

		if message:
			print 'waiting room message received!'
			print room
			print message
			packet = json.loads(message)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/room', methods=['GET', 'POST'])
def room():
	return render_template('room.html')