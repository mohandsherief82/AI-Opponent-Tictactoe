import numpy as np
import matplotlib.pyplot as plt

from board import Board

class QModel:
    """
    A model that can play Tic-Tac-Toe trained by a q learning algorithm.
    """

    n_state = 5478  # Number of all possible states for Tic-Tac-Toe
    n_actions = 9 # Number of all possible actions for Tic-Tac-Toe
    goal_state = "Computer" # Target State

    def __init__(self, l_rate=0.8, discount_factor=0.95, exploration_prob=0.2, epoch=1000):
        # Set Hyperparameters
        self.l_rate = l_rate
        self.discount_factor = discount_factor
        self.exploration_prob =  exploration_prob
        self.epochs =  epoch

        # Initialize Q-table
        self.q_table = np.zeros((self.n_state, self.n_actions))

    def learning_algorithm(self):
        # Repeat for each epoch
        for epoch in range(self.epochs):
            # Initialize board, current state and winner
            board = Board()
            initial_state = board.grid
            winner = None

            # Keeping track of position and values
            max_pos_value = {}
            while board.get_winner() is None:
                # Extract the possible moves
                for action in self.__get_actions(board):
                    max_pos_value[action] = self.q_table[action].max()


    @staticmethod
    def __get_actions(board):
        """Gets all possible actions given a board"""
        # A set of all possible actions
        possible_actions = set()

        for i, row in enumerate(board.grid):
            for j, cell in enumerate(row):
                if cell == board.EMPTY:
                    possible_actions.add((i, j))

        return possible_actions

    def show_q_table(self):
        q_values_grid = np.max(self.q_table, axis=1).reshape((3, 3))

        # Plot the grid of Q-values
        plt.figure(figsize=(6, 6))
        plt.imshow(q_values_grid, cmap='coolwarm', interpolation='nearest')
        plt.colorbar(label='Q-value')
        plt.title('Learned Q-values for each state')
        plt.xticks(np.arange(4), ['0', '1', '2', '3'])
        plt.yticks(np.arange(4), ['0', '1', '2', '3'])
        plt.gca().invert_yaxis()  # To match grid layout
        plt.grid(True)

        # Annotating the Q-values on the grid
        for i in range(4):
            for j in range(4):
                plt.text(j, i, f'{q_values_grid[i, j]:.2f}', ha='center', va='center', color='black')

        plt.show()


def main():
    # Initialize Environment and Model
    board = Board()
    model = QModel()


if __name__ == "__main__":
    main()
