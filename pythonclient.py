from loveletter import *

players = [
    LoveLetterPlayer('blake'),
    LoveLetterPlayer('dave'),
    LoveLetterPlayer('jacob'),
]

LLG = LoveLetterGame()
for p in players:
    LLG.add_player(p)

print "Welcome: " + ", ".join(str(p) for p in players)
LLG.start_new_round()
print "Deck is: ", [str(c) for c in LLG._deck]
print "Burn is: ", [str(c) for c in LLG._burn_pile]

while True:
    turn_player = LLG.get_turn_player()
    print "It is %s's turn" % str(turn_player)
    LLG.draw_card(turn_player)
    print "Your hand is:", turn_player.get_hand()
    break