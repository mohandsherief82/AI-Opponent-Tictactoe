import numpy as np
import matplotlib.pyplot as plt

from board import Board


class QModel:
    """
    A model that can play Tic-Tac-Toe trained by a q learning algorithm.
    """

    n_state = 5478  # Number of all possible states for Tic-Tac-Toe ### Problem including number of states possible
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
        """
        # Initialize the game board
        board = Board()
        for epoch in range(self.epochs):

            # The game loop continues as long as there is no winner
            while board.get_winner() is None:
                # Get the current state as a unique integer identifier
                current_state_id = self.get_state_id(board)

                # Epsilon-Greedy Action Selection Strategy
                if np.random.rand() < self.exploration_prob:
                    # Exploration: Choose a random valid action
                    possible_actions = self.get_actions(board)
                    chosen_action = possible_actions[np.random.randint(len(possible_actions))]
                else:
                    # Exploitation: Choose the best action based on the Q-table
                    action_values = {}
                    for action in self.get_actions(board):
                        # Map the (row, col) action tuple to its corresponding Q-table index (0-8)
                        action_index = action[0] * 3 + action[1]
                        action_values[action] = self.q_table[current_state_id, action_index]

                    # Use the imported max_key function to get the action tuple with the highest value
                    chosen_action = max(action_values, key=action_values.get)

                # Map the chosen (row, col) action tuple to its integer index for the Q-table
                chosen_action_index = chosen_action[0] * 3 + chosen_action[1]

                # Perform the chosen action on the board. This also provides the new state and reward.
                board.perform_action(chosen_action)

                # Get the new state and reward after performing the action
                new_state_id = self.get_state_id(board) ## Having a problem here
                reward = self.get_reward(board)


                # The core Q-learning update formula:
                # Q(s, a) = Q(s, a) + alpha * (r + gamma * max_Q(s', a') - Q(s, a))
                self.q_table[current_state_id, chosen_action_index] = (
                        self.q_table[current_state_id, chosen_action_index] +
                        self.l_rate * (
                                reward +
                                self.discount_factor * np.max(self.q_table[new_state_id]) -
                                self.q_table[current_state_id, chosen_action_index]
                        )
                )

            # Initialize a new game board
            board.set_initial_state()

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
                return 1.0

            # A large negative reward for losing, punishing the agent
            elif winner == board.O:
                return -1.0

            # A small positive reward for a draw
            elif winner == winner:
                return 0.5

        # A small negative reward for every move if the game is still ongoing.
        return -0.01

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
                state += value * multiplier

                # Update multiplier for next cell
                multiplier *= 3

        # Return state
        return state

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

    def play_game(self, board):
        # Get the current state id
        state_id = self.get_state_id(board)

        # Get the best position based on id
        flat_id = np.argmax(self.q_table[:, state_id])
        action = (flat_id // 3, flat_id % 3)

        if action in self.get_actions():
            board.perform_action(action)


def main():
    # Initialize Environment and Model
    board = Board()
    model = QModel()

    model.learning_algorithm()

    model.show_q_table()

if __name__ == "__main__":
    main()