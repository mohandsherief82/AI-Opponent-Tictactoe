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

    def get_actions(self):
        """
        Returns set of all possible actions
        """
        actions = set()

        # Loops for every cell to check if empty
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == self.EMPTY:
                    actions.add((i, j))

        return  actions

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
        win_pos = np.vstack((self.grid, transpose_grid, diagonals))

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

    # Will be removed or alter with model
    def fake_action(self, fake_grid, action):
        i, j = action

        if fake_grid[i, j] == self.EMPTY:
            fake_grid[i, j] = self.player_turn()

        return fake_grid

    def minimax_value(self, fake_board=None):
        if self.player_turn() == self.X:
            func = max
            v = - np.inf
        else:
            func = min
            v = - np.inf


        for action in self.get_actions():
            fake_board = self.grid
            fake_board = self.fake_action(fake_board, action)
            v = func(v, self.minimax_value())

        return v

    def minimax(self):
        for action in self.get_actions():
            if self.minimax_value() == self.minimax_value():
                return action