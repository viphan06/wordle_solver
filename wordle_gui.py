import pygame, random
from wordle import play, Matches, PlayResponse

# Initializes pygame
pygame.init()

# ------------------------------ Constants ------------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 650, 900
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

# Set up fonts
font = pygame.font.Font("assets/HelveticaNeue.ttc", FONT_SIZE)

grid_start_x = 100
grid_start_y = 180

# ----------------------------------- Menu -----------------------------------
def show_menu():
    menu_running = True
    selected_algorithm = None
    algorithms = [
        "Constraint Propagation",
        "Frequency-Based",
        "Information Gain",
        "Rule Based"
    ]
    # Text
    word_font = pygame.font.Font(None, 32)
    word_surface = word_font.render("Pick an algorithm:", True, (102,160,96))
    word_rect = word_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(word_surface, word_rect)

    button_gap = 115
    button_y = 290

    # Load algorithm buttons
    constraint_propagation_image = pygame.image.load("assets/constraint_propagation_button.png")
    constraint_propagation_rect = constraint_propagation_image.get_rect(center=(SCREEN_WIDTH // 2, button_y)) 
    button_y += button_gap

    frequency_based_image = pygame.image.load("assets/frequency_based_button.png")
    frequency_based_rect = frequency_based_image.get_rect(center=(SCREEN_WIDTH // 2, button_y))
    button_y += button_gap

    information_gain_image = pygame.image.load("assets/information_gain_button.png")
    information_gain_rect = information_gain_image.get_rect(center=(SCREEN_WIDTH // 2, button_y))
    button_y += button_gap

    rule_based_image = pygame.image.load("assets/rule_based_button.png")
    rule_based_rect = rule_based_image.get_rect(center=(SCREEN_WIDTH // 2, button_y))

    screen.blit(constraint_propagation_image, constraint_propagation_rect)
    screen.blit(frequency_based_image, frequency_based_rect)
    screen.blit(information_gain_image, information_gain_rect)
    screen.blit(rule_based_image, rule_based_rect)

# ------------------------------ Utility Functions ------------------------------
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

# ------------------------------ Drawing Functions ------------------------------
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

# Load the title image
title_image = pygame.image.load("assets/title.png")
title_rect = title_image.get_rect(center=(SCREEN_WIDTH // 2, 100))  # Position the title at the top center

# Draw the title image
def draw_title():
    screen.blit(title_image, title_rect)

# ------------------------------ Game Logic ------------------------------
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

# ------------------------------ Main Game Loop ------------------------------
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            # Check if Ctrl + Q is pressed
            if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                running = False
                print("Exiting...")
        if event.type == pygame.QUIT:
           running = False
        '''
        ------just for testing--------
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
        '''

    screen.fill(BG_COLOR)
    draw_title()
    show_menu()
    #draw_grid()
    #draw_play_again_button()
    pygame.display.flip()

pygame.quit()
