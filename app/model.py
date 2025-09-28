import numpy as np
from tqdm import tqdm

from board import Board


class QModel:
    """
    A model that can play Tic-Tac-Toe trained by a q learning algorithm.
    """
    n_state = 5478  # Number of all possible states for Tic-Tac-Toe
    n_actions = 9  # Number of all possible actions for Tic-Tac-Toe

    def __init__(self, l_rate=0.8, discount_factor=0.95, exploration_prob=0.2, epoch=1000):
        # Set Hyperparameters
        self.l_rate = l_rate  # Alpha, the learning rate
        self.discount_factor = discount_factor  # Gamma, the discount factor
        self.exploration_prob = exploration_prob  # Epsilon, the probability of exploring (choosing a random action)
        self.epochs = epoch

        # Initialize Q-table with random values.
        self.q_table = np.round(np.random.rand(self.n_state, self.n_actions), 4)

    def learning_algorithm(self):
        """
        The main Q-learning algorithm. It iterates through a number of epochs (games),
        and for each game, it follows the game loop to update the Q-table.
        The algorithm is set for a tic-tac-toe game.
        """
        # Initialize the game board and winner
        board = Board()

        for _ in tqdm(range(self.epochs), desc="Training Model"):

            # The game loop continues as long as there is no winner
            while not board.state:
                # Get the current state as a unique integer identifier
                current_state_id = self.get_state_id(board)

                # Exploitation: Choose the best action based on the Q-table
                action_values = {}
                for action in self.get_actions(board):
                    # Map the (row, col) action tuple to its corresponding Q-table index (0-8)
                    action_index = action[0] * 3 + action[1]
                    action_values[action] = self.q_table[current_state_id, action_index]

                # Use the imported max_key function to get the action tuple with the highest value
                try:
                    chosen_action = max(action_values, key=action_values.get)
                except ValueError:
                    break

                # Map the chosen (row, col) action tuple to its integer index for the Q-table
                chosen_action_index = chosen_action[0] * 3 + chosen_action[1]

                # Perform the chosen action on the board. This also provides the new state and reward.
                board.perform_action(chosen_action)

                # Update the Q-table
                self.update_table(board, current_state_id, chosen_action_index)

                board.get_winner()

            # Initialize a new game board
            board.set_initial_state()

            # Q-table normalization
            self.q_table = (self.q_table - np.min(self.q_table)) / (np.max(self.q_table) - np.min(self.q_table))

    def update_table(self, board, current_state_id, chosen_action_index):
        """The core Q-learning update function"""
        # Q(s, a) = Q(s, a) + alpha * (r + gamma * max_Q(s', a') - Q(s, a))
        self.q_table[current_state_id, chosen_action_index] = (
                self.q_table[current_state_id, chosen_action_index] +
                self.l_rate * (
                        self.get_reward(board) +
                        self.discount_factor * np.max(self.q_table[self.get_state_id(board)]) -
                        self.q_table[current_state_id, chosen_action_index]
                )
        )

    @staticmethod
    def get_state_id(board):
        """Maps the game board to a specific state id."""
        state = 0
        multiplier = 1

        # Iterate through all cells
        for row in range(3):
            for col in range(3):
                value = 0

                # Map the board cell's state to a value
                if board.grid[row][col] == board.X:
                    value = 1
                elif board.grid[row][col] == board.O:
                    value = 2

                # Add cell value to total state ID converting from base-3 to base-10 integer
                state += value * (row + 1)

        # Return state
        return state

    @staticmethod
    def get_reward(board):
        """
        Returns a reward based on the current state of the game.
        """
        winner = board.get_winner()

        # Check if the game has ended in a win or loss
        if winner is not None:
            # A large positive reward for winning
            if winner == board.X:
                return 10.0

            # A large negative reward for losing, punishing the agent
            elif winner == board.O:
                return -10.0

            # A small positive reward for a draw
            elif winner == winner:
                return 3

        # A small negative reward for every move if the game is still ongoing.
        return -0.1

    @staticmethod
    def get_actions(board):
        """Gets all possible actions given a board"""
        # A set of all possible actions
        possible_actions = set()

        for i, row in enumerate(board.grid):
            for j, cell in enumerate(row):
                if cell == board.EMPTY:
                    possible_actions.add((i, j))

        return sorted(possible_actions)

    def play_game(self, board):

        # Get current board state
        state_id = self.get_state_id(board)

        # copy Q-table
        copy_q_table = np.copy(self.q_table[state_id, :])

        # Get possible positions
        actions = self.get_actions(board)

        # Get best action
        best_action = None
        move = None
        for i, j in actions:
            if best_action is None:
                best_action = copy_q_table[i + j]
                move = (i, j)
            elif best_action < copy_q_table[i + j]:
                best_action = copy_q_table[i + j]
                move = (i, j)

        # Perform action
        board.perform_action(move)


def main():
    # Initialize Model
    model = QModel()

    # Training the model
    model.learning_algorithm()


if __name__ == "__main__":
    main()