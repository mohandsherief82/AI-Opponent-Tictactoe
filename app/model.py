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

    def learning_algorithm(self, board : Board):
        # Repeat for each epoch
        for epoch in range(self.epochs):
            current_state = board.grid
            while current_state != self.goal_state:
                if np.random.rand() < self.exploration_prob:
                    action = np.random.randint(0, self.n_actions)
                else:
                    action = np.argmax(self.q_table[current_state])

                next_state = (current_state + 1) % self.n_state

                reward = 1 if next_state == self.goal_state else 0

                self.q_table[current_state, action] += self.l_rate * \
                                                  (reward + self.discount_factor *
                                                   np.max(self.q_table[next_state]) - self.q_table[current_state, action])

                current_state = next_state

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
