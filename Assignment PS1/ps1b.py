###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Lynn Zhang
# Collaborators:
# Time: 90min
# 2021-04-03 08:55 - 09:55 used recursive, looks like greedy, but seems optimal. how to use memo in this case?
#                           - a bit stuck and then googled the thinking logic and tried it by myself - draw the tree
#            11:30 - 12:00 figured out the dynamic programming! - NEED TO LIST OUT ALL THE POSSIBILITIES AND COMPARE
#                           memo dict: key: (tuple,weight) -> value: min number of egg
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1

# IMPLEMENTATION 1 - RECURSIVE & Greedy - seems optimal?
# NO! may be optimal in the 1,5,10,25 - 99 case; but not optimal in 1,6,9 - 14 case!
# wrong implementation
def greedy_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # base, if only one egg, easy to do
    if len(egg_weights) == 1:
        return int(target_weight/egg_weights[0])
    elif egg_weights[-1] > target_weight:
        # Explore right branch only
        return greedy_make_weight(egg_weights[0:len(egg_weights)-1], target_weight, memo)
    else:
        # take the max weight - last element in tuple
        max_current_weight = egg_weights[-1]
        # use max to fill the weight -> min number
        min_number_egg_v1 = greedy_make_weight((max_current_weight,), target_weight)

        # how much weight left after the max egg occupies the space
        weight_left = target_weight - max_current_weight * min_number_egg_v1
        # calculate the min number for the eggs left with weight left
        min_number_egg_v2 = greedy_make_weight(egg_weights[0:len(egg_weights)-1], weight_left)

        # total min number of egg needed
        total_min_number_egg = min_number_egg_v1 + min_number_egg_v2

        return total_min_number_egg

def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    #
    if (egg_weights, target_weight) in memo:
        result = memo[(egg_weights, target_weight)]
    elif egg_weights == () or target_weight == 0:
        result = 0
    elif len(egg_weights) == 1:
        result = target_weight    # Self note: wrong code: result = 1. NO! result(min of egg) = target_weight
    elif egg_weights[-1] > target_weight:
        # Explore right branch only
        result = dp_make_weight(egg_weights[0:len(egg_weights)-1], target_weight, memo)
    else:
        nextItem = egg_weights[-1]
        # Explore left branch
        withMin = dp_make_weight(egg_weights[0:len(egg_weights)],
                                 target_weight - nextItem, memo)
        withMin += 1
        # Explore right branch
        withoutMin = dp_make_weight(egg_weights[0:len(egg_weights)-1], target_weight, memo)
        # Choose better branch
        if withMin < withoutMin:
            result = withMin
        else:
            result = withoutMin
    memo[(egg_weights, target_weight)] = result
    return result


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    #
    # # test one egg situation
    # egg_weights = (1,)
    # n = 99
    # print("Egg weights = (1)")
    # print("n = 99")
    # print("Expected output: 99")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()

    # # test two egg situation
    # egg_weights = (1,5)
    # n = 99
    # print("Egg weights = (1,5)")
    # print("n = 99")
    # print("Expected output: 99")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()

    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected output: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 6, 9)
    n = 14
    print("Egg weights = (1, 6, 9)")
    print("n = 14")
    print("Expected output: 4 (2 * 6 + 2 * 1 = 14)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print("Greedy output:", greedy_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 6, 9, 12, 13, 15)
    n = 724
    print("Egg weights = (1, 6, 9, 12, 13, 15)")
    print("n = 724")
    print("Expected output: 49")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print("Greedy output:", greedy_make_weight(egg_weights, n))
    print()


