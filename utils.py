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
                board[0][0] if board[0][0] else "     ",
                board[0][1] if board[0][1] else "     ",
                board[0][2] if board[0][2] else "     ",
                board[1][0] if board[1][0] else "     ",
                board[1][1] if board[1][1] else "     ",
                board[1][2] if board[1][2] else "     ",
                board[2][0] if board[2][0] else "     ",
                board[2][1] if board[2][1] else "     ",
                board[2][2] if board[2][2] else "     ")

