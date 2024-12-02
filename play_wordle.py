from wordle import Matches, Status, PlayResponse, play
from validate_guess import validate_guess
from word_randomizer import get_word_list, get_a_random_word


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

            

#game set up
win_count = 0
loss_count = 0
sum_guesses = 0
num_games = 10000
for i in range(num_games):
    target_length = 5
    max_attempts = 6
    attempt = 0
    status = Status.IN_PROGRESS

    word_pool = get_word_list()


    target = get_a_random_word(word_pool)

    #guesser

    while True:
        try:
            guess = get_a_random_word(word_pool)
        except Exception as e:
            print(e)


        result = play(target, guess, attempt, validate_guess)

        if result[GAME_STATUS] != IN_PROGRESS:
           if result[GAME_STATUS] == WIN:
               sum_guesses += result[ATTEMPTS]
               win_count += 1
           else:
               loss_count += 1
           break

        word_pool = eliminate_possible_guesses(guess, word_pool, result[TALLY_RESPONSE])
        attempt = result[ATTEMPTS]


win_rate = win_count/num_games
loss_rate = loss_count/num_games
avg_guesses = sum_guesses/num_games
efficency_score = win_rate/avg_guesses

print("win rate:", win_rate)
print("loss rate:", loss_rate)
print("average guesses:", avg_guesses)
print("efficiency score:", efficency_score)
