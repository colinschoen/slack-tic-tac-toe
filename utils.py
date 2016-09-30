HORIZONAL_BORDER = "-"
CORNER_BORDER = "+"
VERTICAL_BORDER = "|"

def getBoard(board):
    """ Returns a pretty ASCII tic tac toe board.
    
    Args:
        board (list): The current board encoded in a list of lists

    Returns:
        str: The current ASCII representation of the board.
    """
    assert type(board) is list, "The board must be a list"

    return "| {} | {} | {} |\n|---+---+---|\n| {} | {} | {} |\n|---+---+---|\n| {} | {} | {} |".format(
                board[0][0],
                board[0][1],
                board[0][2],
                board[1][0],
                board[1][1],
                board[1][2],
                board[2][0],
                board[2][1],
                board[2][2])

