###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Lynn Zhang
# Collaborators:
# Time: 123min
# 2021-04-02 06:22 - 07:00 greedy
#            07:30 - 07:50 greedy debugging and complete
#            08:30 - 09:15 brute force - issue (partition not go from 0, 1, 2 more in an orderly manner)
#            09:50 - 10:00 modify the code to brute force on all possible choices
#            10:00 - 10:10 complete compare
from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

COW_FILE = 'ps1_cow_data.txt'

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = {}   # cow dictionary

    # read the file
    f = open(filename, 'r')
    # with open(filename) as f:    # more efficient way to read the file, also close the file after
    #     read_data = f.read()
    for line in f:
        cow_data = line.split(',')
        cow_dict[cow_data[0]] = int(cow_data[1].strip())    # weight value: get rid of \n and change to integer
    f.close()

    return cow_dict


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # initialization
    cows_total = cows.copy()   # need to make the copy, otherwise refer to the same one
    trip_list = []
    space_total = limit   # space on the spaceship
    # as long as cows_left is not none, do follows
    while len(cows_total) > 0:
        # trip list initialization
        trip = []
        cows_left = {}
        # as long as the space is not less than or equal to 0, still can find the next heaviest
        # in this loop, need to find the max that can be taken on the spaceship
        # print('Trip', num_trip)
        while space_total > 0 and len(cows_total) > 0:
            # find the heaviest in the cows_left - need to
            heaviest_cow = max(cows_total, key=cows_total.get)   # get the key with max value in dict
            heaviest_weight = max(cows_total.values())
            # print('The heaviest_cow is,', heaviest_cow, 'with the weight', heaviest_weight)
            # if the weight is less than the current limit, then add in the list.
            if heaviest_weight <= space_total:
                # print('It has now added to the spaceship')
                trip.append(heaviest_cow)
                # update the cows_total and space
                space_total -= heaviest_weight
                # print('Space left:',space_total)
            else:
                # print('It is too heavy. Cannot be added to the spaceship')
                cows_left[heaviest_cow] = heaviest_weight
            del (cows_total[heaviest_cow])
        # combine cows_left with cows_total
        cows_total.update(cows_left)
        trip_list.append(trip)
        # go for the next trip, space is available again
        # print('Next trip')
        # print('==============')
        space_total = limit
    return trip_list

# Problem 3
def sum_list_weight_from_dict(cow_list,cow_dict):
    weight_sum = 0
    for item in cow_list:
        weight_sum += cow_dict[item]
    return weight_sum

def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    # init
    cows_total = cows.copy()
    cows_list = cows_total.keys()

    # keep track of all the possible results in the result
    possible_partition = []
    for partition in get_partitions(cows_list):     # generator always starts with min partition; but not guaranteed to increase gradually
        # print(partition)
        num_partition = len(partition)
        # print('Number partition:', num_partition)
        find_mark = False
        # loop in the partition and check each list, weight should be within the limit
        for i in range(num_partition):
            # calculate the total weight of the partition
            weight_partition = sum_list_weight_from_dict(partition[i], cows_total)      # note: partition is a list of lists
            # print('weight is', weight_partition)
            # check whether it is within the weight limit
            # if yes, then return
            if weight_partition <= limit:
                # print('This set can go')
                find_mark = True
            # if not, continue the loop
            else:
                # print('Overweight! Try next...')
                find_mark = False
                break  # as long as there is one set that does not meet the requirement, no need to check others
        if find_mark == True:
            # print('Find it!')
            # print('Current partition is:', num_partition)
            # print(partition)
            possible_partition.append(partition)
    # print(possible_partition)
    min_partition = len(cows_list)
    for item in possible_partition:
        if len(item) < min_partition:
            min_partition = len(item)
            min_trip_list = item
    # print(min_partition)
    # print(min_trip_list)
    return min_trip_list
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # load the cows dict
    cows = load_cows(COW_FILE)
    # run greedy, print out the trip and keep track of the time and print out
    start = time.time()
    greedy_list = greedy_cow_transport(cows)
    print('Number of trip using Greedy is', len(greedy_list))
    end = time.time()
    print('Time used:', end-start)

    # run brute force, print out the trip and keep track of the time and print out
    start = time.time()
    bruteforce_list = brute_force_cow_transport(cows)
    print('Number of trip using Brute Force is', len(bruteforce_list))
    end = time.time()
    print('Time used:', end-start)

if __name__ == '__main__':
    cows = load_cows(COW_FILE)
    print(cows)
    # print(greedy_cow_transport(cows))
    # brute_force_cow_transport(cows)
    compare_cow_transport_algorithms()
    # Greedy is faster but not return the optimal solution