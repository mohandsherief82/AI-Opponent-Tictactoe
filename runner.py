import pygame
import sys
import time

from board import Board

# Initialize all imported Pygame modules.
pygame.init()

# Set the dimensions of the display window.
size = width, height = 600, 600

# Define RGB color tuples for black, blue, red, and white.
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)

# Create the display surface for the game window.
screen = pygame.display.set_mode(size)

# Load fonts for displaying text in different sizes.
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

# Initialize variables for the user's player, game state, and computer's turn.
user = None
board = Board()
computer_turn = False
winner_player = None

# Main game loop.
while True:
    # Event loop to check for user input and system events.
    for event in pygame.event.get():
        # Check if the user has clicked the window's close button.
        if event.type == pygame.QUIT:
            # Quit Pygame and exit the program.
            sys.exit()

    # Fill the entire screen with black to clear the previous frame.
    screen.fill(black)

    # Check if a user has been chosen. If not, show the player selection screen.
    if user is None:

        # Render the game title text.
        title = largeFont.render("Play Tic-Tac-Toe", True, white)

        # Get the rectangle for the title text to position it.
        titleRect = title.get_rect()

        # Center the title horizontally and set its vertical position.
        titleRect.center = ((width / 2), 50)

        # Blit (draw) the title onto the screen surface.
        screen.blit(title, titleRect)

        # Create a rectangle for the 'Play as X' button.
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)

        # Render the text for the 'Play as X' button in blue.
        playX = mediumFont.render("Play as X", True, blue)

        # Get the rectangle for the 'Play as X' text.
        playXRect = playX.get_rect()

        # Center the 'Play as X' text within its button rectangle.
        playXRect.center = playXButton.center

        # Draw a white rectangle for the 'Play as X' button.
        pygame.draw.rect(screen, white, playXButton)

        # Blit the 'Play as X' text onto the screen.
        screen.blit(playX, playXRect)


        # Create a rectangle for the 'Play as O' button.
        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)

        # Render the text for the 'Play as O' button in red.
        playO = mediumFont.render("Play as O", True, red)

        # Get the rectangle for the 'Play as O' text.
        playORect = playO.get_rect()

        # Center the 'Play as O' text within its button rectangle.
        playORect.center = playOButton.center

        # Draw a white rectangle for the 'Play as O' button.
        pygame.draw.rect(screen, white, playOButton)

        # Blit the 'Play as O' text onto the screen.
        screen.blit(playO, playORect)


        # Get the state of the mouse buttons.
        click, _, _ = pygame.mouse.get_pressed()

        # Check if the left mouse button is pressed.
        if click == 1:
            # Get the current mouse cursor position.
            mouse = pygame.mouse.get_pos()

            # Check if the mouse is clicking the 'Play as X' button.
            if playXButton.collidepoint(mouse):
                # Add a small delay to prevent multiple clicks from registering.
                time.sleep(0.2)

                # Set the user's player to 'X'.
                user = board.X

            # Check if the mouse is clicking the 'Play as O' button.
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)

                # Set the user's player to 'O'.
                user = board.O

    # If a user has been chosen, draw the game board and play the game.
    else:

        # Define the size of each grid tile.
        tile_size = 100

        # Calculate the top-left coordinate for the entire grid.
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))

        # A list to store the rectangles for each tile, for collision detection.
        tiles = []

        # Loop through rows and columns to draw the grid.
        for i in range(3):
            row = []
            for j in range(3):
                # Create a rectangle for the current tile.
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )

                # Draw the tile rectangle outline on the screen.
                pygame.draw.rect(screen, white, rect, 3)

                # Check if the tile is occupied by an X or O.
                if board.grid[i, j] != board.EMPTY:
                    # Determine the color of the move based on the player.
                    color = blue if board.grid[i, j] == 'X' else red

                    # Render the X or O text in the appropriate color.
                    move = moveFont.render(board.grid[i, j], True, color)

                    # Get the rectangle for the text.
                    moveRect = move.get_rect()

                    # Center the text within the tile rectangle.
                    moveRect.center = rect.center

                    # Blit the X or O onto the screen.
                    screen.blit(move, moveRect)

                # Add the tile's rectangle to the row list.
                row.append(rect)

            # Add the row list to the main tiles list.
            tiles.append(row)

        # Get the current game state and the current player's turn.
        game_over = board.state
        player = board.player_turn()

        # Determine and render the title text based on the game's state.
        if game_over:
            winner = board.get_winner()
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
                player = board.player_turn()
                if user == player:
                    winner_player = "(Computer wins)."
                elif user != player:
                    winner_player = "(Player 1 wins)."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."

        # Render the final title text.
        title = largeFont.render(title, True, white)

        # Get its rectangle and center it at the top of the screen.
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)

        # Blit the title to the screen.
        screen.blit(title, titleRect)

        # Render and display the winner's message if the game is over.
        winner_title = mediumFont.render(winner_player, True, white)
        winner_titleRect = winner_title.get_rect()
        winner_titleRect.center = ((width / 2), 84)
        screen.blit(winner_title, winner_titleRect)

        # Check for a user's click and if the game is not over.
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and not game_over:
            # Get the mouse position.
            mouse = pygame.mouse.get_pos()

            # Iterate through the tiles to see if a tile was clicked.
            for i in range(3):
                for j in range(3):
                    # Check if the tile is empty and the mouse is colliding with it.
                    if board.grid[i, j] == board.EMPTY and tiles[i][j].collidepoint(mouse):
                        # Perform the action (place X or O on the board).
                        board.perform_action((i, j))

            # Update the game state after the move.
            winner = board.get_winner()
            game_over = board.state


        # Check if the game is over and display the "Play Again" button.
        if game_over:
            # Create a rectangle for the 'Play Again' button.
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)

            # Render the 'Play Again' text.
            again = mediumFont.render("Play Again", True, black)

            # Get the text rectangle and center it within the button rectangle.
            againRect = again.get_rect()
            againRect.center = againButton.center

            # Draw the button rectangle.
            pygame.draw.rect(screen, white, againButton)

            # Blit the text onto the button.
            screen.blit(again, againRect)

            # Check for a click on the 'Play Again' button.
            click, _, _ = pygame.mouse.get_pressed()

            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    # Reset game state to start a new game.
                    user = None
                    board.set_initial_state()
                    computer_turn = False
                    winner_player = None

    # Update the full display surface to show everything that was drawn.
    pygame.display.flip()