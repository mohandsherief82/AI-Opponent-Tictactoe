- # AI Opponent Tictactoe

  - ## Components

    - The game will consist of a board defined in the file board.py, a model defined in the model.py file and a runner in the runner.py file.
    - Each of these files contain all the context it might need.

  - ## Summary

    - The runner is built using a basic GUI on the pygame library, which allows the user to choose whether he wants to play X or O and shows the score.
    - The board is a class that allows the user and the computer to take their turns respectively detect winner and update scoreboard.
    - The model will run on a Q-Learning algorithm and deployed with the board
    - To allow the model to be unbeatable, we need high learning rate, discount factor and number of epochs and a low exploration rate that is decaying.