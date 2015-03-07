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
LLG.start()
print "Deck is: ", [str(c) for c in LLG._deck]
print "Burn is: ", [str(c) for c in LLG._burn_pile]