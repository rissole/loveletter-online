ARG_TYPE_PLAYER = 0
ARG_TYPE_CHOICE = 1
PLAYER_FILTER_NOT_SELF = 1
PLAYER_FILTER_NOT_DEAD = 2

class LoveLetterCard(object):
    """ Abstract card object """
    default_amount = 0

    def __init__(self, game):
        # there are advantages to a LoveLetterPlayer.NO_PLAYER constant but I think this is fine.
        self._owner = None
        self._game = game

    def draw_action(self, player):
        self._owner = player

    def discard_action(self, player):
        """ Actions that occur from discarding the card """
        pass

    def command_action(self, player, **kwargs):
        """ The action of playing the card from hand """
        pass

    @staticmethod
    def get_name():
        return "Unknown"

    @staticmethod
    def get_value():
        return 0

    @staticmethod
    def get_required_command_args():
        return {}

    def get_owner(self):
        return self._owner

    def get_game(self):
        return self._game

    def get_notifier(self):
        """ Convenience method """
        return self._game.get_notifier()

class LoveLetterInvalidCommand(Exception):
    """ You tried to do something a card has no business doing """
    pass

class SoldierCard(LoveLetterCard):
    default_amount = 5

    def __init__(self, game):
        super(SoldierCard, self).__init__(game)

    @staticmethod
    def get_name():
        return "Soldier"

    @staticmethod
    def get_value():
        return 1

    # oh BOY Blake this is gonna require some documentation or a complicated builder
    # eventually the latter but let's just do json-like hackery for now
    @staticmethod
    def get_required_command_args():
        return {
            'target': {
                'type': ARG_TYPE_PLAYER,
                'filters': [
                    PLAYER_FILTER_NOT_SELF,
                    PLAYER_FILTER_NOT_DEAD
                ]
            },
            'guess': {
                'type': ARG_TYPE_CHOICE,
                'filters': map(lambda c: c.get_name(), ALL_CHARACTERS)
            }
        }

    def command_action(self, player, target, guess):
        if not target.is_targetable():
            if all(not t.is_targetable() for t in player.get_game().get_players_excluding(player)):
                # you don't need a target if there are no targetable players.
                self.outcome_no_target(self, player)
                return
            else:
                raise LoveLetterInvalidCommand("Invalid target '%s': target is not targetable." % str(target))

        if type(target.get_hand_first_card()) == guess:
            self.outcome_hit(player, target, guess)
        else:
            self.outcome_whiff(player, target, guess)

    def outcome_hit(self, player, target, guess):
        self.get_notifier().send(self._game.get_all_players(), 'soldier_hit', {'player': player, 'target': target, 'guess': guess})
        target.lose()

    def outcome_whiff(self, player, target, guess):
        self.get_notifier().send(self._game.get_all_players(), 'soldier_whiff', {'player': player, 'target': target, 'guess': guess})

    def outcome_no_target(self, player):
        self.get_notifier().send(self._game.get_all_players(), 'soldier_no_target', {'player': player})

ALL_CHARACTERS = [
    SoldierCard
]

def get_all_characters():
    return ALL_CHARACTERS
