var React = require('react');
var io = require('socket.io-client');
var $ = require('jquery');

module.exports = React.createClass({
    getInitialState: function() {
        return {
            roomMembers: [],
            secondsRemaining: 0
        };
    },

    loadRoomMembersFromServer: function() {
        $.get(`/room/${this.props.roomName}/members`)
        .done((data) => {
            if (data.result === 'success') {
                this.setState({
                    roomMembers: data.members
                });
            }
        });
    },

    componentDidMount: function() {
        this.loadRoomMembersFromServer();

        // set up a socket to listen to people joining/leaving the room
        this.socket = io();
        this.socket.emit('join', {room_name: this.props.roomName, my_name: this.props.username});
        this.socket.on('player_joined', (data) => {
            this.handlePlayerJoined(data.player_name);
        });
        this.socket.on('player_left', (data) => {
            this.handlePlayerLeft(data.player_name);
        });
    },

    componentWillUnmount: function() {
        clearInterval(this.interval);
    },

    handlePlayerJoined: function(memberName) {
        this.setState({
            roomMembers: this.state.roomMembers.concat([memberName]),
        });
    },

    handlePlayerLeft: function(memberName) {
        this.setState({
            roomMembers: this.state.roomMembers.filter((existingMember) => existingMember != memberName)
        });
    },

    setCountdown: function(seconds) {
        this.setState({
            secondsRemaining: seconds
        });
        this.interval = setInterval(this.tick, 1000);
    },

    tick: function() {
        this.setState({secondsRemaining: this.state.secondsRemaining - 1});
        if (this.state.secondsRemaining <= 0) {
          clearInterval(this.interval);
          this.handleCountdownComplete();
        }
    },

    handleCountdownComplete: function() {
        this.props.onRoomReady();
    },

    render: function() {
        return (
            <div>
                <h1>Your room name is: {this.props.roomName}</h1>
                <h2>People in this room:</h2>
                <MemberList roomMembers={this.state.roomMembers} />
                <Countdown secondsRemaining={this.state.secondsRemaining} />
            </div>
        );
    }
});

let MemberList = React.createClass({
    render: function() {
        let memberNodes = this.props.roomMembers.map((member) => {
            return (
                <Member key={member} name={member} />
            );
        });
        return (
            <ul id="players">
                {memberNodes}
            </ul>
        );
    }
});

let Member = (props) => <li>{props.name}</li>;

let Countdown = (props) => 
    <h1 
    style={{
        display: props.secondsRemaining > 0 ? "block" : "none"
    }}>
        {props.secondsRemaining}
    </h1>