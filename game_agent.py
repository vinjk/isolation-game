"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)
    
    #Position of the centre of the board
    board_centre = (round(0.5*game.height)-1, round(0.5*game.width)-1); 
    
    #find the current position of the player
    curr_pos = game.get_player_location(player);
    
    #find the position of the opponent
    opp_pos = game.get_player_location(game.get_opponent(player));
    
    #Compute square of distance to board centre for both player and opponent
    dist2c_own = (curr_pos[0]-board_centre[0])**2 + (curr_pos[1]-board_centre[1])**2;
    dist2c_opp = (opp_pos[0]-board_centre[0])**2 + (opp_pos[1]-board_centre[1])**2;
    
    #return difference between the distance to board centre between opponent
    # and player
    return float(dist2c_opp - dist2c_own)
    
    # TODO: finish this function!
    raise NotImplementedError


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)
    
    #Get legal moves of the player and also of the opponent
    own_moves = game.get_legal_moves(player);
    opp_moves = game.get_legal_moves(game.get_opponent(player));
    
    #if opponent has no moves then return +inf
    if not opp_moves:
        return float("inf")
    #return the ratio between number of moves for player and number of moves 
    # for opponent
    return float(len(own_moves)/len(opp_moves))
    
    # TODO: finish this function!
    raise NotImplementedError
    


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)
    
    #weightage for number of legal moves
    w = 0.5;
    
    #get the possible legal moves
    own_moves = game.get_legal_moves(player);
    
    #find the current position of the player
    curr_pos = game.get_player_location(player);
    
    #compute the distance to the centre of the board from the current position
    #closer to the centre, better is the position of the player
    
    board_centre = (round(0.5*game.height)-1, round(0.5*game.width)-1);
    dist2c = (board_centre[0]-curr_pos[0])**2+(board_centre[1]-curr_pos[1])**2
    
    #return score for the current position with weightage w given to the number
    #legal moves available and (1-w) weightage given to the dist2c. If distance
    #to centre is 0, then return max score +inf
    if dist2c == 0:
        return float("inf")
    else:
        return w*len(own_moves)+(1-w)*(1/dist2c);  
    
    # TODO: finish this function!
    raise NotImplementedError


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
    def __init__(self, search_depth=3, score_fn=custom_score_3, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
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

    def minimax(self, game, depth, max_layer=True, flag_entry = False, depth_max = 0):
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
        
        #Get avaiable legal moves
        legal_moves = game.get_legal_moves();
        if not legal_moves: #check if there are no legal moves
            #if not topmost max layer return score else return move (-1,-1)
            if depth != depth_max: 
                return float("-inf")
            else:
                return (-1,-1)
        
        #Store the max depth to identify whether we are at topmost max layer
        #Initialise best move with a random choice from available moves
        if not flag_entry:
            depth_max = depth;
            best_move = random.choice(legal_moves);
            flag_entry = True;
        else:
            best_move = (-1,-1)  
        
        #If at the deepest layer
        if depth == 1:
            if max_layer:
                best_score = float("-inf");
                for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    score_game = self.score(new_game_state, self);
                    if score_game > best_score:
                        best_score, best_move = score_game, move;
            else:
                best_score = float("inf");
                for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    score_game = self.score(new_game_state, self);
                    if score_game < best_score:
                        best_score, best_move = score_game, move;
        #If at other layers
        else:    
            if max_layer:
                best_score = float("-inf");
                for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    score_game = self.minimax(new_game_state, depth-1, False, flag_entry, depth_max);
                    if score_game > best_score:
                        best_score, best_move = score_game, move;
            else:
                best_score = float("inf");
                for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    score_game = self.minimax(new_game_state, depth-1, True, flag_entry, depth_max);
                    if score_game < best_score:
                        best_score, best_move = score_game, move;
        
        #if at the topmost max layer return best_move else return best score
        if depth == depth_max:
            return best_move
        else:
#            print (best_score)
            return best_score
                
        # TODO: finish this function!
        raise NotImplementedError


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
        
        #All possible legal moves
        legal_moves = game.get_legal_moves();
        
        #flag to indicate whether it's player's first move
        first_move_flag = not game.get_player_location(game.active_player);        
        
        if not legal_moves:
            #Return (-1,-1) if no legal moves available
            return (-1,-1)
        else:
            if first_move_flag:
                board_centre = (round(0.5*game.height)-1, round(0.5*game.width)-1);
                if game.move_is_legal(board_centre):
                    #return the centre of the board as next move if available
                    return board_centre
            else:
                best_move = random.choice(legal_moves);               
        
        #Initialise depth as 1 
        depth = 1;
        
        try:
            #Iterative deepening(ID) search
            while(1):
                move = self.alphabeta(game, depth)
                if not move or move == (-1,-1):
                    #Stop search if endgame
                    break
                else:
                    best_move = move;
                #Increment the depth for next round of ID
                depth += 1;
            return best_move                
        except SearchTimeout:            
            return best_move
            
        # TODO: finish this function!
        raise NotImplementedError

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"),\
                  max_layer = True, flag_entry = False, depth_max = 0):
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
        
        max_layer : bool
            Flag to indicate max player or not
        
        flag_entry : bool
            Flag to indicate whether this is call from get_move or part or call
            via recursion
            
        depth_max : int
            maximum search depth. Used to check when to return best_move

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
        
        #Get all available legal moves
        legal_moves = game.get_legal_moves();
        
        #Store the depth if it's the first call from get_move. Also initialise
        # best_move with random choice from legal_moves. For all other recursive
        #call to function initialise best_move with None
        if not flag_entry:
            depth_max = depth;
            best_move = random.choice(legal_moves);
            flag_entry = True;
        else:
            best_move = None
        
        #Return (-1,-1) if no legal moves available if at the topmost max layer
        #else return score (alpha - beta)
        if not legal_moves:
            if depth != depth_max:
                if max_layer:
                    return float("-inf"), float("-inf")
                else:
                    return float("inf"), float("inf")
            else:
                return (-1,-1)
                      
        # Alpha-beta pruning- alternate between min layer and max layer till 
        # depth = 1
        #For deepest layer, depth = 1
        if depth == 1:
            if max_layer:
               for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    alpha_sc, beta_sc = float("-inf"), self.score(new_game_state, self);
                    if alpha_sc >= beta:
                        alpha = alpha_sc;
                        break
                    elif beta_sc > alpha:
                        alpha = beta_sc;
                        best_move = move;
                        if alpha >= beta:
                            break
            else:
                for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    alpha_sc, beta_sc = self.score(new_game_state, self), float("inf");
                    if alpha_sc <= alpha:
                        beta = alpha_sc;
                        break
                    elif alpha_sc < beta:
                        beta = alpha_sc;
                        best_move = move;
                        if beta <= alpha:
                            break
        else:        
            # For all other layers
            if max_layer:
                for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    alpha_sc, beta_sc = self.alphabeta(new_game_state, depth-1,\
                                                       alpha,beta,False, \
                                                       flag_entry, depth_max);
                    if alpha_sc >= beta:
                        alpha = alpha_sc;
                        break
                    elif beta_sc > alpha:
                        alpha = beta_sc;
                        best_move = move;
                        if alpha >= beta:
                            break
            else:
                for move in legal_moves:
                    new_game_state = game.forecast_move(move);
                    alpha_sc, beta_sc = self.alphabeta(new_game_state, depth-1,\
                                                 alpha,beta,True, flag_entry,\
                                                 depth_max);
                    if alpha_sc <= alpha:
                        beta = alpha_sc;
                        break
                    elif alpha_sc < beta:
                        beta = alpha_sc;
                        best_move = move;
                        if beta <= alpha:
                            break
        
        #Return best_move if in first layer (max, where depth = depth_max)
        #else return alpha, beta values
        if depth == depth_max:
            return best_move
        else:
            return alpha, beta                

        # TODO: finish this function!
        raise NotImplementedError
