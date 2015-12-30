var React = require('react');
var io = require('socket.io-client');
var $ = require('jquery');

module.exports = React.createClass({
    getInitialState: function() {
        return {
            remoteRoomMembers: []
        };
    },

    loadRoomMembersFromServer: function() {
        $.get(`/room/${this.props.roomName}/members`)
        .done((data) => {
            if (data.result === 'success') {
                this.setState({
                    remoteRoomMembers: data.members
                });
            }
        });
    },

    componentDidMount: function() {
        this.loadRoomMembersFromServer();

        // set up a socket to listen to people joining/leaving the room
        let socket = io();
        socket.emit('join', {room_name: this.props.roomName, my_name: this.props.username});
        socket.on('player_joined', (data) => {
            this.handlePlayerJoined(data.player_name);
        });
        socket.on('player_left', (data) => {
            this.handlePlayerLeft(data.player_name);
        });
    },

    handlePlayerJoined: function(memberName) {
        this.setState({
            remoteRoomMembers: this.state.remoteRoomMembers.concat([memberName])
        });
    },

    handlePlayerLeft: function(memberName) {
        this.setState({
            remoteRoomMembers: this.state.remoteRoomMembers.filter((existingMember) => existingMember != memberName)
        });
    },

    render: function() {
        return (
            <div>
                <h1>Your room name is: {this.props.roomName}</h1>
                <h2>People in this room:</h2>
                <MemberList localPlayer={this.props.username} remoteRoomMembers={this.state.remoteRoomMembers} />
            </div>
        );
    }
});

let MemberList = React.createClass({
    render: function() {
        let memberNodes = this.props.remoteRoomMembers.map((member) => {
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