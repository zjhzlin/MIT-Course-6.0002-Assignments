# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Lynn Zhang
# Collaborators (discussion):
# Time: 156min
# 2021-04-06 05:34 - 06:34 60min need to solve: no module name matplotlib
#                          problem 1 done
#            07:06 - 07:28 22min
#            07:40 - 08:00 20min standard robot class done
#                                when testing no module name matplotlib - temporary use python 2.7 as intepreter
#            08:12 - 08:34 22min debugging and test_robot_movement pass and faulty robot done
#                                so fun to see the test_robot_movement! :)
#            08:40 - 09:12 32min run simulation implement and run the simulator
#                                self note: new class - robot can also be put into the list

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        self.dict = {}  # store the tile dirt info into a dictionary
        for i in range(width):
            for j in range(height):
                self.dict[(i,j)] = dirt_amount
        # raise NotImplementedError
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        # get the x, y position of the tile
        tile_pos_x = math.floor(pos.get_x())
        tile_pos_y = math.floor(pos.get_y())
        # check how much dirt is there
        current_dirt = self.get_dirt_amount(tile_pos_x, tile_pos_y)
        # clean the tile
        if capacity >= current_dirt:     # if capacity exceeds, then mark 0
            current_dirt = 0
        else:
            current_dirt = current_dirt - capacity
        # update the dirt amount on that tile
        self.dict[(tile_pos_x, tile_pos_y)] = current_dirt
        # raise NotImplementedError

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        if self.get_dirt_amount(m,n) == 0:
            return True
        else:
            return False
        # raise NotImplementedError

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        num_cleaned_tiles = 0
        m = self.width
        n = self.height
        # check all the tiles one by one
        for i in range(m):
            for j in range(n):
                if self.is_tile_cleaned(i,j):
                    num_cleaned_tiles += 1
        # print(self.dict)
        return num_cleaned_tiles
        # raise NotImplementedError
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        # get the x, y position of the tile
        tile_pos_x = math.floor(pos.get_x())
        tile_pos_y = math.floor(pos.get_y())
        if tile_pos_x <= self.width-1 and tile_pos_y <= self.height-1:
            # print(self.dict)
            return True
        else:
            return False
        # raise NotImplementedError
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.dict[(m, n)]
        # raise NotImplementedError
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError 
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        

# testing RectagularRoom class
# room = RectangularRoom(2,3,3)
# print(room.get_num_cleaned_tiles())
# print(room.get_dirt_amount(1,1))
# p = Position(1.3,1)
# print(room.is_position_in_room(p))
# room.clean_tile_at_position(p,3)
# print(room.get_dirt_amount(1,1))
# print(room.get_num_cleaned_tiles())


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive integer; the amount of dirt cleaned by the robot
                  in a single time-step
        """
        self.room = room
        self.speed = speed
        self.capacity = capacity
        self.position = room.get_random_position()
        self.direction = random.random()*360        # random.randrange(start, stop[, step]) return integer; here requires float
        # raise NotImplementedError

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position
        # raise NotImplementedError

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction
        # raise NotImplementedError

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position
        # raise NotImplementedError

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction
        # raise NotImplementedError

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width * self.height
        # raise NotImplementedError
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        if self.is_position_in_room(pos):
            return True
        else:
            return False
        # raise NotImplementedError
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        x = random.random() * self.width
        y = random.random() * self.height
        return Position(x, y)
        # raise NotImplementedError

class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        # check whether the (m,n) is in furniture_tiles
        if (m, n) in self.furniture_tiles:
            return True
        else:
            return False
        # raise NotImplementedError
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        # find the tile
        m = math.floor(pos.get_x())
        n = math.floor(pos.get_y())
        # check whether the tile is furnished or not
        if self.is_tile_furnished(m, n):
            return True
        else:
            return False
        # raise NotImplementedError
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        if self.is_position_in_room(pos) and not self.is_position_furnished(pos):
            return True
        else:
            return False
        # raise NotImplementedError
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        # total - furnished titles
        total_tiles = self.width * self.height
        furnished_tiles = len(self.furniture_tiles)
        return total_tiles-furnished_tiles
        # raise NotImplementedError

    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        x = random.random() * self.width
        y = random.random() * self.height
        while self.is_position_furnished(Position(x, y)):    # exit condition, (x,y) not in furnished tiles
            x = random.random() * self.width
            y = random.random() * self.height
        return Position(x, y)
        # raise NotImplementedError

# test furnished room
# room = FurnishedRoom(2,3,3)
# print(room.is_position_in_room(Position(1,1)))
# room.add_furniture_to_room()
# print(room.get_num_tiles())
# p=room.get_random_position()
# print(p.get_x(),p.get_y())
# print(room.is_position_furnished(p))

# test empty room
# room = EmptyRoom(2,3,3)
# print(room.is_position_in_room(Position(1,1)))

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        current_position = self.get_robot_position()
        new_position = current_position.get_new_position(self.get_robot_direction(), self.speed)

        # check the new position's validity - need to make sure new_position are all positive values and also is valid
        new_x = new_position.get_x()
        new_y = new_position.get_y()
        # if new position out of the room or not valid position, -> only need to update the direction
        if new_x < 0 or new_y < 0 or not self.room.is_position_valid(new_position):
            new_direction = random.random() * 360
            self.set_robot_direction(new_direction)
        else:
            # if valid, clean the dirt, and update the new position
            # check whether the tile is clean or not, clean if dirty
            if not self.room.is_tile_cleaned(math.floor(new_x), math.floor(new_y)):
                self.room.clean_tile_at_position(new_position, self.capacity)
            self.set_robot_position(new_position)
        # raise NotImplementedError

# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        if self.gets_faulty():
            # if faulty: not clean and update the direction
            new_direction = random.random() * 360
            self.set_robot_direction(new_direction)
        else:
            # not faulty
            current_position = self.get_robot_position()
            new_position = current_position.get_new_position(self.get_robot_direction(), self.speed)

            # check the new position's validity - need to make sure new_position are all positive values and also is valid
            new_x = new_position.get_x()
            new_y = new_position.get_y()
            # if new position out of the room or not valid position, -> only need to update the direction
            if new_x < 0 or new_y < 0 or not self.room.is_position_valid(new_position):
                new_direction = random.random() * 360
                self.set_robot_direction(new_direction)
            else:
                # if valid, clean the dirt, and update the new position
                # check whether the tile is clean or not, clean if dirty
                if not self.room.is_tile_cleaned(math.floor(new_x), math.floor(new_y)):
                    self.room.clean_tile_at_position(new_position, self.capacity)
                self.set_robot_position(new_position)

        # raise NotImplementedError

# test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
# def robot_clean(robot, room):
#     robot.update_position_and_clean()

def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    trial_total_time = 0    #keep track of total time of all the trials
    for trial in range(num_trials):
        # for each trial, room needs to reset
        room = EmptyRoom(width, height, dirt_amount)
        robot_list = []
        for num_r in range(num_robots):
            robot_list.append(robot_type(room, speed, capacity))  # number of robots?
        # keep track of the total time used per trial
        time = 0
        # exit condition: fraction of room is cleaned
        while room.get_num_cleaned_tiles()/room.get_num_tiles() < min_coverage:
            # each robot cleans the room in turn
            for num_r in range(num_robots):
                robot_list[num_r].update_position_and_clean()
            time += 1       # update the time used per trial
        trial_total_time += time       # update the trial total time
    # average trial time
    avg_trial_time = trial_total_time/num_trials
    return avg_trial_time


    # raise NotImplementedError


# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
#  3 robot types using standard robot
#  50%: 5425 vs 1870

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#  - standard robot: 2714
#  - faulty robot: 3284

# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
