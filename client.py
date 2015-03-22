def print_status(game):
    print "ayy lmao"

def print_options(game, player):
    print "[1] ayy [2] lmao"

player_names = ['a', 'b', 'c']
players = []
game = LoveLetterGame()
for p in player_names:
    pl = LoveLetterPlayer(p)
    players.add(pl)
    game.add_player(pl)

game.init_deck()
game.burn_card()
print_status(game)
while True:
    turn_player = game.get_turn_player()
    if turn_player == None:
        break
    game.draw_card(turn_player)
    if not turn_player.is_alive():
        continue
    print_options(game, turn_player)
    hand = turn_player.get_hand()
    while True:
        option = input("> ")
        if option < 0 or option >= len(hand):
            print "nayy lmao"
            continue
        break
    game.play_card(turn_player, hand[option])
