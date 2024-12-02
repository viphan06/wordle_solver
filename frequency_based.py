from wordle import Matches, Status, PlayResponse, play
from validate_guess import validate_guess
from word_randomizer import get_word_list, get_a_random_word

globals().update(PlayResponse.__members__)
globals().update(Status.__members__)
globals().update(Matches.__members__)

def calculate_letter_frequencies(word_list):
    """Calculate the frequency of each letter in the word list."""
    from collections import Counter
    letter_counts = Counter()
    for word in word_list:
        letter_counts.update(set(word))
    return letter_counts


def score_words(word_list, letter_frequencies):
    """Score words based on the frequency of their unique letters."""
    scored_words = {}
    for word in word_list:
        scored_words[word] = sum(letter_frequencies[char] for char in set(word))
    return scored_words

def get_best_guess(word_list):
    """Get the word with the highest score."""
    letter_frequencies = calculate_letter_frequencies(word_list)
    scored_words = score_words(word_list, letter_frequencies)
    return max(scored_words, key=scored_words.get)

def eliminate_possible_guesses(guess, word_list, matches):
    filtered_list = word_list
    for i in range(len(matches)):

        # Green match
        if matches[i] == EXACT_MATCH:
            filtered_list = [word for word in filtered_list if word[i] == guess[i]]

        # Yellow match
        elif matches[i] == PARTIAL_MATCH:
            filtered_list = [
                word for word in filtered_list
                if word[i] != guess[i] and word.count(guess[i]) >= guess[:i+1].count(guess[i])
            ]

        # Gray match
        else:
            filtered_list = [
                word for word in filtered_list
                if word.count(guess[i]) < guess.count(guess[i])
            ]
    return filtered_list

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

    # Guesser
    while True:
        try:
            guess = get_best_guess(word_pool)
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
efficiency_score = win_rate/avg_guesses

print("win rate:", win_rate)
print("loss rate:", loss_rate)
print("average guesses:", avg_guesses)
print("efficiency score:", efficiency_score)
