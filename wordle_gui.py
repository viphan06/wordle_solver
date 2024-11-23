import pygame
from wordle import play, Matches, PlayResponse, Status

# Initializes pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 520, 700
GRID_ROWS, GRID_COLS = 6, 5
CELL_SIZE = 80
MARGIN = 20
FONT_SIZE = 50
BG_COLOR = (49, 54, 60)
TEXT_COLOR = (0, 0, 0)
CELL_COLOR_DEFAULT = (211, 211, 211)
CELL_COLORS = {
    Matches.EXACT_MATCH: (165, 182, 141),
    Matches.PARTIAL_MATCH: (250, 223, 161),
    Matches.WRONG_MATCH: (201, 104, 104),
}

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wordle Game for COSC 4368")

# Set up font
font = pygame.font.Font("/Users/vickynguyen/Library/Mobile Documents/com~apple~CloudDocs/Downloads/bubblegum/Bubblegum.ttf", 50)
text = "WORDLE"
text_surface = font.render(text, True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))

# State variables
target_word = "BAGEL"
CURR_ROW = 0
CURR_COL = 0
grid = [["" for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
grid_colors = [[CELL_COLOR_DEFAULT for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
game_over = False

def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CELL_SIZE + MARGIN) + MARGIN
            y = row * (CELL_SIZE + MARGIN) + 100
            pygame.draw.rect(screen, grid_colors[row][col], (x, y, CELL_SIZE, CELL_SIZE), border_radius=20)

            letter = grid[row][col]
            if letter:
                text_surface = font.render(letter, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)

def handle_guess(guess):
    global CURR_ROW, game_over

    response = play(target_word, guess, CURR_ROW)
    tally_response = response[PlayResponse.TALLY_RESPONSE]

    # Update grid colors
    for col, match in enumerate(tally_response):
        grid_colors[CURR_ROW][col] = CELL_COLORS[match]

    # Update game status
    game_status = response[PlayResponse.GAME_STATUS]
    if game_status == Status.WIN:
        print(response[PlayResponse.MESSAGE])
        game_over = True
    elif game_status == Status.LOSS:
        print(response[PlayResponse.MESSAGE])
        game_over = True

    CURR_ROW += 1

"""
# Display a message on the screen
def display_message(message):
    message_surface = font.render(message, True, TEXT_COLOR)
    message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    screen.blit(message_surface, message_rect)

# Draw the "Play Again" button
def draw_play_again():
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 50, 150, 40)
    pygame.draw.rect(screen, (CELL_COLOR_DEFAULT), button_rect)
    button_text = font.render("Play Again", True, CELL_COLOR_DEFAULT)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    return button_rect

    """
# Game loop
current_guess = ""
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_BACKSPACE:
                if CURR_COL > 0:
                    CURR_COL -= 1
                    grid[CURR_ROW][CURR_COL] = ""
                    current_guess = current_guess[:-1]
            elif event.key == pygame.K_RETURN:
                if CURR_COL == GRID_COLS:
                    handle_guess(current_guess.upper())
                    current_guess = ""
                    CURR_COL = 0
            elif event.unicode.isalpha() and len(current_guess) < GRID_COLS:
                grid[CURR_ROW][CURR_COL] = event.unicode.upper()
                current_guess += event.unicode.upper()
                CURR_COL += 1

    screen.fill(BG_COLOR)
    screen.blit(text_surface, text_rect)

    draw_grid()

    # if(game_over):
    #    play_again = draw_play_again()

    pygame.display.flip()

pygame.quit()
