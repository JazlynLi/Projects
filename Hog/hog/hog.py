"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

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
    result, pig_out = 0, False
    for num in range(0, num_rolls):
        increment = dice()
        if increment == 1:
            pig_out = True
        result += increment
    if pig_out:
        return 1
    return result

def free_bacon(opponent_score):
    """Return the points gained by the Free Bacon Rule."""
    digit_1 = opponent_score % 10
    digit_10 = (opponent_score - digit_1) / 10
    return (int)(abs(digit_1 - digit_10)) + 1

def swine_swap(score, opponent_score):
    """Return swapped scores if the game is in a swine_swap situation, 
    otherwise return the original scores."""
    if score == 2 * opponent_score or opponent_score == 2 * score:
        return opponent_score, score
    return score, opponent_score

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
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    if (score + opponent_score) % 7 == 0:
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
        return goal, goal, 0
    elif bid0 == bid1 + 5:
        return 10, 0, 0
    elif bid1 == bid0 + 5:
        return 0, 10, 1
    elif bid1 > bid0:
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
    while score0 < goal and score1 < goal:
        # Player 0's round
        s0 = strategy0(score0, score1)
        score0 += take_turn(s0, score1, select_dice(score0, score1))
        if score0 < goal and score1 < goal:
            score0, score1 = swine_swap(score0, score1)
            # Palyer 1's round
            s1 = strategy1(score1, score0)
            score1 += take_turn(s1, score0, select_dice(score1, score0))
            if score0 < goal and score1 < goal:
                score1, score0 = swine_swap(score1, score0)

    return score0, score1

#######################
# Phase 2: Strategies #
#######################

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

def make_averaged(fn, num_samples=30000):
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
    def average_value(*args):
        summation = 0
        for n in range(0, num_samples):
            summation += fn(*args)
        return summation / num_samples
    return average_value

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
    current_max_return, num_dice = 0, 0
    average_dice = make_averaged(roll_dice)
    for n in range(1, 11):
        average_return = average_dice(n, dice)
        if average_return > current_max_return:
            current_max_return, num_dice = average_return, n
    return num_dice

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
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def worth_bacon(score, opponent_score, margin=8):
    """Return True if taking free_bacon won't lead to a harmful swap
    and the free_bacon is larger than MARGIN, otherwise return false."""
    bacon_score = free_bacon(opponent_score)
    if score + bacon_score != 2 * opponent_score:
        if bacon_score >= margin:
            return True
    return False

def worth_swap(score, opponent_score):
    """Return True if scores would result in a beneficial swap, otherwise
    return False."""
    if 2 * (score + free_bacon(opponent_score)) == opponent_score:
        return True
    return False

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    if free_bacon(opponent_score) >= margin:
        return 0
    return num_rolls

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    if worth_swap(score, opponent_score):
        return 0
    if worth_bacon(score, opponent_score, margin):
        return 0
    return num_rolls

def hog_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a hog wild for the 
    opponent and rolls 0 if it that gives at least MARGIN points and rolls 
    NUM_ROLLS otherwise."""
    if can_hog(score, opponent_score):
        return 0
    if worth_bacon(score, opponent_score, margin):
        return 0
    return num_rolls

# Functions for final_strategy
def safe_from_harmful_swap(score, opponent_score, method):
    """Return True if METHOD won't result in harmful swap, otherwise 
    return False.

    METHOD == 0 represents free_bacon 
    METHOD == 10 represents taking 1 point"""
    baconed_score = score + free_bacon(opponent_score)
    if (method == 0) and (baconed_score == 2 * opponent_score):
        return False
    if (method == 10) and (score + 1 == 2 * opponent_score):
        return False
    return True

def should_take_1(score, opponent_score):
    """Return True if taking 1 point will result in beneficial swap or hog, 
    otherwise return False."""
    if 2 * (score + 1) == opponent_score:
        return True
    if (score + 1 + opponent_score) % 7 == 0:
        return True
    return False

def can_swap(score, opponent_score, method):
    """Return True if a beneficial swap can be achieved by free_bacon
    OR by taking 1 point, otherwise return False.

    Method == 0 represents using free_bacon 
    Method == 10 represents taking 1 point"""
    bacon_score = free_bacon(opponent_score)
    if (method == 0) and (2 * (score + bacon_score) == opponent_score):
        return True
    if (method == 10) and (2 * (score + 1) == opponent_score):
        return True
    return False

def can_hog(score, opponent_score, method):
    """Return True if a hog wild can be created by free_bacon OR by taking 
    1 point, otherwise return False.

    Method == 0 represents using free_bacon 
    Method == 10 represents taking 1 point"""
    bacon_score = free_bacon(opponent_score)
    if (method == 0) and ((score + bacon_score + opponent_score) % 7 == 0):
        return True
    if (method == 10) and ((score + 1 + opponent_score) % 7 == 0):
        return True
    return False

def should_swap(score, opponent_score, margin=1):
    """Return True if swine_swap is more beneficial than hog, 
    otherwise return False."""
    if opponent_score - score > margin:
        return True
    return False

def appropriate_margin(score, opponent_score):
    """Return the appropriate margin for bacon_strategy based
    on the current situation."""
    points_to_win = GOAL_SCORE - score
    difference = opponent_score - score
    if score > opponent_score:
        if points_to_win >= 10:
            return 8
        elif points_to_win >= 6:
            return 5
        elif points_to_win >= 2:
            return 2
        else: 
            return 1
    else: 
        if GOAL_SCORE - opponent_score < 5:
            return GOAL_SCORE - score
        if difference <= 5:
            return 8
        elif difference <= 10: 
            return 9
        else:
            return 10

def is_hogged(score, opponent_score):
    """Return True if the current player is hogged for this round,
    otherwise return False."""
    if (score + opponent_score) % 7 == 0:
        return True
    return False

def appropriate_rolls(score, opponent_score):
    """Return the appropriate num_rolls based on the current situation."""
    points_to_win = GOAL_SCORE - score
    difference = opponent_score - score
    if is_hogged(score, opponent_score):
        if score >= opponent_score:
            if points_to_win > 5:
                return 3
            elif points_to_win > 2:
                return 2
            else: 
                return 1
        else:
            if difference <= 10:
                return 4
            elif difference <= 20:
                return 5
            elif difference <= 30:
                return 6
            elif difference <= 60:
                return 9
            else:
                return 10
    else:
        if score >= opponent_score:
            if points_to_win > 14:
                return 5
            elif points_to_win > 10:
                return 4
            elif points_to_win > 6:
                return 3
            elif points_to_win > 2:
                return 2
            else: 
                return 1
        else:
            if GOAL_SCORE - opponent_score < 8 and difference < 5:
                return 7
            elif difference <= 10:
                return 6
            elif difference <= 20:
                return 7
            elif difference <= 40:
                return 8
            elif difference <= 60:
                return 9
            else:
                return 10

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    0. Always Always Always avoid harmful Swine Swap. (The Zeroth Rule!)
    1. If taking a free bacon can result in victory, then take the bacon.
    2. Always try to create benefitial Swine Swap and Hog Wild (by taking free
       bacon or roll 10).
    3. Make wise decision when there's a Dilemma --  when Swine Swap and Hog 
       Wild can be achieved by different means in the same round.
    4. Adjusting the number of rolls according to the current game condition. 
       (floating risk level)
    """
    "*** YOUR CODE HERE ***"
    # One step winning.
    if free_bacon(opponent_score) >= GOAL_SCORE - score:
        return 0

    # Dilemma: Condition in which benefitial swap and hog are both achievable
    # but not at the same time.
    if can_swap(score, opponent_score, 0) and can_hog(score, opponent_score, 10):
        if should_swap(score, opponent_score):
            if safe_from_harmful_swap(score, opponent_score, 0):
                return 0
        elif safe_from_harmful_swap(score, opponent_score, 10):
            return 10
    if can_swap(score, opponent_score, 10) and can_hog(score, opponent_score, 0):
        if should_swap(score, opponent_score):
            if safe_from_harmful_swap(score, opponent_score, 10):
                return 10
        elif safe_from_harmful_swap(score, opponent_score, 0):
            return 0

    # Free_bacon: to create either a swap or a hog, or both at the same time.
    if safe_from_harmful_swap(score, opponent_score, 0):
        if can_swap(score, opponent_score, 0):
            return 0
        elif can_hog(score, opponent_score, 0):
            return 0
        else:
            margin = appropriate_margin(score, opponent_score)
            num_rolls = appropriate_rolls(score, opponent_score)
            return bacon_strategy(score, opponent_score, margin, num_rolls)

    # Return 10 rolls (in order to get 1 point): to create either a swap or a
    # hog, or both at the same time.
    if should_take_1(score, opponent_score):
        if can_swap(score, opponent_score, 10):
            return 10
        elif can_hog(score, opponent_score, 10):
            return 10

    # Baseline: When neither swap or hog is possible.
    else:
        num_rolls = appropriate_rolls(score, opponent_score)
        return num_rolls
    

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
