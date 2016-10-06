HORIZONAL_BORDER = "-"
CORNER_BORDER = "+"
VERTICAL_BORDER = "|"

def getCurrentTurn(board):
    """Returns a pretty message reminding players whose turn it is
    Args:
        board (Board): The current board object
    Returns:
        str: The current players turn in a nice pretty string.
    """
    current_turn = board.player_turn
    if current_turn == player0_id:
        player_name = board.player0_nickname
    else:
        player_name = board.player1_nickname
    return "It is {}'s turn.".format(player_name)



def getBoard(board):
    """ Returns a pretty ASCII tic tac toe board.
    
    Args:
        board (list): The current board encoded in a list of lists

    Returns:
        str: The current ASCII representation of the board.

    >>> getBoard([["X", "O", "X"], ["X", "X", "X"], ["O", "X", "X"]])
    '|X|O|X|\\n|X|X|X|\\n|O|X|X|'
    >>> getBoard([[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])
    '| | | |\\n| | | |\\n| | | |'
    """
    assert type(board) is list, "The board must be a list"

    return "|{}|{}|{}|\n|{}|{}|{}|\n|{}|{}|{}|".format(
                board[0][0] if board[0][0] else "    ",
                board[0][1] if board[0][1] else "    ",
                board[0][2] if board[0][2] else "    ",
                board[1][0] if board[1][0] else "    ",
                board[1][1] if board[1][1] else "    ",
                board[1][2] if board[1][2] else "    ",
                board[2][0] if board[2][0] else "    ",
                board[2][1] if board[2][1] else "    ",
                board[2][2] if board[2][2] else "    ")

