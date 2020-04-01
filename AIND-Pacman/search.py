# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def get_path(self):
        "Create a list of nodes from the root to this node."
        if not self.action:
            x, result = self, []
        else:
            x, result = self, [self.action]
        while x.parent and x.parent.action:
            result.append(x.parent.action)
            x = x.parent
        return list(reversed(result))

    def expand(self, problem):
        "Return a list of nodes reachable from this node. [Fig. 3.8]"
        return [Node(next, self, act,
                     self.path_cost + problem.getCostOfActions(self.get_path))
                for (act, next) in problem.getSuccessors(self.state)]


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def __init__(self):
        pass

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from util import Stack

    root = problem.getStartState()

    frontier = Stack()
    frontier.push((root, []))
    explored = set()
    while not frontier.isEmpty():
        node, path = frontier.pop()

        if problem.isGoalState(node):
            return path

        if node not in explored:
            explored.add(node)
            for state, action, cost in problem.getSuccessors(node):
                if state not in explored:
                    frontier.push((state, path + [action]))

    return []


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    root_state = problem.getStartState()

    frontier = util.Queue()
    frontier.push((root_state, []))
    explored = set()

    while not frontier.isEmpty():
        node, path = frontier.pop()

        if problem.isGoalState(node):
            return path

        if node not in explored:
            explored.add(node)
            # Children of current node
            for child_node, action, cost in problem.getSuccessors(node):
                if child_node not in explored:
                    frontier.push((child_node, path + [action]))
    return []


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    from util import PriorityQueueWithFunction
    root_node = Node(problem.getStartState())

    frontier = PriorityQueueWithFunction(lambda n, p: n.path_cost)
    frontier.push(root_node, problem)
    explored = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        path = node.get_path()

        if problem.isGoalState(node.state):
            return path

        if node.state not in explored:
            explored.add(node.state)
            # Children of current node
            for child_state, action, cost in problem.getSuccessors(node.state):
                if child_state not in explored:
                    new_node = Node(child_state, parent=node, action=action, path_cost=node.path_cost + cost)
                    frontier.push(new_node, problem)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    from util import PriorityQueueWithFunction
    root_node = Node(problem.getStartState())

    frontier = PriorityQueueWithFunction(lambda n, p: n.path_cost + heuristic(n.state, p))
    frontier.push(root_node, problem)
    explored = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        path = node.get_path()

        if problem.isGoalState(node.state):
            print 'path length was ',len(path)
            return path

        if node.state not in explored:
            explored.add(node.state)
            # Children of current node
            for child_state, action, cost in problem.getSuccessors(node.state):
                if child_state not in explored:
                    new_node = Node(child_state, parent=node, action=action, path_cost=node.path_cost + cost)
                    frontier.push(new_node, problem)
    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
