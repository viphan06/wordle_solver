from wordle import Matches, Status, PlayResponse, play
from validate_guess import validate_guess
from word_randomizer import get_word_list, get_a_random_word, get_starter_word_list
import random


globals().update(PlayResponse.__members__)
globals().update(Status.__members__)
globals().update(Matches.__members__)

def eliminate_possible_guesses(guess, word_list, matches):
    filtered_list = word_list
    for i in range(len(matches)): #loops through the guess result
        
#green match: takes in all words with letter in same position as green position and discards the rest
        if matches[i] == EXACT_MATCH: 
            filtered_list = [word for word in filtered_list if word[i] == guess[i]]
            
        #yellow match: removes all words with letter as same position as the yellow
        #removes all words where the count of the letter is less than the count of the letter in the guess word up to that index
        elif matches[i] == PARTIAL_MATCH: 
            filtered_list = [word for word in filtered_list if word[i] != guess[i] and word.count(guess[i]) >= guess[:i+1].count(guess[i])]
            
        #gray match removes all words with the letter count greater than letter count in guess
        else:
            filtered_list = [word for word in filtered_list if word.count(guess[i]) < guess.count(guess[i])] #fix for multiple letters
    return filtered_list

   
#According to NYTimes, the best starter words according to
# the WordleBot are SLATE, CRANE, TRACE 
#https://www.nytimes.com/2023/12/17/upshot/wordle-bot-year-in-review.html#

#Note that if you want to add another starter word, you must make sure that it
#is inside BOTH best_starter_words.txt AND wordle-allowed-guesses.txt
starter_words = get_starter_word_list()

for first_word in starter_words:
    print("Starter word: " + first_word) 
    win_count = 0
    attempts_list = []       

    #game set up
    for i in range(1000):
        target_length = 5
        max_attempts = 6
        attempt = 0
        status = Status.IN_PROGRESS

        word_pool = get_word_list()


        target = get_a_random_word(word_pool)


        guess_list = []
        pool_list = []
        


        #guesser
        first_guess = True
        while True:
            try:
                if first_guess:
                    guess = first_word
                    first_guess = False
                else:
                    guess = get_a_random_word(word_pool) #implement a starter_word/good guessing algo'


            except Exception as e:
                print(e)
                print( guess_list, target.upper())
                for pol in pool_list:
                    print(pol)
            guess_list.append(guess)
            result = play(target, guess, attempt, validate_guess)

            if result[GAME_STATUS] != IN_PROGRESS:
                #print(result[GAME_STATUS], result[ATTEMPTS], target)
                if result[GAME_STATUS] == Status.WIN:
                    win_count += 1
                    attempts_list.append(result[ATTEMPTS])
                break

            word_pool = eliminate_possible_guesses(guess, word_pool, result[TALLY_RESPONSE])
            pool_list.append(word_pool)
            attempt = result[ATTEMPTS]
    
    win_rate = win_count/1000
    if attempts_list:
        average_guesses = sum(attempts_list) / len(attempts_list)
    else:
        average_guesses = 0
    print(f"\tWin Rate: {win_rate}\n\tAvg. # Guesses per Game: {round(average_guesses, 2)}")


