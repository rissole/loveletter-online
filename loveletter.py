import random

import lovelettercards

class LoveLetterGame(object):

    def __init__(self):
        self._deck = []
        self._burn_pile = []
        self._players = []
        self.config = LoveLetterGameConfig()
        self._current_turn = 0

    def get_current_turn(self):
        return self._current_turn

    def get_turn_player(self):
        return self._players[self._current_turn % len(self._players)]

    def get_all_players(self):
        return self._players

    def get_players_excluding(self, *exclude):
        return filter(lambda p: p not in exclude, self._players)

    def get_live_players(self):
        return filter(lambda p: p.is_alive(), self._players)

    def get_live_players_excluding(self, *exclude):
        return filter(lambda p: p.is_alive() and p not in exclude, self._players)

    def start_new_round(self):
        players = self._players
        if len(players) < self.config.min_players or len(players) > self.config.max_players:
            raise LoveLetterGameException("Expected more than %s and less than %s players, got %s." % (self.config.min_players, self.config.max_players, len(players)))
        self._current_turn = 0

        self.init_deck()
        self.burn_deck_card()
        for p in players:
            p.reset()
            self.draw_card(p)

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
        self.next_turn()

    def draw_card(self, player):
        if len(self._deck) == 0:
            raise LoveLetterGameException("%s tried to draw a card but the deck is empty" % str(player))
        card = self._deck.pop()
        player.draw(card)

    def next_turn(self):
        self._current_turn += 1
        # no cards left? let's do the compare step
        if len(self._deck) == 0:
            winner = max(p in self._players, key=lambda p: p.get_hand_first_card().get_value())
            for p in self.get_live_players_excluding(winner):
                p.lose()
        # if priestess is up on next player, remove immunity now.. well this will be the aura system


class LoveLetterGameException(Exception):
    pass

class LoveLetterPlayer(object):

    def __init__(self, profile, game):
        self.reset()
        # profile is some unique identifier for this player
        self._profile = profile
        self._game = game

    def reset(self):
        """ Reset player as if starting a new round """
        self._played_cards = []
        self._hand = []
        self._alive = True

    def get_played_cards(self):
        return self._played_cards

    def get_hand(self):
        return self._hand

    def get_hand_first_card(self):
        return self._hand[0]

    def is_alive(self):
        return self._alive

    def discard(self, card, no_action=False):
        if card not in self._hand:
            raise LoveLetterGameException("Tried to discard card %s, but player %s doesn't have it in hand" % (str(card), str(self)))
        self._played_cards.append(card)
        self._hand.remove(card)
        if not no_action:
            card.discard_action(self)

    def draw(self, card):
        self._hand.append(card)
        card.draw_action(self)

    def lose(self):
        for card in self._hand:
            self.discard(card, no_action=True)
        self._alive = False
        # check if all but one dead, and end round if so
        if len(self.get_game().get_live_players()) == 1:
            self._game.start_new_round()

    def get_profile(self):
        return self._profile

    def get_game(self):
        return self._game

    def is_targetable(self):
        # TODO and not has immune aura
        return self._alive

    def __str__(self):
        return self._profile

class LoveLetterGameConfig(object):

    # Do my public variables upset you? You can submit your feedback at http://swagify.net/
    def __init__(self):
        self.min_players = 3
        self.max_players = 4
        self.num_cards_per_character = { c : c.default_amount for c in lovelettercards.get_all_characters() }
        self.rounds_to_win = 3

    # reckon i should put another constructor here? nah
