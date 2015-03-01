"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

from operator import abs

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################
    
def free_bacon(opponent_score):
    a = opponent_score//10
    b = opponent_score - 10*a
    score = 1 + abs(a - b)
    return score

def worth_bacon(score, opponent_score, margin = 8):
    bacon_score = free_bacon(opponent_score)
    if score + bacon_score != 2 * opponent_score:
        if bacon_score > margin:
            return True
    return False

def swine_swap(score, op_score):
    if (score == 2 * op_score) or (op_score == 2 * score):
        return op_score, score
    return score, op_score



def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    i, one_count, total = 0, 0, 0
    while i<num_rolls:
        i += 1
        num = dice()
        if num == 1:
            one_count = 1
        total += num
    if one_count == 0:
        return total
    return one_count


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    
    # def free_bacon(opponent_score):
    #     a = opponent_score//10
    #     b = opponent_score - 10*a
    #     score = 1 + abs(a - b)
    #     return score
    
    if num_rolls !=0:
        score = roll_dice(num_rolls, dice)
    else:
        score = free_bacon(opponent_score)
    return score


   

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    if (score + opponent_score)%7 == 0:
        return four_sided
    return six_sided

def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    """Given the bids BID0 and BID1 of each player, returns three values:

    - the starting score of player 0
    - the starting score of player 1
    - the number of the player who rolls first (0 or 1)
    """
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"

    # The buggy code is below:
    if bid0 == bid1:
        return 100, 100, 0
    if bid1 == bid0 - 5:
        return 10, 0, 0
    if bid1 == bid0 + 5:
        return 0, 10, 1
    if bid1 > bid0:
        return bid1, bid0, 1
    else:
        return bid1, bid0, 0

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    # score0, score1, player_now = bid_for_start(bid0, bid1, goal)
    # def swine_swap():
    #     nonlocal score0, score1
    #     if (score0 == 2 * score1) or (score1 == 2 * score0):
    #         score0, score1 = score1, score0

    def game_continue():
        nonlocal score0, score1, goal
        if(score0 >= goal or score1 >= goal):
            return False
        return True
        
    while game_continue():
            score0 += take_turn(strategy0(score0, score1), score1, select_dice(score0, score1))
            score0, score1 = swine_swap(score0, score1)
            if game_continue():
                score1 += take_turn(strategy1(score1, score0), score0, select_dice(score1, score0))
                score1, score0 = swine_swap(score1, score0)

    return score0, score1  # You may want to change this line.

#######################
# Phase 2: Strategies #
#######################

def worth_swap(score, opponent_score):
    if 2 * (score + free_bacon(opponent_score)) == opponent_score:
        return True
    return False

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=10000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def averaged(*arg):
        sum = 0
        for n in range(0, num_samples):
            sum += fn(*arg)
        return sum/num_samples
    return averaged


        

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
    i = 0
    max_num = 0
    avg = 0
    while i < 10:
        i += 1
        t = make_averaged(roll_dice, 10000)(i, dice)
        if t > avg:
            max_num = i
            avg = t
    return max_num



def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(10) win rate:', average_win_rate(always_roll(10)))
        # print('always_roll(9) win rate:', average_win_rate(always_roll(9)))
        # print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
        # print('always_roll(7) win rate:', average_win_rate(always_roll(7)))
        # print('always_roll(6) win rate:', average_win_rate(always_roll(6)))
        # print('always_roll(5) win rate:', average_win_rate(always_roll(5)))
        # print('always_roll(4) win rate:', average_win_rate(always_roll(4)))
        # print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
        # print('always_roll(2) win rate:', average_win_rate(always_roll(2)))
        # print('always_roll(1) win rate:', average_win_rate(always_roll(1)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=4, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    a = opponent_score//10
    b = opponent_score - 10*a
    mar = 1 + abs(a - b)
    if mar >= margin:
        return 0
    return num_rolls 
    # return None # Replace this statement

def swap_strategy(score, opponent_score, margin=4, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    # def worth_swap():
    #     if 2 * (score + free_bacon(opponent_score)) == opponent_score:
    #         return True
    #     return False
    # def worth_bacon():
    #     bacon_score = free_bacon(opponent_score)
    #     if score + bacon_score != 2 * opponent_score:
    #         if bacon_score > margin:
    #             return True
        # return False
    if worth_swap(score, opponent_score):
        return 0
    if worth_bacon(score, opponent_score, margin):
        return 0
    return num_rolls
 
    # return None # Replace this statement


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"



    # if worth_swap(score, opponent_score):
    #     return 0
    # if (score + opponent_score + free_bacon(opponent_score)) %7 == 0:
    #     return 0

    # score > opponent_score

    # def avg_stuff(num_samples = 1000):
    #     """
    #     >>> avg_stuff()
    #     0

    #     """
    #     reference = []
    #     for i in range(1, 11):
    #         k = 0
    #         total = 0
    #         while k < num_samples:
    #             k += 1
    #             total += roll_dice(i)
    #         temp_poss = total/num_samples
    #         reference.append(temp_poss)
    #         # print(reference[i - 1])
    #     return reference

    # reference = avg_stuff()
    # reference = [3.495, 5.809, 7.522, 8.116, 8.144, 8.787, 8.662, 8.245, 8.372, 7.659]
    reference = [3, 5, 7, 8, 8, 8, 8, 8, 8, 7]

    if score >= 90:
        if worth_bacon(score, opponent_score, 1):
            # if (score + opponent_score + free_bacon(opponent_score)) %7 == 0:
            return 0
        temp_roll = 7
        if (score + opponent_score + temp_roll) % 7 == 0:
            return 10
        elif worth_swap(score + temp_roll, opponent_score):
            return 10
    if score < 10:
        if worth_bacon(score, opponent_score, 7):
            # if (score + opponent_score + free_bacon(opponent_score)) %7 == 0:
            #     return 0
            # if worth_swap(score, opponent_score):
            return 0
        temp_roll = 7
        if (score + opponent_score + temp_roll) % 7 == 0:
            return 10
        elif worth_swap(score + temp_roll, opponent_score):
            return 10
    if score >= 10 and score < 40:
        if worth_bacon(score, opponent_score, 5):
            return 0
        temp_roll = 8
        if worth_swap(score + temp_roll, opponent_score):
            return 5

    # if score < 50 and opponent_score - score > 20:
    #     if worth_bacon(score, opponent_score, 6):
    #         return 0
    #     for i in range(1, 11):
    #         if 2* (score + reference[i - 1]) == opponent_score:
    #             return i
    #     for i in range(1, 11):
    #         if (score + opponent_score + reference[i - 1]) % 7 == 0:
    #             return i


    # # score < opponent_score
    # if opponent_score - score > 20:
    #     for i in range(1, 11):
    #         if 2 * (score + round (reference[i - 1])) == opponent_score:
    #             return i
    #     for i in range(1, 11):
    #         if (score + opponent_score + round (reference[i - 1])) % 7 == 0:
    #             return i
    #     if worth_bacon(score, opponent_score, 4):
    #         return 0
     

    return 5 # Replace this statement


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
