from app import db
import time
import utils

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player0_id = db.Column(db.String(100))
    player1_id = db.Column(db.String(100))
    player0_nickname = db.Column(db.String(40))
    player1_nickname = db.Column(db.String(40))
    player_turn = db.Column(db.String(100))
    channel_id = db.Column(db.String(100))
    state = db.Column(db.String(9))
    updated_at = db.Column(db.String(100))
    created_at = db.Column(db.String(100))
    STARTING_BOARD = [[None, None, None], [None, None, None], [None, None, None]]

    def __init__(self, player0_id=None, player1_id=None, player1_nickname=None,
            player0_nickname=None, player_turn=None, channel_id=None, state=None,
            updated_at=time.ctime(), created_at=time.ctime()):
        """
        Creates a new board
        """
        self.player0_id = player0_id
        self.player1_id = player1_id
        self.player0_nickname = player0_nickname
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

        >>> encode_state([["X", "O", "X"], ["X", "O", "X"], ["X", "O", "X"]])
        >>> 'XOXXOXXOX'
        >>> encode_state([[None, "O", "X"], ["X", None, "X"], ["X", "O", "X"]])
        >>> ' OXX XXOX'
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

        >>> decode_state("XOXOXOXOX")
        [["X", "O", "X"], ["X", "O", "X"], ["X", "O", "X"]]

        >>> decode_state(" O OXOXOX")
        [[None, "O", None], ["X", "O", "X"], ["X", "O", "X"]]
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
        """ 
        Returns true or false depending on if the game is over
        
        Warning -- This is really messy and can be greatly improved.
        
        returns:
            over(bool) - True if game is over False otherwise
        """
        #TODO(@colinschoen) Make this actually legible and more efficient
        #   Perhaps use magic square
        state = str(self.state)
        if " " not in state:
            return True
        state = self.decode_state(state)
        for row in state:
            player0_row_score = 0
            player1_row_score = 0
            for element in row:
                if element == "X":
                    player0_row_score += 1
                elif element == "O":
                    player1_row_score += 1
            if player0_row_score == 3 or player1_row_score == 3:
                return True
        # Check diagonals
        d1 = [state[0][0], state[1][1], state[2][2]] 
        d2 = [state[2][0], state[1][1], state[0][2]]
        if d1 == ["X", "X", "X"] or  d1 == ["O", "O", "O"] or d2 == ["X", "X", "X"] or d2 ==["O", "O", "O"]:
            return True
        # Finally check the columns
        transpose = list(zip(*state))
        return any([c == ("O", "O", "O") or c == ("X", "X", "X") for c in transpose])
        
    @staticmethod
    def help(payload=None, args=None):
        """
        Prints a help message detailing the commands for the user

        args:
            payload (dict) - Dictionary containing POST payload from Slack.
            args (list) - List containing arguments or flags passed after Sack
                 commands.
        returns:
            help (str) - A "helpful" help string

        """
        return """
        Available commands:


        board - (E.g. /ttt board) Display the current board in the channel 
        move [row index] [col index] - (E.g. /ttt move 0 3) Make a move to the 0th row and 3rd column
        start [user] - (E.g. /ttt start @colin) Start a game with opponent @Colin
        """

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
        board = Board(player0_id=payload['user_id'],
                player0_nickname=payload['user_name'],
                player1_nickname=opponent[1:],
                player_turn=payload['user_id'],
                channel_id=payload['channel_id'],
                state=state
                )
        db.session.add(board)
        db.session.commit()
        state = Board.decode_state(state)
        return "{}\n{}".format(utils.getBoard(state), utils.getCurrentTurn(board))
        
    @staticmethod
    def move(payload, args):
        """
        Makes a move for a player if it is the players turn and a game exists.

        args:
            payload (dict) - Dictionary containing POST payload from Slack.
            args (list) - List containing arguments or flags passed after Sack
                 commands.
        """
        # Were the proper arguments passed?
        if len(args) < 2:
            return 'Error: You must specific a position to make your move (E.g. /ttt move 0 3)'
        # Make our arguments ints
        args = [int(arg) for arg in args]
        # Do we have valid arguments?
        if not all([arg <= 2 and arg >= 0 for arg in args]):
            return 'Error: Invalid row or column specified'
        # Does a game exist?
        channel_id = payload['channel_id']
        board = Board.query.filter_by(channel_id=channel_id).first()
        if not board:
            return 'Error: No game exists in current channel. "Try /ttt start @opponent"'
        # Do we need to log this as player 1
        if not board.player1_id and str(board.player1_nickname) == payload['user_name'].lower():
            board.player1_id = payload['user_id']
            db.session.commit()
        # Is this user even a player involved in the game?
        if payload['user_id'] != str(board.player0_id) and payload['user_id'] != str(board.player1_id):
            return 'Error: You are not a player in this game'
        # Is it the "invoking" players turn?
        if payload['user_id'] == board.player0_id and board.player_turn != board.player0_id or ( payload['user_id'] == board.player1_id and board.player_turn and board.player_turn != board.player1_id):
            return "Error: It is your opponents turn."
        state = Board.decode_state(str(board.state))
        row, col = args[0], args[1]
        if state[row][col] == "O" or state[row][col] == "X":
            return "Error: You can't move here."
        state[row][col] = "X" if payload['user_id'] == str(board.player0_id) else "O"
        # Update our board
        board.state = Board.encode_state(state)
        # Update our current players turn
        board.player_turn = board.player0_id if payload['user_id'] != str(board.player0_id) else board.player1_id
        db.session.commit()
        if board.isGameOver():
            # Delete the board
            db.session.delete(board)
            db.session.commit()
            return utils.getBoard(state) + "\n Game is over!"
        return "{}\n{}".format(utils.getBoard(state), utils.getCurrentTurn(board))


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
        return "{}\n{}".format(utils.getBoard(state), utils.getCurrentTurn(board))
