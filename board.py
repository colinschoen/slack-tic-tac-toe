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
        self.player1_nickname = player1_nickname
        self.player_turn = player_turn
        if not player_turn:
            self.player_turn = player0_id
        self.channel_id = channel_id
        self.state = state
        self.updated_at = updated_at
        self.created_at = created_at


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
        return strState

    @staticmethod
    def decode_state(state):
        """
        Decode the serialized game state by creating the list structure

        args:
            state(str) The serialized string state to decode
        returns:
            state(list) A list representation of the state
        """
        assert type(state) is str, "state must be a string"

        state = list(state)
        lstState = []
        for _ in range(3):
            row = []
            for _ in range(3):
                element = state[0] if state[0] !=  " " else None
                row.append(state[0])
                state = state[1:]
            lstState.append(row)
        return lstState

    def isGameOver(self):
        state = decode_state(self.state)
        for row in state:
            player0_row_score = 0
            player1_row_score = 0
            for element in row:
                if element == x:
                    player0_row_score += 1
                elif element == 0:
                    player1_row_score += 1
            if player0_row_score == 3 or player1_row_score == 3:
                return True
        return False
        #TODO(@colinschoen) Check columns and diagonals
                

        
    @staticmethod
    def start(payload, args):
        """
        Starts a new game if one doesn't already exist in the channel

        args:
            payload (dict) - Dictionary containing POST payload from Slack.
            args (list) - List containing arguments or flags passed after Sack
                 commands.
        """
        if len(args) < 1:
            return "Error: You must specify an opponent"
        # Does a game already exist in this channel?
        channel_id = payload['channel_id']
        board = Board.query.filter_by(channel_id=channel_id).first()
        if board and not board.isGameOver():
            return "Error: An active game already exists in this channel."
        opponent = args[0]
        if opponent[1:].lower() == payload['user_name'].lower():
            return "Error: You can't challenge yourself."
        # There isn't a way to properly validate that a user with the handle
        #    exists, so just ensure the format is correct.
        if opponent[0] != '@':
            return 'Error: You must specify an opponent by their @handle'
        state = Board.encode_state(Board.STARTING_BOARD)
        print("state =", state)
        board = Board(player0_id=payload['user_id'],
                player1_nickname=opponent[1:],
                player_turn=payload['user_id'],
                channel_id=payload['channel_id'],
                state=state
                )
        db.session.add(board)
        db.session.commit()
        state = Board.decode_state(state)
        return utils.getBoard(state)
        
    def make_move(payload, args):
        """
        Makes a move for a player if it is the players turn and a game exists.

        args:
            payload (dict) - Dictionary containing POST payload from Slack.
            args (list) - List containing arguments or flags passed after Sack
                 commands.
        """
        # Does a game exist?
        channel_id = payload['channel_id']
        board = Board.query.filter_by(channel_id=channel_id).first()
        if not board:
            return 'Error: No game exists in current channel. "Try /ttt start @opponent"'
        # Is it the "invoking" players turn?
        if board.player_turn != payload['user_id']:
            return "Error: It is your opponents turn."
        # TODO(@colinschoen) Update DB with this move
        # TODO(@colinschoen) Fetch current board from DB
        return utils.getBoard(Board.encode_state(board.state))


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
        state = Board.decode_state(str(board.state))
        return utils.getBoard(state)
