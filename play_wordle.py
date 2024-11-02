from wordle import Matches, Status, PlayResponse, play
from agilec_spellcheck_service import validate_guess
from agilec_randomizer_service import get_word_list, get_a_random_word


globals().update(PlayResponse.__members__)
globals().update(Status.__members__)
globals().update(Matches.__members__)

def eliminate_possible_guesses(guess, word_list, matches):
    filtered_list = word_list
    for i in range(len(matches)):

        if matches[i] == EXACT_MATCH:
            filtered_list = [word for word in filtered_list if word[i] == guess[i]]

        elif matches[i] == PARTIAL_MATCH:
            filtered_list = [word for word in filtered_list if word[i] != guess[i] and word.count(guess[i]) >= guess[:i+1].count(guess[i])] #fix for multiple letters

        else:
            filtered_list = [word for word in filtered_list if word.count(guess[i]) < guess.count(guess[i])] #fix for multiple letters
    return filtered_list

            

#game set up
for i in range(1000000):
    target_length = 5
    max_attempts = 6
    attempt = 0
    status = Status.IN_PROGRESS

    word_pool = get_word_list()


    target = get_a_random_word(word_pool)


    guess_list = []
    pool_list = []

    #guesser

    while True:
        try:
            guess = get_a_random_word(word_pool) #implement a starter_word/good guessing algo'
        except Exception as e:
            print(e)
            print( guess_list, target.upper())
            for pol in pool_list:
                print(pol)
        guess_list.append(guess)
        result = play(target, guess, attempt, validate_guess)

        if result[GAME_STATUS] != IN_PROGRESS:
           # print(result[GAME_STATUS], result[ATTEMPTS], target)
            break

        word_pool = eliminate_possible_guesses(guess, word_pool, result[TALLY_RESPONSE])
        pool_list.append(word_pool)
        attempt = result[ATTEMPTS]


