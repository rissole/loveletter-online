var React = require('react');
var ReactDOM = require('react-dom');
var LoginScreen = require('./login-screen');
var WaitingRoomScreen = require('./waiting-room-screen');

let LoveLetterApp = React.createClass({
    getInitialState: function() {
        return {
            user: null,
            room: null,
            roomReady: false
        };
    },

    handleLogin: function(username, roomName) {
        this.setState({
            user: username,
            roomName: roomName
        });
    },

    handleRoomReady: function() {
        this.setState({roomReady: true})
    },

    render: function() {
        let screen;

        if (this.state.user === null || this.state.roomName === null) {
            screen = <LoginScreen onLogin={this.handleLogin} />;
        } else if (this.state.user !== null && this.state.roomName !== null && this.state.roomReady !== true) {
            screen = <WaitingRoomScreen 
                        username={this.state.user}
                        roomName={this.state.roomName}
                        onRoomReady={this.handleRoomReady} />;
        }
        else if (this.state.roomReady === true) {
            screen = <h1>YOU ARE READY TO PLAY THE GAME</h1>
        }

        return (
            <div>
                {screen}
            </div>
        );
    }
});

ReactDOM.render(
  <LoveLetterApp />,
  document.getElementById('llApp')
);