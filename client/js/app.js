var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery');
require('purecss/build/pure-min.css');

let LoveLetterApp = React.createClass({
    getInitialState: function() {
        return {
            user: '',
            roomName: '',
            roomMembers: []
        };
    },

    handleLogin: function(username, roomName) {
        this.setState({
            user: username,
            roomName: roomName
        });
    },

    render: function() {
        let screen = <LoginScreen onLogin={this.handleLogin} />;

        if (this.state.user !== '' && this.state.roomName !== '') {
            screen = <WaitingRoomScreen username={this.state.user} roomName={this.state.roomName} />;
        }

        return (
            <div>
                {screen}
            </div>
        );
    }
});

let LoginScreen = React.createClass({
    getInitialState: function() {
        return {
            'username': '',
            'roomName': ''
        };
    },

    handleUsernameChange: function(e) {
        this.setState({'username': e.target.value});
    },

    handleRoomNameChange: function(e) {
        this.setState({'roomName': e.target.value});
    },

    joinRoom: function(roomName) {
        this.props.onLogin(this.state.username, roomName);
    },

    handleJoinRoomSubmit: function(e) {
        e.preventDefault();
        this.joinRoom(this.state.roomName);
    },

    handleCreateRoomSubmit: function(e) {
        e.preventDefault();
        $.post('/create')
        .done((response) => {
            if (response.result === "success") {
                this.joinRoom(response.room_name);
            }
        });
    },

    render: function() {
        return (
            <form className="pure-form pure-form-stacked" method="get">
                <fieldset>  
                    <label htmlFor="llLoginScreenUsername">What's your name?</label>
                    <input 
                        type="text"
                        id="llLoginScreenUsername"
                        placeholder="Your name"
                        value={this.state.username}
                        onChange={this.handleUsernameChange}
                    />
                    <hr/>
                    <label htmlFor="llLoginScreenRoom">Want to join a friend's room?</label>
                    <input
                        type="text"
                        id="llLoginScreenRoom"
                        placeholder="Room name"
                        value={this.state.roomName}
                        onChange={this.handleRoomNameChange}
                    />
                    <button
                        type="submit" 
                        className="pure-button pure-button-primary"
                        onClick={this.handleJoinRoomSubmit}
                    >
                        Join room
                    </button>
                    <hr/>
                    <label>Want to create a new room?</label>
                    <button 
                        type="submit"
                        className="pure-button pure-button-primary"
                        onClick={this.handleCreateRoomSubmit}
                    >
                        Create room
                    </button>
                </fieldset>
            </form>
        );
    }
});

let WaitingRoomScreen = React.createClass({
    render: function() {
        return (
            <h1>Hey, {this.props.username}. You are waiting for players in the room: {this.props.roomName}.</h1>
        );
    }
});

ReactDOM.render(
  <LoveLetterApp />,
  document.getElementById('llApp')
);