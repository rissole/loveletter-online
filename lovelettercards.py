class LoveLetterCard(object):
    """ Abstract card object """
    default_amount = 0

    def draw_action(self, player):
        """ Actions that occur from drawing the card """
        pass

    def discard_action(self, player):
        """ Actions that occur from discarding the card """
        pass

    def command_action(self, player, **kwargs):
        """ The action of playing the card from hand """
        pass

    @staticmethod
    def get_name():
        return "Unknown"

    def __str__(self):
        return type(self).get_name()

class LoveLetterInvalidCommand(Exception):
    """ You tried to do something a card has no business doing """
    pass

class SoldierCard(LoveLetterCard):
    default_amount = 5

    def __init__(self):
        super(SoldierCard, self).__init__()

    @staticmethod
    def get_name():
        return "Soldier"

    def command_action(self, player, target, guess):
        if not player.is_alive() or not target.is_alive():
            raise LoveLetterInvalidCommand()
        if type(target.get_hand_first_card()) == guess:
            return self.outcome_hit(player, target)
        else:
            return self.outcome_whiff(player, target, guess)

    def outcome_hit(self, player, target):
        # broadcast packets
        target.discard(self)

    def outcome_whiff(self, player, target, guess):
        # broadcast packets
        pass

ALL_CHARACTERS = [
    SoldierCard
]

def get_all_characters():
    return ALL_CHARACTERS
