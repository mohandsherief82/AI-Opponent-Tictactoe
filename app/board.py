import numpy as np

class Board:

    EMPTY = None
    X = "X"
    O = "O"

    def __init__(self):
        # Create the initial grid of size  3 x 3 using 2D array
        self.grid = np.full((3, 3), self.EMPTY)

        # Initialize the game state
        self.state = False

    def set_initial_state(self):
        # For multiple games
        self.grid = np.full((3, 3), self.EMPTY)
        self.state = False

    def player_turn(self):
        """
        Return the player who has the next turn
        """
        # Number of alternated turns
        count = 0

        # Loops on every row on the grid
        for row in self.grid:
            count += np.sum(row == self.X) - np.sum(row == self.O)

        # Returns whose turn
        return self.X if count == 0 else self.O

    def perform_action(self, action):
        """
        Returns the grid after performing an action
        """
        i, j = action

        # Check if move is Valid
        if self.grid[i, j] == self.EMPTY:
            self.grid[i, j] = self.player_turn()
        else:
            raise Exception("Invalid Action!")

    def get_winner(self):
        """
        Returns the player who is the winner and
        the game state when over.
        """
        transpose_grid = np.transpose(self.grid)

        # Find the grid's diagonals
        diagonals = np.concatenate((np.diagonal(self.grid), np.diagonal(np.fliplr(self.grid))), axis=0)

        # Create a list of all possible winning positions
        win_pos = np.vstack((self.grid, transpose_grid, diagonals.reshape((2,3))))

        winner = None

        # Loop over all possible position combinations for winner
        for position in win_pos:
            count = 0 + np.sum(position == position[0])
            if count == 3:
                winner = position[0]

        if winner == self.X or winner == self.O:
            self.state = True

        # Return winner
        return winner

    def is_full(self):
        count = 0
        for row in self.grid:
            for cell in row:
                if cell != self.EMPTY:
                    count += 1

        if count != 9:
            return True
        return False
