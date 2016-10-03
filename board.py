from app import db
import time
import utils

class Board(db.Model):
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
    def encode_state(state):
        """
        Encode a game state by flattening it to a string to be stored in the DB

        args:
            state(list) The state to encode
        returns:
            strState(str) A string representation of the state
        """
        strState = ""
        for row in state:
            for column in row:
                strState += column if column is not None else " "

    @staticmethod
    def decode_state(state):
        """
        Decode the serialized game state by creating the list structure

        args:
            state(str) The serialized string state to decode
        returns:
            state(list) A list representation of the state
        """
        state = split('')
        lstState = []
        for _ in range(3):
            row = []
            for _ in range(3):
                element = state[0] if state[0] !=  " " else None
                row.append(state[0])
                state = state[1:]
            lstState.append(row)
        return lstState

        
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
    def board(payload, args=None):
        """
        Fetches and outputs a pretty version of the current game state (board)

        args:
            payload (dict) - Dictionary containing POST payload from Slack.
            args (list) - List containing arguments or flags passed after Sack
                 commands.
        """
        channel_id = payload['channel_id']
        board = Board.query.filter_by(channel_id=channel_id).first()
        if not board:
            return 'Error: No game exists in this channel'
        state = Board.decode(board.state)
        return utils.getBoard(state)
