import random

import lovelettercards

class LoveLetterGame(object):

    def __init__(self, notifier):
        self._deck = []
        self._burn_pile = []
        self._players = []
        self.config = LoveLetterGameConfig()
        self._current_turn = 0
        self._notifier = notifier
        self._current_round = 0
        self._current_turn_player = None

    def get_current_turn(self):
        return self._current_turn

    def get_turn_player(self):
        if self.get_live_players():
            return self._current_turn_player
        else:
            raise LoveLetterGameException("Unable to get current turn player, all players dead.")

    def get_all_players(self):
        return self._players

    def get_players_excluding(self, *exclude):
        return filter(lambda p: p not in exclude, self._players)

    def get_live_players(self):
        return filter(lambda p: p.is_alive(), self._players)

    def get_live_players_excluding(self, *exclude):
        return filter(lambda p: p.is_alive() and p not in exclude, self._players)

    def get_config(self):
        return self.config

    def start_new_round(self, starting_player=None):
        self._current_round += 1
        players = self._players
        if len(players) < self.config.min_players or len(players) > self.config.max_players:
            raise LoveLetterGameException("Expected more than %s and less than %s players, got %s." % (self.config.min_players, self.config.max_players, len(players)))
        self._current_turn = 0
        self._current_turn_player = starting_player if starting_player else self._players[0]

        self.init_deck()
        self.burn_deck_card()

        for p in players:
            p.reset()
            self.draw_card(p)

        self.get_notifier().send(self.get_all_players(), 'round_begin', {'number': self._current_round})
        return self._current_round

    def init_deck(self):
        self._deck = []
        self._burn_pile = []
        for character, amount in self.config.num_cards_per_character.iteritems():
            for _ in xrange(amount):
                self._deck.append(character(self))
        random.shuffle(self._deck)

    def burn_deck_card(self):
        self._burn_pile.append(self._deck.pop())

    def add_player(self, player):
        players = self._players
        if len(players) + 1 > self.config.max_players:
            raise LoveLetterGameException("Cannot add more players to game: already have %s players." % (self.config.max_players))

        self._players.append(player)

    def get_player(self, player_name):
        return next(p for p in self._players if p.get_name() == player_name)

    def remove_player(self, player):
        self._players.remove(player)

    def play_card(self, player, card, **command_args):
        if card.get_owner() != player:
            raise LoveLetterGameException("Cannot play card %s: Player %s doesn't own card." % (card, player))
        player.discard(card)
        card.command_action(player, **command_args)
        self.next_turn()

    def draw_card(self, player):
        if len(self._deck) == 0:
            raise LoveLetterGameException("%s tried to draw a card but the deck is empty." % str(player))
        card = self._deck.pop()
        player.add_card_to_hand(card)
        self.get_notifier().send(self.get_players_excluding(player), 'anon_card_draw', {'player': player})
        self.get_notifier().send_to_player(player, 'card_draw', {'card': card})
        card.draw_action(player)

    def _increment_turn_player(self):
        current_player_index = self._players.index(self._current_turn_player)
        while True:
            current_player_index = (current_player_index + 1) % len(self._players)
            if self._players[current_player_index].is_alive():
                self._current_turn_player = self._players[current_player_index]
                break

    def next_turn(self):
        # check if all but one dead, and end round if so
        live_players = self.get_live_players()
        if len(live_players) == 1:
            winner = live_players[0]
            winner.give_win_credit()
            self.get_notifier().send(self.get_all_players(), 'win', {'player': winner})
            return self.start_new_round()

        # no cards left? let's do the compare step
        elif len(self._deck) == 0:
            self.get_notifier().send(self.get_all_players(), 'compare_phase_begin', {})
            self.do_compare_phase()
            return self.start_new_round()

        self._current_turn += 1
        self._increment_turn_player()
        # aura system next turn...
        return False

    def do_compare_phase(self):
        """ At the end of a round, when no cards are left in the deck, the
            winner is the player with the highest card."""
        winning_card = max((pl.get_hand_first_card() for pl in self.get_live_players()), key=lambda c: c.get_value())
        winners = filter(lambda pl: pl.get_hand_first_card().get_value() == winning_card.get_value(), self.get_live_players())
        for loser in self.get_live_players_excluding(winners):
            loser.lose()
        for winner in winners:
            winner.give_win_credit()
        self.get_notifier().send(self.get_all_players(), 'compare_phase_end', {'winners': winners, 'value': winning_card.get_value()})

    def get_notifier(self):
        return self._notifier

class LoveLetterGameException(Exception):
    pass

class LoveLetterPlayer(object):

    def __init__(self, name, game):
        self.reset()
        # name is some unique identifier for this player
        self._name = name
        self._game = game
        self._won_rounds = 0

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
            raise LoveLetterGameException("Tried to discard card %s, but player %s doesn't have it in hand." % (str(card), str(self)))
        self._played_cards.append(card)
        self._hand.remove(card)
        self.get_notifier().send(self._game.get_all_players(), 'discard', {'player': self, 'card': card})
        if not no_action:
            card.discard_action(self)

    def add_card_to_hand(self, card):
        self._hand.append(card)

    def lose(self):
        self.get_notifier().send(self._game.get_all_players(), 'lose', {'player': self})
        for card in self._hand:
            self.discard(card, no_action=True)
        self._alive = False

    def get_name(self):
        return self._name

    def get_game(self):
        return self._game

    def get_notifier(self):
        if self._game:
            return self._game.get_notifier()
        else:
            return None

    def is_targetable(self):
        # TODO and not has immune aura
        return True

    def give_win_credit(self):
        self._won_rounds += 1

    def get_won_rounds(self):
        return self._won_rounds

    def __str__(self):
        return self._name

    def __repr__(self):
        return str(self)

class LoveLetterGameConfig(object):

    # Do my public variables upset you? You can submit your feedback at http://swagify.net/
    def __init__(self):
        self.min_players = 3
        self.max_players = 4
        self.num_cards_per_character = { c : c.default_amount for c in lovelettercards.get_all_characters() }
        self.rounds_to_win = 3

    # reckon i should put another constructor here? nah
