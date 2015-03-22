from loveletter import *
from lovelettercards import *
from notifiers import ConsoleNotifier

def get_valid_number(validator):
    while True:
        option = input("> ")
        if not validator(option):
            print "nayy lmao"
            continue
        break
    return option

LLG = LoveLetterGame(ConsoleNotifier())

players = [
    LoveLetterPlayer('blake', LLG),
    LoveLetterPlayer('dave', LLG),
    LoveLetterPlayer('jacob', LLG),
]

for p in players:
    LLG.add_player(p)

LLG.get_notifier().send(players, 'welcome', {'msg': 'welcome scrubs'})
LLG.start_new_round()

while True:
    LLG.get_notifier().send(players, 'deck', {'cards': [c.get_name() for c in LLG._deck]})
    LLG.get_notifier().send(players, 'burn', {'cards': [c.get_name() for c in LLG._burn_pile]})
    turn_player = LLG.get_turn_player()
    LLG.get_notifier().send(players, 'turn', {'player': str(turn_player)})
    LLG.draw_card(turn_player)
    hand = turn_player.get_hand()
    LLG.get_notifier().send([turn_player], 'hand', {'cards': [c.get_name() for c in hand]})
    option = get_valid_number(lambda opt: opt >= 0 and opt < len(hand))
    card = hand[option]
    args_required = card.get_required_command_args()
    returned_args = {}
    for arg_name, arg in args_required.iteritems():
        if arg['type'] == ARG_TYPE_PLAYER:
            choice_players = LLG.get_all_players()
            if PLAYER_FILTER_NOT_DEAD in arg['filters']:
                choice_players = filter(lambda p: p.is_alive(), choice_players)
            if PLAYER_FILTER_NOT_SELF in arg['filters']:
                choice_players = filter(lambda p: p != turn_player, choice_players)
            if len(choice_players) == 0:
                LLG.get_notifier().send([turn_player], 'choice_none')

            LLG.get_notifier().send([turn_player], 'choice_prompt', {'options': [str(p) for p in choice_players]})
            player_option = get_valid_number(lambda opt: opt >=0 and opt < len(choice_players))
            returned_args[arg_name] = choice_players[player_option]
        elif arg['type'] == ARG_TYPE_CHOICE:
            LLG.get_notifier().send([turn_player], 'choice_prompt', {'options': arg['filters']})
            opt = get_valid_number(lambda opt: opt >= 0 and opt < len(arg['filters']))
            returned_args[arg_name] = arg['filters'][opt]

    LLG.play_card(turn_player, hand[option], **returned_args)
