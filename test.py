import unittest
from loveletter import *
import notifiers

class TestLoveLetterCore(unittest.TestCase):
	def setUp(self):
		self.game = LoveLetterGame(notifiers.DevNullNotifier())
		self.players = [
		    LoveLetterPlayer('blake', self.game),
		    LoveLetterPlayer('dave', self.game),
		    LoveLetterPlayer('jacob', self.game),
		]
		for p in self.players:
		    self.game.add_player(p)
		self.game.start_new_round()

	def test_turn(self):
		self.assertEquals(self.players[0], self.game.get_turn_player())
		self.game.next_turn()
		self.assertEquals(self.players[1], self.game.get_turn_player())
		self.game.next_turn()
		self.assertEquals(self.players[2], self.game.get_turn_player())
		self.players[0].lose()
		self.game.next_turn()
		self.assertEquals(self.players[1], self.game.get_turn_player())
		self.game.next_turn()
		self.assertEquals(self.players[2], self.game.get_turn_player())
		self.game.next_turn()
		self.assertEquals(self.players[1], self.game.get_turn_player())

if __name__ == '__main__':
	unittest.main()