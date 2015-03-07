class LoveLetterCard(object):
    default_amount = 0

class SoldierCard(LoveLetterCard):
    default_amount = 5

    def __init__(self):
        super(SoldierCard, self).__init__()

ALL_CHARACTERS = [
    SoldierCard
]

def get_all_characters():
    return ALL_CHARACTERS
