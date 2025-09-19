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
mediumFont = pygame.font.Font("../OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("../OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("../OpenSans-Regular.ttf", 60)

# Initialize game state variables.
user = None  # Stores the player's chosen symbol ('X' or 'O').
board = Board()  # Represents the game board.
computer_turn = False  # Flag to manage computer's turn.
winner_player = None  # Stores a descriptive message for the winner.
score = {"Player": 0, "Computer": 0}  # Tracks the scores for each player.

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

        # Draw title for player selection screen.
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons to choose between X and O.
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, blue)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, red)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if a button is clicked to set the user's player.
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = board.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = board.O

    # If a user has been chosen, start the game against the computer.
    else:
        # Display the current scores.
        player_score_text = mediumFont.render(f"Player Score: {score['Player']}", True, white)
        computer_score_text = mediumFont.render(f"Computer Score: {score['Computer']}", True, white)
        screen.blit(player_score_text, (10, 75))
        screen.blit(computer_score_text, (width - computer_score_text.get_width() - 10, 75))

        # Draw the tic-tac-toe game board.
        tile_size = 100
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                # Create a rectangle for each tile.
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                # Draw the tile's outline.
                pygame.draw.rect(screen, white, rect, 3)

                # Check if the tile is occupied.
                if board.grid[i, j] != board.EMPTY:
                    # Determine the color based on the player's move.
                    color = blue if board.grid[i, j] == 'X' else red
                    # Render the X or O.
                    move = moveFont.render(board.grid[i, j], True, color)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    # Blit the move onto the screen.
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = board.state
        player = board.player_turn()

        # Show game title based on the current state.
        if game_over:
            winner = board.get_winner()
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
                # Update the score based on the winner.
                if winner == user:
                    score["Player"] += 1
                    winner_player = "(Player wins)."
                else:
                    score["Computer"] += 1
                    winner_player = "(Computer wins)."
        elif user == player:
            # It's the human player's turn.
            title = f"Play as {user}"
        else:
            # It's the computer's turn.
            title = f"Computer thinking..."

        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Display the winner's message if the game is over.
        if winner_player is not None:
            winner_title = mediumFont.render(winner_player, True, white)
            winner_titleRect = winner_title.get_rect()
            winner_titleRect.center = ((width / 2), 84)
            screen.blit(winner_title, winner_titleRect)

        # Check for AI move only when it's the computer's turn.
        if user != player and not game_over:
            # Logic for computer's move would go here.
            # Example: time.sleep(0.5); move = board.minimax(); board.perform_action(move);
            pass

        # Check for a user move.
        click, _, _ = pygame.mouse.get_pressed()
        # Only handle clicks if it's the user's turn and the game is not over.
        if click == 1 and not game_over and user == player:
            mouse = pygame.mouse.get_pos()
            # Iterate through tiles to see if a valid move was made.
            for i in range(3):
                for j in range(3):
                    if board.grid[i, j] == board.EMPTY and tiles[i][j].collidepoint(mouse):
                        board.perform_action((i, j))

            winner = board.get_winner()
            game_over = board.state

        # Check if the game is over and display the "Play Again" button.
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    # Reset game state for a new round, preserving the score.
                    board.set_initial_state()
                    computer_turn = False
                    winner_player = None

    # Update the full display surface to show everything that was drawn.
    pygame.display.flip()