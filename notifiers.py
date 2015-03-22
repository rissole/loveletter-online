class ConsoleNotifier(object):

    def send_to_player(self, player, opcode, msg_args):
        print str(player), ":", opcode, str(msg_args)

    def send(self, players, opcode, msg_args):
        print ', '.join(str(p) for p in players), ":", opcode, str(msg_args)