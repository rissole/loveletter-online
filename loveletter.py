import random

import lovelettercards

class LoveLetterGame(object):

    def __init__(self):
        self._deck = []
        self._burn_pile = []
        self._players = []
        self.config = LoveLetterGameConfig()
        self._current_turn = 0

    def start(self):
        players = self._players
        if len(players) < self.config.min_players or len(players) > self.config.max_players:
            raise LoveLetterGameException("Expected more than %s and less than %s players, got %s." % (self.config.min_players, self.config.max_players, len(players)))

        self.init_deck()
        self.burn_deck_card()

    def init_deck(self):
        self._deck = []
        for character, amount in self.config.num_cards_per_character.iteritems():
            for _ in xrange(amount):
                self._deck.append(character())
        random.shuffle(self._deck)

    def burn_deck_card(self):
        self._burn_pile.append(self._deck.pop())

    def add_player(self, player):
        players = self._players
        if len(players) + 1 > self.config.max_players:
            raise LoveLetterGameException("Cannot add more players to game: already have %s players." % (self.config.max_players))

        self._players.append(player)

    def play_card(self, player, card, **command_args):
        card.command_action(player, **command_args)
        player.discard(card)

class LoveLetterGameException(Exception):
    pass

class LoveLetterPlayer(object):

    def __init__(self, profile):
        self._played_cards = []
        self._hand = []
        self._alive = True
        # profile is some unique identifier for this player
        self._profile = profile

    def get_played_cards(self):
        return self._played_cards

    def get_hand(self):
        return self._hand

    def get_hand_first_card(self):
        return self._hand[0]

    def is_alive(self):
        return self._alive

    def discard(self, card):
        if card not in self._hand:
            raise LoveLetterGameException("Tried to discard card %s, but player %s doesn't have it in hand" % (str(card), str(self)))
        self._played_cards.append(card)
        self._hand.remove(card)
        card.discard_action(self)

    def get_profile(self):
        return self._profile

    def __str__(self):
        return self._profile

class LoveLetterGameConfig(object):

    # Do my public variables upset you? You can submit your feedback at http://swagify.net/
    def __init__(self):
        self.min_players = 3
        self.max_players = 4
        self.num_cards_per_character = { c : c.default_amount for c in lovelettercards.get_all_characters() }

    # reckon i should put another constructor here? nah
