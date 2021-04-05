# 6.0002 Problem Set 5
# Graph optimization
# Name: Lynn Zhang
# Collaborators:
# Time: 399min
# 2021-04-03 09:55 - 10:17 22min problem 2b & 2c
#            10:30 - 11:30 60min problem 3 stuck in completing the function, graph thinking
#            13:33 - 14:30 57min debugging path - embedded list - list is mutable! need to use copy
#                          the path in the recursive need to pass the empty one
#                          still not that clear.
# 2021-04-04 60min stuck in the get the best path function
# 2021-04-05 06:00 - 09:00 180min debugging line by line
#        finally solved! - list is mutable. when updating the path, need to pay attention
#         wrong: path[0] += [start]           vs    correct: path[0] = path[0] + [start]
#           += doesn't create a new list;            + create a new list
#             09:30 - 09:50 20min

# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# Each node represent each building in the MIT. And its name is the number in the 1st/2nd position in each line
# Edge represent the direct access relationship between two buildings - 1st & 2nd -> edge
# 3rd and 4th represents the total distance and weighted distance between two buildings.

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    #
    MITDigraph = Digraph()

    print("Loading map from file...")
    f = open(map_filename, 'r')
    for line in f:
        # split each line into 4 elements and assign a variable
        entry = line.split()
        src = Node(entry[0])
        dest = Node(entry[1])
        total_distance = int(entry[2])
        weighted_distance = int(entry[3])
        # edge = Edge(src, dest)
        weighted_edge = WeightedEdge(src, dest, total_distance, weighted_distance)
        if not MITDigraph.has_node(src):
            MITDigraph.add_node(src)
        if not MITDigraph.has_node(dest):
            MITDigraph.add_node(dest)
        # if not MITDigraph.has_edge(weighted_edge):
        MITDigraph.add_edge(weighted_edge)
    f.close()
    return MITDigraph

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# TEST_FILENAME = 'test_load_map.txt'
TEST_FILENAME = 'mit_map.txt'
testdigraph = load_map(TEST_FILENAME)
print(testdigraph)

#
# Problem 3: Finding the Shortest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# minimize distance from a to b; constraints: outdoor distance < limit

# # Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    path[0] = path[0] + [start]     #!!!!!!!!! not the same thing: path[0] += [start]  += doesn't create a new list; + create a new list
    if path[2] > max_dist_outdoors:  # checking if current dist outdoor exceeds the max limit
        return None
    start_node = Node(start)
    end_node = Node(end)
    # if start and end node is not valid nodes, raise error
    if not (digraph.has_node(start_node) and digraph.has_node(end_node)):
        raise ValueError('Start or End node is invalid')
    # elif start and end are the same node, update the global variables?
    elif start_node == end_node:
        return path[0], path[1]
    # else
    # for all the children nodes of start
    for child_edge in digraph.edges[start_node]:
        child_node = child_edge.get_destination()
        child = child_node.get_name()
        distance = path[1] + child_edge.get_total_distance()
        outdoors = path[2] + child_edge.get_outdoor_distance()
        if child not in path[0]:  # avoid loop
            # construct the path including that node
            updated_path = [path[0], distance, outdoors]
            # if this path is longer than the best path, then no need to explore further
            # also if outdoor distance is bigger than max, no need to explore further
            if best_path == None or child_edge.get_total_distance() <= best_dist \
                    and distance <= best_dist:
                # recursively solve the rest of the path, from child to dest
                new_best_path = get_best_path(digraph, child, end, updated_path,
                                              max_dist_outdoors, best_dist, best_path)
                if new_best_path:
                    if not best_dist or new_best_path[1] <= best_dist:  # if distance on current path shorter than best one,
                #     print('Update the best path')
                        best_path = new_best_path[0]
                        best_dist = new_best_path[1]
                        print('Best path is', best_path, 'Distance is', best_dist)
        else:
            print('Already visited')

    # return the shortest path
    return best_path, best_dist

# for test
# print(get_best_path(testdigraph, 'a', 'e', [[],0,0], 100000, 100000, []))

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors)
    # initialzing variables
    path = [[],0,0]
    best_dist = max_total_dist
    best_path = []
    best_path_found = get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path)
    if best_path_found[0] == []:
        raise ValueError('No best path found')
    return best_path_found[0]

# print(directed_dfs(testdigraph, '10','32',100,99999))

# ================================================================∂
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    # pass
    unittest.main()
