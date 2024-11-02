from enum import Enum


TARGET_LENGTH = 5
MAX_ATTEMPTS = 6

class Matches(Enum):
    EXACT_MATCH = 'green'
    PARTIAL_MATCH = 'yellow'
    WRONG_MATCH = 'gray'
    
class Status(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    WIN = "WIN"
    LOSS = "LOSS"

class PlayResponse(Enum):
    ATTEMPTS = "Attempts: "
    TALLY_RESPONSE = "Tally Response: "
    GAME_STATUS = "Game Status: "
    MESSAGE = "Message: "
   
def count_letters(word):
    letter_count = {}
    for letter in word:
        if letter in letter_count:
            letter_count[letter]+=1
        else:
            letter_count[letter] = 1
    return letter_count

def tally(target, guess): 
    result = []
    word_dict = count_letters(target)

    for i in range(len(guess)):

        if target[i] == guess[i]:
            word_dict[target[i]] -= 1
            result.append(Matches.EXACT_MATCH)

        elif guess[i] in word_dict and word_dict[guess[i]] > 0:
            word_dict[guess[i]] -=1
            result.append(Matches.PARTIAL_MATCH)
        else:
            result.append(Matches.WRONG_MATCH)

    return result
  

def tally_for_position(index, target, guess):
    if target[index] == guess[index]:
        return Matches.EXACT_MATCH

    letter_guess = guess[index]

    total_exact_occurrences = count_occurrences(target, guess, letter_guess)
    total_partial_occurrences = count_occurrences_until_index(len(target) - 1, target, letter_guess) - total_exact_occurrences

    total_occurrences_guess_until_position = count_occurrences_until_index(index, guess, letter_guess)

    if total_partial_occurrences >= total_occurrences_guess_until_position:
        return Matches.PARTIAL_MATCH

    return Matches.WRONG_MATCH


def count_occurrences(target, guess, letter):
    return sum(1 for i in range(len(target)) if target[i] == guess[i] == letter)


def count_occurrences_until_index(index, word, letter):
    matches = word[:index + 1].count(letter)
    return matches if matches else 0


def validate_number_of_attempts(current_attempt): 
    return current_attempt < MAX_ATTEMPTS

    
def get_game_status(attempt_validity, tally_score, attempt):
    if attempt_validity:
        if tally_score == [Matches.EXACT_MATCH] * TARGET_LENGTH:
            return Status.WIN
        
        if attempt == MAX_ATTEMPTS - 1:
            return Status.LOSS
        
        return Status.IN_PROGRESS

    return Status.LOSS


def get_game_message(game_status, attempt, target):
    if game_status == Status.WIN:
        win_message = {0: "Amazing!",
                   1: "Splendid!",
                   2: "Awesome!",
                   3: "Yay!",
                   4: "Yay!",
                   5: "Yay!"}
        return win_message[attempt]
    
    if game_status == Status.IN_PROGRESS:
        return ""

    return "It was " + target + ", better luck next time!"


def play(target, guess, attempt, validate_guess = lambda word: True):
    attempt_validity = validate_number_of_attempts(attempt)
    
    if not validate_guess(guess):
        raise ValueError("invalid guess, please check length, spelling, and charac")

    tally_score = tally(target, guess)
    
    game_status = get_game_status(attempt_validity, tally_score, attempt)

    message = get_game_message(game_status, attempt, target)

    return {PlayResponse.ATTEMPTS : attempt + 1,
            PlayResponse.TALLY_RESPONSE : tally_score,
            PlayResponse.GAME_STATUS : game_status, 
            PlayResponse.MESSAGE : message }
