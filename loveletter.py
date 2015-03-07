import random

import lovelettercards

class LoveLetterGame(object):

    def __init__(self):
        self._deck = []
        self._discard_pile = []
        self._players = []
        self.config = LoveLetterGameConfig()
        self._current_turn = 0

    def start(self):
        if len(players) < self.config.min_players or len(players) > self.config.max_players:
            raise LoveLetterGameException("Expected more than %s and less than %s players, got %s." % (self.config.min_players, self.config.max_players, len(players)))

        self.init_deck()
        self.discard_card()
        self.do_turn()

    def init_deck(self):
        self._deck = []
        for character, amount in self.config.num_cards_per_character:
            for _ in xrange(amount):
                self._deck.append(character())
        random.shuffle(self._deck)

    def discard_card(self):
        self._discard_pile.append(self._deck.pop())

    def do_turn(self):
        pass

    def add_player(self, player):
        if len(players) + 1 > self.config.max_players:
            raise LoveLetterGameException("Cannot add more players to game: already have %s players." % (self.config.max_players))

        self._players.append(player)

class LoveLetterGameConfig(object):

    # Do my public variables upset you? You can submit your feedback at http://swagify.net/
    def __init__(self):
        self.min_players = 3
        self.max_players = 4
        self.num_cards_per_character = { c : c.default_amount for c in lovelettercards.get_all_characters() }

    # reckon i should put another constructor here? nah

class LoveLetterGameException(Exception):
    pass

class LoveLetterPlayer(object):

    def __init__(self):
        self._played_cards = []
        self._hand = []

    def get_played_cards(self):
        return self._played_cards

    def get_hand(self):
        return self._hand
