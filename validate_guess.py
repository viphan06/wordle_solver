def is_spelling_correct(guess_word):
    file = open("wordle-allowed-guesses.txt", "r")
    return guess_word in file.read()

def validate_guess(guess_word):
    with open("wordle-allowed-guesses.txt", "r") as file:
        return guess_word in file.read()
