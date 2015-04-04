import gevent
from flask import Flask, render_template
from flask_sockets import Sockets
import json

app = Flask(__name__)
app.debug = True

sockets = Sockets(app)

@sockets.route('/command')
def command(ws):
	while ws is not None:
		# Sleep to prevent *contstant* context-switches.
		gevent.sleep()
		message = ws.receive()

		if message:
			print ws.handler
			print ws.current_app
			print ws.path
			print ws.protocol
			print ws.environ
			print message
			packet = json.loads(message)
			print 'opcode:', packet['opcode']