"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score_2(game, player):
    """
    Calculate the number of open spaces around the player in a 2
    block wide canvas.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_y, own_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))
    blank_spaces = game.get_blank_spaces()

    own_canvas_count = 0
    opp_canvas_count = 0
    for bx, by in blank_spaces:
        if (abs(bx - own_x) == 2 and abs(by - own_y) <= 2) or (
                        abs(by - own_y) == 2 and abs(bx - own_x) <= 2):
            own_canvas_count += 1

        if (abs(bx - opp_x) == 2 and abs(by - opp_y) <= 2) or (
                        abs(by - opp_y) == 2 and abs(bx - opp_x) <= 2):
            opp_canvas_count += 1

    return float(own_canvas_count - opp_canvas_count)


def custom_score_3(game, player):
    """
    Calculate how far each player is from the center of the board.
    The closer to the center, the higher the probability of success,
    because being along the edges means less possibly moves.

    Use Manhattan distance (distance along grid lines) instead of euclidean
    distance.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Center position of board
    center_x, center_y = (game.width / 2), (game.height / 2)

    # Opponent x and y coordinates
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))

    opp_distance = abs(opp_x - center_x) + abs(opp_y - center_y)

    # Player x and y coordinates
    own_y, own_x = game.get_player_location(player)

    own_distance = abs(own_x - center_x) + abs(own_y - center_y)

    return float(opp_distance - own_distance)


def custom_score(game, player):
    """
    Minimize the portion of available moves that fall along the edges of the game board

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # moves available to player and opponent
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # losing branch
    if not own_moves:
        return float("-inf")

    # winning branch
    if not opp_moves:
        return float("inf")

    # Count moves along edges of board for player and opponent
    own_moves_edges = [move for move in own_moves if
                       move[0] == 0 or move[0] == game.width or move[1] == 0 or move[1] == game.height]
    opp_moves_edges = [move for move in opp_moves if
                       move[0] == 0 or move[0] == game.width or move[1] == 0 or move[1] == game.height]

    # Minimize the ratio of edge moves for the player and maximize for the opponent
    return len(opp_moves_edges) / len(opp_moves) - len(own_moves_edges) / len(own_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """
    Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float('-inf')
        best_move = None

        i = 0
        for move in game.get_legal_moves():
            move_score = self.min_value(game.forecast_move(move), depth)
            if move_score > best_score:
                best_move = move
                best_score = move_score
            i += 1

        return best_move

    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # If terminal state or search depth has been reached
        if self.terminal_test(game) or depth <= 0:
            return 1

        depth -= 1
        if depth <= 0:
            return self.score(game, self)

        v = float('inf')
        for move in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(move), depth))
        return v

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(game):
            return -1

        depth -= 1
        if depth <= 0:
            return self.score(game, self)

        v = float('-inf')
        for move in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(move), depth))

        return v

    def terminal_test(self, game):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not bool(game.get_legal_moves())


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float('-inf')
        best_move = None

        for move in game.get_legal_moves():
            move_score = self.min_value(game.forecast_move(move), depth, alpha, beta)
            # Update alpha between nodes, because we start with the min player
            if (move_score > alpha):
                alpha = move_score
            alpha = max(alpha, move_score)
            # Update the best move
            if move_score > best_score:
                best_move = move
                best_score = move_score

        return best_move

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # If we reached a terminal state (no more valid moves for MAX player)
        # return -1 indicating a branch that terminates in a loss for MAX (win for MIN)
        if self.terminal_test(game):
            return -1

        # Decrement current search depth and do check
        # If search depth is reached, evaluate the score of this level
        # and propagate that upwards
        depth -= 1
        if depth <= 0:
            return self.score(game, self)

        v = float('-inf')
        for move in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(move), depth, alpha, beta))
            if v >= beta:
                break
            alpha = max(alpha, v)

        return v

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # If we reached a terminal state (no more valid moves for MIN player)
        # return +1 indicating a branch that terminates in a loss for MIN (win for MAX)
        if self.terminal_test(game) or depth <= 0:
            return 1

        # Decrement current search depth and do check
        # If search depth is reached, evaluate the score of this level
        # and propagate that upwards
        depth -= 1
        if depth <= 0:
            return self.score(game, self)

        v = float('inf')
        for move in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(move), depth, alpha, beta))
            if v <= alpha:
                break
            beta = min(beta, v)
        return v

    def terminal_test(self, game):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not bool(game.get_legal_moves())
