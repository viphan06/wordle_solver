from wordle import Matches, Status, PlayResponse, play
from word_randomizer import get_word_list, get_a_random_word

globals().update(PlayResponse.__members__)
globals().update(Status.__members__)
globals().update(Matches.__members__)


def filter_word_list(word_list, exact_matches, partial_matches, excluded_letters):
    """
    Filters the word list based on feedback:
    - Exact matches (green) must be in the correct positions.
    - Partial matches (yellow) must be in the word but in different positions.
    - Excluded letters (gray) must not appear in the word.
    """
    filtered_list = []

    for word in word_list:
        # Skip words with excluded letters
        if any(letter in excluded_letters for letter in word):
            continue

        # Ensure exact matches are in the correct positions
        if not all(word[i] == letter for i, letter in exact_matches.items()):
            continue

        # Ensure partial matches are included but in different positions
        if not all(word[i] != letter and letter in word for letter, i in partial_matches.items()):
            continue

        filtered_list.append(word)

    return filtered_list


def rule_based_guess(word_list, exact_matches, partial_matches, excluded_letters):
    """
    Makes a guess based on simple rules:
    - Respects exact matches (green).
    - Avoids placing partial matches (yellow) in the same positions.
    - Excludes gray matches completely.
    """

    def score_word(word):
        # Base score: prefer words with unique letters
        unique_letters = set(word)
        score = len(unique_letters)

        # Bonus for containing exact matches
        score += sum(1 for i, letter in exact_matches.items() if word[i] == letter)

        # Bonus for containing partial matches
        score += sum(1 for letter in partial_matches.keys() if letter in word)

        # Penalty for containing excluded letters
        score -= sum(1 for letter in word if letter in excluded_letters)

        return score

    # Filter the word list based on feedback
    filtered_list = filter_word_list(word_list, exact_matches, partial_matches, excluded_letters)

    # Choose the best-scoring word
    return max(filtered_list, key=score_word) if filtered_list else None


def play_wordle():
    """
    Runs a single Wordle game with rule-based guessing.
    """
    word_list = get_word_list()
    target_word = get_a_random_word(word_list)
    max_attempts = 6
    attempts = 0
    exact_matches = {}
    partial_matches = {}
    excluded_letters = set()

    print(f"The target word is '{target_word}' (hidden in real gameplay).")

    while attempts < max_attempts:
        guess = rule_based_guess(word_list, exact_matches, partial_matches, excluded_letters)
        if not guess:
            print("No valid guesses remaining. You lose!")
            break

        print(f"Attempt {attempts + 1}: Guessing '{guess}'")

        if guess == target_word:
            print(f"Guessed correctly in {attempts + 1} attempts! The word was '{target_word}'.")
            return

        # Get feedback
        matches = [
            Matches.EXACT_MATCH if guess[i] == target_word[i]
            else Matches.PARTIAL_MATCH if guess[i] in target_word
            else Matches.WRONG_MATCH
            for i in range(len(guess))
        ]

        # Update feedback tracking
        for i, match in enumerate(matches):
            if match == Matches.EXACT_MATCH:
                exact_matches[i] = guess[i]
            elif match == Matches.PARTIAL_MATCH:
                partial_matches[guess[i]] = i
            elif match == Matches.WRONG_MATCH:
                excluded_letters.add(guess[i])

        # Remove the guess from the word list
        word_list = [word for word in word_list if word != guess]

        attempts += 1

    print(f"Failed to guess the word. The correct word was '{target_word}'.")


######

# Uncomment the function below to run 10,000 games and calculate metrics
# def simulate_wordle_with_metrics(num_games=10000):
#     win_count = 0
#     loss_count = 0
#     total_guesses_for_wins = 0
#
#     for _ in range(num_games):
#         word_list = get_word_list()
#         target_word = get_a_random_word(word_list)
#         max_attempts = 6
#         attempts = 0
#         guessed_correctly = False
#
#         # Feedback tracking
#         exact_matches = {}
#         partial_matches = {}
#         excluded_letters = set()
#
#         while attempts < max_attempts and not guessed_correctly:
#             guess = rule_based_guess(word_list, exact_matches, partial_matches, excluded_letters)
#             if not guess:
#                 break
#
#             if guess == target_word:
#                 guessed_correctly = True
#                 win_count += 1
#                 total_guesses_for_wins += (attempts + 1)
#                 break
#
#             matches = [
#                 Matches.EXACT_MATCH if guess[i] == target_word[i]
#                 else Matches.PARTIAL_MATCH if guess[i] in target_word
#                 else Matches.WRONG_MATCH
#                 for i in range(len(guess))
#             ]
#
#             for i, match in enumerate(matches):
#                 if match == Matches.EXACT_MATCH:
#                     exact_matches[i] = guess[i]
#                 elif match == Matches.PARTIAL_MATCH:
#                     partial_matches[guess[i]] = i
#                 elif match == Matches.WRONG_MATCH:
#                     excluded_letters.add(guess[i])
#
#             word_list = [word for word in word_list if word != guess]
#             attempts += 1
#
#         if not guessed_correctly:
#             loss_count += 1
#
#     # Calculate metrics
#     win_rate = win_count / num_games
#     loss_rate = loss_count / num_games
#     avg_guesses = total_guesses_for_wins / win_count if win_count > 0 else 0
#     efficiency_score = win_rate / avg_guesses if avg_guesses > 0 else 0
#
#     # Display results
#     print(f"Win Rate: {win_rate:.4f}")
#     print(f"Loss Rate: {loss_rate:.4f}")
#     print(f"Average Guesses (Wins): {avg_guesses:.2f}")
#     print(f"Efficiency Score: {efficiency_score:.4f}")


if __name__ == "__main__":
    play_wordle()  # Play a single Wordle game interactively

    # Uncomment the line below to run the simulation
    # simulate_wordle_with_metrics(num_games=10000)
