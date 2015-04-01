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

    def __repr__(self):
        return self.get_name()

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
                'filters': map(lambda c: c.get_name(), filter(lambda c: c != SoldierCard, ALL_CHARACTERS))
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

        if target.get_hand_first_card().get_name() == guess:
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

class ClownCard(LoveLetterCard):
    default_amount = 3

    def __init__(self, game):
        super(ClownCard, self).__init__(game)

    @staticmethod
    def get_name():
        return "Clown"

    @staticmethod
    def get_value():
        return 2

    @staticmethod
    def get_required_command_args():
        return {
            'target': {
                'type': ARG_TYPE_PLAYER,
                'filters': [
                    PLAYER_FILTER_NOT_SELF,
                    PLAYER_FILTER_NOT_DEAD
                ]
            }
        }

    def command_action(self, player, target):
        if not target.is_targetable():
            if all(not t.is_targetable() for t in player.get_game().get_players_excluding(player)):
                # you don't need a target if there are no targetable players.
                self.outcome_no_target(self, player)
                return
            else:
                raise LoveLetterInvalidCommand("Invalid target '%s': target is not targetable." % str(target))

        self.outcome_hit(player, target)

    def outcome_hit(self, player, target):
        self.get_notifier().send(self._game.get_all_players(), 'clown_hit', {'player': player, 'target': target})
        self.get_notifier().send_to_player(player, 'clown_reveal', {'target': target, 'hand': target.get_hand_first_card()})

    def outcome_no_target(self, player):
        self.get_notifier().send(self._game.get_all_players(), 'clown_no_target', {'player': player})


class KnightCard(LoveLetterCard):
    default_amount = 3

    def __init__(self, game):
        super(KnightCard, self).__init__(game)

    @staticmethod
    def get_name():
        return "Knight"

    @staticmethod
    def get_value():
        return 3

    @staticmethod
    def get_required_command_args():
        return {
            'target': {
                'type': ARG_TYPE_PLAYER,
                'filters': [
                    PLAYER_FILTER_NOT_SELF,
                    PLAYER_FILTER_NOT_DEAD
                ]
            }
        }

    def command_action(self, player, target):
        if not target.is_targetable():
            if all(not t.is_targetable() for t in player.get_game().get_players_excluding(player)):
                # you don't need a target if there are no targetable players.
                self.outcome_no_target(self, player)
                return
            else:
                raise LoveLetterInvalidCommand("Invalid target '%s': target is not targetable." % str(target))

        self.outcome_hit(player, target)

    def outcome_hit(self, player, target):
        self.get_notifier().send(self._game.get_all_players(), 'knight_hit', {'player': player, 'target': target})
        player_value = player.get_hand_first_card().get_value()
        target_value = target.get_hand_first_card().get_value()
        if player_value > target_value:
            target.lose()
        elif target_value > player_value:
            player.lose()
        else:
            self.get_notifier().send(self._game.get_all_players(), 'knight_equal', {'player': player, 'target': target})


    def outcome_no_target(self, player):
        self.get_notifier().send(self._game.get_all_players(), 'knight_no_target', {'player': player})

ALL_CHARACTERS = [
    SoldierCard,
    ClownCard,
    KnightCard
]

def get_all_characters():
    return ALL_CHARACTERS
