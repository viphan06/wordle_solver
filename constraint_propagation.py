from collections import Counter
from wordle import Matches, Status, PlayResponse, play
from word_randomizer import get_word_list, get_a_random_word
from play_wordle import eliminate_possible_guesses

def get_letter_frequencies(word_list):
    # Flatten the list of words into a single string and count the frequency of each letter
    all_letters = ''.join(word_list)
    return Counter(all_letters)

def make_guess(word_list, letter_frequencies, guessed_words):
    # Score each word based on the frequency of its letters
    word_scores = {word: sum(letter_frequencies[letter] for letter in word) for word in word_list if word not in guessed_words}
    # Return the word with the highest score
    if word_scores:
        return max(word_scores, key=word_scores.get)
    else:
        return None

def play_wordle_with_frequency():
    word_list = get_word_list()
    target_word = get_a_random_word(word_list)
    letter_frequencies = get_letter_frequencies(word_list)
    
    max_attempts = 6
    attempts = 0
    guessed_correctly = False
    guessed_words = set()

    while attempts < max_attempts and not guessed_correctly:
        guess = make_guess(word_list, letter_frequencies, guessed_words)
        if not guess:
            print("No more words to guess.")
            break
        print(f"Attempt {attempts + 1}: Guessing '{guess}'")
        
        if guess == target_word:
            guessed_correctly = True
            print("Guessed correctly!")
        else:
            # Add the guess to the set of guessed words
            guessed_words.add(guess)
            # Get the match results (this would be provided by the game logic)
            matches = [Matches.EXACT_MATCH if guess[i] == target_word[i] else Matches.PARTIAL_MATCH if guess[i] in target_word else Matches.WRONG_MATCH for i in range(len(guess))]
            # Filter the word list based on the guess and matches
            word_list = eliminate_possible_guesses(guess, word_list, matches)
            letter_frequencies = get_letter_frequencies(word_list)
        
        attempts += 1

    if not guessed_correctly:
        print(f"Failed to guess the word. The correct word was '{target_word}'.")

if __name__ == "__main__":
    play_wordle_with_frequency()