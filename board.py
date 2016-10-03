from app import db
import time
import utils

class Board(db.model):
    id = db.Column(db.Integer, primary_key=True)
    player0_id = db.Column(db.String(100))
    player1_id = db.Column(db.String(100))
    player1_nickname = db.Column(db.String(40))
    player_turn = db.Column(db.String(100))
    channel_id = db.Column(db.String(100))
    state = db.Column(db.String(9))
    updated_at = db.Column(db.String(100))
    created_at = db.Column(db.String(100))
    STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

    def __init__(self, player0_id=None, player1_id=None, player1_nickname=None,
            player_turn=None, channel_id=None, state=None,
            updated_at=time.ctime(), created_at=time.ctime()):
        """
        Creates a new board
        """
        self.player0_id = player0_id
        self.player1_id = player1_id
        self.player1_nikcname = player1_nickname
        self.player_turn = player_turn
        if not player_turn:
            self.player_turn = player0_id
        self.channel_id = channel_id
        self.state = state


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
