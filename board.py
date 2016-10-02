import utils

class Board:

    STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

    @staticmethod
    def start(payload, args):
        """
        Starts a new game if one doesn't already exist in the channel

        args:
            payload (dict) - Dictionary containing POST payload from Slack.
            args (list) - List containing arguments or flags passed after Sack
                 commands.
        """
        opponent = args[0]
        # There isn't a way to properly validate that a user with the handle
        #    exists, so just ensure the format is correct.
        if opponent[0] != '@':
            return 'Error: You must specify an opponent by their @handle'
        channel_id, user_id = payload['channel_id'], payload['user_id']
        # TODO(@colinschoen) Does a game already exist in this channel
        #    sql('SELECT count(*) FROM GAMES WHERE channel_id=channel_id')
        
    def make_move(payload, args):
        """
        Makes a move for a player if it is the players turn and a game exists.

        args:
            payload (dict) - Dictionary containing POST payload from Slack.
            args (list) - List containing arguments or flags passed after Sack
                 commands.
        """
        # Does a game exist?
        # TODO(@colinschoen) Fetch from DB current game for this channel
        exists = True
        if not exist:
            return 'Error: No game exists in current channel. "Try /ttt start @opponent"'
        # Is it the "invoking" players turn?
        # TODO(@colinschoen) Fetch from DB current players turn
        turn = 0 
        if payload['user_id'] != turn:
            return "Error: It is your opponents turn."
        # TODO(@colinschoen) Update DB with this move
        # TODO(@colinschoen) Fetch current board from DB
        return utils.getBoard([])


    @staticmethod
    def board(payload=None, args=None):
        return utils.getBoard(Board.STARTING_BOARD)
