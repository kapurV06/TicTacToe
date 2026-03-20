import numpy as np

board = np.zeros((3, 3), dtype=int)


def print_board(b):
    symbols = {0: " ", 1: "X", -1: "O"}
    for r in range(3):
        row = " | ".join(symbols[val] for val in b[r])
        print(" " + row)
        if r < 2:
            print("---|---|---")
    print()


def check_winner(b):
    """
    Returns 'X' if X wins, 'O' if O wins, None otherwise.
    X is stored as 1, O as -1.
    A player wins if any row, col, or diagonal sums to ±3.
    """
    row_sums = np.sum(b, axis=1)
    col_sums = np.sum(b, axis=0)
    main_diag = np.trace(b)                   # top-left to bottom-right
    anti_diag = np.trace(np.fliplr(b))        # top-right to bottom-left

    all_sums = np.concatenate([row_sums, col_sums, [main_diag, anti_diag]])

    if 3 in all_sums:
        return "X"
    if -3 in all_sums:
        return "O"
    return None


def is_draw(b):
    """Returns True if the board is full and there is no winner."""
    return np.all(b != 0) and check_winner(b) is None


def is_valid_move(b, row, col):
    """Returns True if the cell is empty."""
    return b[row, col] == 0


def make_move(b, row, col, player):
    """
    Places the player's mark on the board.
    player: 1 for X, -1 for O.
    Returns True if the move was made, False if the cell was occupied.
    """
    if not is_valid_move(b, row, col):
        return False
    b[row, col] = player
    return True


def get_available_moves(b):
    """Returns a list of (row, col) tuples for all empty cells."""
    return list(zip(*np.where(b == 0)))


def reset_board():
    """Returns a fresh empty board."""
    return np.zeros((3, 3), dtype=int)


# ── CLI game loop (run this file directly to play in the terminal) ──────────
if __name__ == "__main__":
    board = reset_board()
    current_player = 1          # X goes first
    symbols = {1: "X", -1: "O"}

    print("Welcome to TicTacToe!")
    print_board(board)

    while True:
        print(f"Player {symbols[current_player]}'s turn.")
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
        except ValueError:
            print("Invalid input. Enter integers 0-2.")
            continue

        if not (0 <= row <= 2 and 0 <= col <= 2):
            print("Out of range. Enter values between 0 and 2.")
            continue

        if not make_move(board, row, col, current_player):
            print("Cell already taken. Try again.")
            continue

        print_board(board)

        winner = check_winner(board)
        if winner:
            print(f"Player {winner} wins! 🎉")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        current_player *= -1   # switch turns