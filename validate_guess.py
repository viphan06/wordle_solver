def validate_guess(guess_word):
    file = open("wordle-allowed-guesses.txt", "r")
    
    return (guess_word in file.read())
