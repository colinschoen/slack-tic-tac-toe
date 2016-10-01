import utils

class Board:

    STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

    @staticmethod
    def start(payload, args):
        return "Creating game..."

    @staticmethod
    def board(payload, args):
        return utils.getBoard(STARTING_BOARD)
