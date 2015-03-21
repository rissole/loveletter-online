from loveletter import *
from lovelettercards import *

def get_valid_number(validator):
    while True:
        option = input("> ")
        if not validator(option):
            print "nayy lmao"
            continue
        break
    return option

LLG = LoveLetterGame()

players = [
    LoveLetterPlayer('blake', LLG),
    LoveLetterPlayer('dave', LLG),
    LoveLetterPlayer('jacob', LLG),
]

for p in players:
    LLG.add_player(p)

print "Welcome: " + ", ".join(str(p) for p in players)
LLG.start_new_round()

while True:
    print "Deck is: ", [str(c) for c in LLG._deck]
    print "Burn is: ", [str(c) for c in LLG._burn_pile]
    turn_player = LLG.get_turn_player()
    print "It is %s's turn" % str(turn_player)
    LLG.draw_card(turn_player)
    hand = turn_player.get_hand()
    print "Your hand is:", hand
    option = get_valid_number(lambda opt: opt >= 0 and opt < len(hand))
    card = hand[option]
    args_required = card.get_required_command_args()
    returned_args = {}
    for arg_name, arg in args_required.iteritems():
        if arg['type'] == ARG_TYPE_PLAYER:
            players = LLG.get_all_players()
            if PLAYER_FILTER_NOT_DEAD in arg['filters']:
                players = filter(lambda p: p.is_alive(), players)
            if PLAYER_FILTER_NOT_SELF in arg['filters']:
                players = filter(lambda p: p != turn_player, players)
            if len(players) == 0:
                print "no choices lmao"

            print "choose a player: ", players
            player_option = get_valid_number(lambda opt: opt >=0 and opt < len(players))
            returned_args[arg_name] = players[player_option]
        elif arg['type'] == ARG_TYPE_CHOICE:
            print "pick one: ", arg['filters']
            opt = get_valid_number(lambda opt: opt >= 0 and opt < len(arg['filters']))
            returned_args[arg_name] = arg['filters'][opt]

    LLG.play_card(turn_player, hand[option], **returned_args)
