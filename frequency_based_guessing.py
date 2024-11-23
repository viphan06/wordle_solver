from collections import Counter
import random

def get_word_list():
    return ["apple", "grape", "berry", "melon", "peach", "plumb", "lemon"]

def get_a_random_word(word_list):
    return random.choice(word_list)

def get_letter_frequencies(word_list):
    # Flatten the list of words into a single string and count the frequency of each letter
    all_letters = ''.join(word_list)
    return Counter(all_letters)

def make_guess(word_list, letter_frequencies):
    # Score each word based on the frequency of its letters
    word_scores = {word: sum(letter_frequencies[letter] for letter in word) for word in word_list}
    # Return the word with the highest score
    return max(word_scores, key=word_scores.get)

def play_game():
    word_list = get_word_list()
    target_word = get_a_random_word(word_list)
    letter_frequencies = get_letter_frequencies(word_list)
    
    max_attempts = 6
    attempts = 0
    guessed_correctly = False

    while attempts < max_attempts and not guessed_correctly:
        guess = make_guess(word_list, letter_frequencies)
        print(f"Attempt {attempts + 1}: Guessing '{guess}'")
        
        if guess == target_word:
            guessed_correctly = True
            print("Guessed correctly!")
        else:
            # Filter the word list based on the guess
            word_list = [word for word in word_list if word != guess]
            letter_frequencies = get_letter_frequencies(word_list)
        
        attempts += 1

    if not guessed_correctly:
        print(f"Failed to guess the word. The correct word was '{target_word}'.")

if __name__ == "__main__":
    play_game()