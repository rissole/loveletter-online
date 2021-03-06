import flask
import json
import flask_socketio
import loveletter

app = flask.Flask(
    __name__,
    static_folder="client/public",
    template_folder="client/templates"
)
app.debug = True
with open('app_secret') as f:
    app.config['SECRET_KEY'] = f.read()

socketio = flask_socketio.SocketIO(app)

# room name -> room map
ROOMS = {}

def json_error(message):
    print('error', message)
    return flask.jsonify(
        result='error',
        message=message
    )

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    name = 'memes'
    if name not in ROOMS:
        ROOMS[name] = Room(name, socketio)
    return flask.jsonify(
        result='success',
        room_name=name
    )

@app.route('/room/<room_name>/config', methods=['GET'])
def get_config_for_room(room_name):
    if room_name not in ROOMS:
        return json_error('Room doesn\'t exist'), 404

    config = ROOM[room_name].get_game().config
    return flask.jsonify(
        minPlayers=config.min_players,
        maxPlayers=config.max_players,
        numCardsPerCharacter=config.num_cards_per_character,
        roundsToWin=config.rounds_to_win
    )

@app.route('/room/<room_name>/members', methods=['GET'])
def get_room_members(room_name):
    if room_name not in ROOMS:
        return json_error('Room doesn\'t exist'), 404
    return flask.jsonify(
        result='success',
        members=[p.get_name() for p in ROOMS[room_name].get_game().get_all_players()]
    )

@app.route('/validateLogin', methods=['GET'])
def validateLogin():
    username = flask.request.args.get('username', '')
    room_name = flask.request.args.get('roomName', '')
    errors = {}

    if username == '' or room_name == '':
        errors['username'] = errors['roomName'] = 'You gotta send me username and roomName, kay?'
    elif room_name not in ROOMS:
        errors['roomName'] = 'That room doesn\'t exist, you probably made a typo, haha.'
    elif not ROOMS[room_name].is_full():
        errors['roomName'] = 'That room is full, gotta be quick!'
    elif username in ROOMS[room_name].get_member_names():
        errors['username'] = 'A user with that name is already in that room... be original!'

    return flask.jsonify({
        'errors': errors
    })

# triggered when someone begins to wait in a room
@socketio.on('join')
def join(data):
    room_name = data['room_name']
    player_name = data['my_name']

    if room_name not in ROOMS:
        return json_error('Room doesn\'t exist'), 404

    flask_socketio.join_room(room_name)
    create_room_player(flask.request.sid, player_name, room_name)

@socketio.on('disconnect')
def on_disconnect(): 
    matching_rooms = [ROOMS[room_name] for room_name in flask_socketio.rooms() if room_name in ROOMS]
    if len(matching_rooms) == 0:
        return json_error('Room doesn\'t exist'), 404
    room = matching_rooms[0]
    player_name = room.get_name_for_socket_id(flask.request.sid)
    room.remove_member(player_name)

    room.send_to_all('player_left', {
        'player_name': player_name
    })

    print 'room',room.get_name(),'lost player',(player_name, flask.request.sid)

def create_room_player(socket_id, player_name, room_name):
    room = ROOMS[room_name]

    #broadcast join to existing members
    room.send_to_all('player_joined', {
        'player_name': player_name
    })

    room.add_member(
        socket_id,
        loveletter.LoveLetterPlayer(player_name, room.get_game())
    )

    print 'room',room.get_name(),'just got new player',(player_name, socket_id)

# lol, class room, nice funny
class Room(object):

    def __init__(self, name, socketio):
        self._name = name
        self._socketio = socketio
        self._game = loveletter.LoveLetterGame(self)

        # map of player names -> socket ids
        self._player_sockets = {}

    def get_name(self):
        return self._name

    def add_member(self, socket_id, love_letter_player):
        self._player_sockets[love_letter_player.get_name()] = socket_id
        self._game.add_player(love_letter_player)

    def remove_member(self, player_name):
        del self._player_sockets[player_name]
        self._game.remove_player(self._game.get_player(player_name))

    def get_member_names(self):
        return self._player_sockets.keys()

    def get_num_sockets(self):
        return len(self._player_sockets)

    def get_socket_id_for_player(self, player):
        return self._player_sockets[player.get_name()]

    def get_name_for_socket_id(self, socket_id):
        return next(name for name, sid in self._player_sockets.iteritems() if socket_id == sid)

    def get_game(self):
        return self._game

    def is_full(self):
        return len(self._game.get_all_players()) >= self._game.get_config().max_players

    # notifier part

    def _send_to_socketio_room(self, socketio_room_id, opcode, msg_args):
        self._socketio.emit(opcode, msg_args, room=socketio_room_id)

    def send_to_player(self, player, opcode, msg_args):
        socket_id = self.get_socket_id_for_player(player)
        self._send_to_socketio_room(socket_id, opcode, msg_args)

    def send(self, players, opcode, msg_args):
        if len(players) == self.get_num_sockets():
            return self.send_to_all(opcode, msg_args)
            
        for p in players:
            self.send_to_player(p, opcode, msg_args)

    def send_to_all(self, opcode, msg_args):
        self._send_to_socketio_room(self.get_name(), opcode, msg_args)

if __name__ == '__main__':
    socketio.run(app)