import random


def get_word_list():
    file = open("wordle-allowed-guesses.txt", "r")
    words_text = file.read()
    
    if not words_text:
        raise ValueError("No words found in response")
    
    return words_text.splitlines()

def get_a_random_word(word_list):
    return random.choice(word_list)