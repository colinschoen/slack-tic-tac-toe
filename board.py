import utils

class Board:

    STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

    @staticmethod
    def start(payload, args):
        """
        Starts a new game if one doesn't already exist in the channel
        """
        opponent = args[0]
        # There isn't a way to properly validate that a user with the handle
        #    exists, so just ensure the format is correct.
        if opponent[0] != '@':
            return "Error: You must specify an opponent by their @handle"
        channel_id, user_id = payload['channel_id'], payload['user_id']
        # TODO(@colinschoen) Does a game already exist in this channel
        #    sql('SELECT count(*) FROM GAMES WHERE channel_id=channel_id')
        

    @staticmethod
    def board(payload, args):
        return utils.getBoard(Board.STARTING_BOARD)
