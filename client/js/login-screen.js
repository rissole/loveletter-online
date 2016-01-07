var React = require('react');
var $ = require('jquery');
require('purecss/build/pure-min.css');

module.exports = React.createClass({
    getInitialState: function() {
        return {
            'username': '',
            'roomName': '',
            'errors': {}
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

    validateRoomName: function() {
        let length = this.state.roomName.length
        if (length === 0) {
            return {
                'roomName': 'Enter a room name, dingus'
            };
        } else if (length > 32) {
            return {
                'roomName': 'That room name is a bit too long mate'
            };
        }
        return {};
    },

    validateUsername: function() {
        let length = this.state.username.length
        if (length === 0) {
            return {
                'username': 'Enter a username, dingus'
            };
        } else if (length > 32) {
            return {
                'username': 'That username is a bit too long mate'
            };
        }
        return {};
    },

    validateServerside: function(callback) {
        $.ajax(`/validateLogin?username=${this.state.username}&roomName=${this.state.roomName}`)
        .done((result) => {
            callback(result.errors);
        });
    },

    handleJoinRoomSubmit: function(e) {
        e.preventDefault();

        let errors = Object.assign(this.validateUsername(), this.validateRoomName());
        if (Object.keys(errors).length) {
            return this.setState({
                'errors': errors
            });
        }

        this.validateServerside((errors) => {
            if (Object.keys(errors).length) {
                return this.setState({
                    'errors': errors
                });
            } else {
                this.joinRoom(this.state.roomName);
            }
        })
    },

    handleCreateRoomSubmit: function(e) {
        e.preventDefault();
        
        let errors = this.validateUsername();
        if (Object.keys(errors).length) {
            this.setState({
                'errors': errors
            });
        } else {
            $.post('/create')
            .done((response) => {
                if (response.result === "success") {
                    this.joinRoom(response.room_name);
                }
            });
        }
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
                    <span style={{color: 'red'}}>{this.state.errors.username}</span>
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
                    <span style={{color: 'red'}}>{this.state.errors.roomName}</span>
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