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
# Added new variable to track game mode choice.
game_mode = None

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

    # Check if game mode has been chosen.
    if game_mode is None:
        # Draw the title for game mode selection.
        title = largeFont.render("Choose Game Mode", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw the 'One Player' button.
        onePlayerButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        onePlayer = mediumFont.render("One Player", True, black)
        onePlayerRect = onePlayer.get_rect()
        onePlayerRect.center = onePlayerButton.center
        pygame.draw.rect(screen, white, onePlayerButton)
        screen.blit(onePlayer, onePlayerRect)

        # Draw the 'Two Player' button.
        twoPlayerButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        twoPlayer = mediumFont.render("Two Player", True, black)
        twoPlayerRect = twoPlayer.get_rect()
        twoPlayerRect.center = twoPlayerButton.center
        pygame.draw.rect(screen, white, twoPlayerButton)
        screen.blit(twoPlayer, twoPlayerRect)

        # Check for button clicks to set the game mode.
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if onePlayerButton.collidepoint(mouse):
                time.sleep(0.2)
                game_mode = "one_player"
            elif twoPlayerButton.collidepoint(mouse):
                time.sleep(0.2)
                game_mode = "two_player"

    # If game mode is chosen but player is not, show player selection.
    elif user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
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

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = board.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = board.O

    # If a user and game mode have been chosen, start the game.
    else:
        # Draw game board
        tile_size = 100
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board.grid[i, j] != board.EMPTY:
                    color = blue if board.grid[i, j] == 'X' else red
                    move = moveFont.render(board.grid[i, j], True, color)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = board.state
        player = board.player_turn()

        # Show title
        if game_over:
            winner = board.get_winner()
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
                if game_mode == "one_player":
                    if user == player:
                        winner_player = "(Computer wins)."
                    elif user != player:
                        winner_player = "(Player 1 wins)."
        elif game_mode == "one_player":
            if user == player:
                title = f"Play as {user}"
            else:
                title = f"Computer thinking..."
        else:  # Two player mode
            title = f"Player {player}'s turn"

        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        if winner_player is not None:
            winner_title = mediumFont.render(winner_player, True, white)
            winner_titleRect = winner_title.get_rect()
            winner_titleRect.center = ((width / 2), 84)
            screen.blit(winner_title, winner_titleRect)

        # Check for AI move only in one-player mode.
        if game_mode == "one_player" and user != player and not game_over:
            #########################################################
            # This is where the computer's turn logic would be.
            # You can uncomment and use the minimax() function here.
            #########################################################
            pass

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and not game_over:
            mouse = pygame.mouse.get_pos()

            for i in range(3):
                for j in range(3):
                    # In one player mode, only the user can click.
                    # In two player mode, both players can click.
                    if board.grid[i, j] == board.EMPTY and tiles[i][j].collidepoint(mouse):
                        board.perform_action((i, j))

            winner = board.get_winner()
            game_over = board.state

        # check if game is over
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
                    # Reset all variables for a new game.
                    user = None
                    board.set_initial_state()
                    computer_turn = False
                    winner_player = None
                    game_mode = None

    # Update the full display surface to show everything that was drawn.
    pygame.display.flip()