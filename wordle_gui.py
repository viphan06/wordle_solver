import pygame, random
from wordle import play, Matches, PlayResponse, Status

# Initializes pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 650, 800
GRID_ROWS, GRID_COLS = 6, 5
CELL_SIZE = 80
MARGIN = 10
FONT_SIZE = 50
BG_COLOR = (255, 255, 255)
TEXT_COLOR_DEFAULT = (0, 0, 0)  # Before submitting, font is black
TEXT_COLOR = (255, 255, 255)  # After submitting guess, font is white
DEFAULT_CELL = (211, 211, 211)
CELL_COLORS = {
    Matches.EXACT_MATCH: (105, 169, 100),    # Green
    Matches.PARTIAL_MATCH: (201, 180, 85),  # Yellow
    Matches.WRONG_MATCH: (247, 102, 95),    # Red
}

# Title setup
title_font = pygame.font.Font("assets/HelveticaNeue.ttc", 50)
title_surface = title_font.render("WORDLE SOLVER", True, TEXT_COLOR_DEFAULT)  # Render the title
title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))  # Position at the top center

# Get random word from word list
def get_word(file_path):
    with open(file_path, "r") as file:
        words = [line.strip().upper() for line in file.readlines()]
    return words

# Load the words
word_list = get_word("wordle-allowed-guesses.txt")

# Pick random target word
def reset_target_word():
    return random.choice(word_list)

# Initial target word
target_word = reset_target_word()
print(f"Target word: {target_word}")  # For debugging

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wordle Solver")

# Set up fonts
font = pygame.font.Font("assets/HelveticaNeue.ttc", FONT_SIZE)

# Load Play Again button
play_again_image = pygame.image.load("assets/play_again_button.png")
play_again_rect = play_again_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))


# Game state variables
letters = [["" for _ in range(5)] for _ in range(6)]  # Empty grid: 6 rows, 5 columns
grid_colors = [[DEFAULT_CELL for _ in range(5)] for _ in range(6)]  # All cells default color
current_row = 0
current_col = 0

# Game state variables
def reset_game_state():
    global letters, grid_colors, current_row, current_col, target_word
    letters = [["" for _ in range(5)] for _ in range(6)]  # Empty grid: 6 rows, 5 columns
    grid_colors = [[DEFAULT_CELL for _ in range(5)] for _ in range(6)]  # All cells default color
    current_row = 0
    current_col = 0
    target_word = reset_target_word()
    print(f"New target word: {target_word}")  # Debugging

#reset_game_state()  # Initialize game state

grid_start_x = 100
grid_start_y = 100

# Draw the grid and letters
def draw_grid():
    for row in range(6):  # 6 rows for Wordle
        for col in range(5):  # 5 columns
            x = grid_start_x + col * (CELL_SIZE + MARGIN)
            y = grid_start_y + row * (CELL_SIZE + MARGIN)

            # Draw rectangle
            pygame.draw.rect(screen, grid_colors[row][col], (x, y, CELL_SIZE, CELL_SIZE), border_radius=5)

            # Draw letter
            if letters[row][col]:
                letter_color = TEXT_COLOR if grid_colors[row][col] != DEFAULT_CELL else TEXT_COLOR_DEFAULT
                letter_surface = font.render(letters[row][col], True, letter_color)
                letter_rect = letter_surface.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(letter_surface, letter_rect)

# Draw Play Again button
def draw_play_again_button():
    screen.blit(play_again_image, play_again_rect)

# Evaluate the current guess
def evaluate_guess():
    global current_row

    guess = "".join(letters[current_row])  # Combine the row's letters into a single word
    if len(guess) == 5:  # Only evaluate if the row is full
        response = play(target_word, guess, current_row)

        # Update grid colors based on the response
        tally_response = response[PlayResponse.TALLY_RESPONSE]
        for col, match in enumerate(tally_response):
            grid_colors[current_row][col] = CELL_COLORS[match]

        # Advance to the next row
        if current_row < GRID_ROWS - 1:
            current_row += 1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Handle backspace to remove the last letter
            if event.key == pygame.K_BACKSPACE:
                if current_col > 0:
                    current_col -= 1
                    letters[current_row][current_col] = ""

            # Handle Enter to evaluate the guess and move to the next row
            elif event.key == pygame.K_RETURN:
                if current_col == 5:  # Ensure row is full
                    evaluate_guess()
                    current_col = 0

            # Handle typing letters
            elif event.unicode.isalpha():
                if current_col < 5:  # Stay within the column limit
                    letters[current_row][current_col] = event.unicode.upper()
                    current_col += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if Play Again button was clicked
            if play_again_rect.collidepoint(event.pos):
                reset_game_state()

    # Fill the screen with background color
    screen.fill(BG_COLOR)

    # Draw the title
    screen.blit(title_surface, title_rect)

    # Draw the grid
    draw_grid()

    # Draw Play Again button
    draw_play_again_button()

    # Update the display
    pygame.display.flip()

pygame.quit()
