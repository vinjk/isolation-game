"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

from game_agent import (AlphaBetaPlayer, MinimaxPlayer, custom_score, custom_score_3, custom_score_2)
from sample_players import (improved_score, center_score)

from importlib import reload


#class IsolationTest(unittest.TestCase):
#    """Unit tests for isolation agents"""
#
#    def setUp(self):
#        reload(game_agent)
#        self.player1 = sample_players.GreedyPlayer
#        self.player2 = game_agent.AlphaBetaPlayer
#        self.game = isolation.Board(self.player1, self.player2)
#        game_agent.IsolationPlayer.__init__(3,game_agent.custom_score,10);


if __name__ == "__main__":
    from isolation import Board
    
#    reload(game_agent)
    player1_win = 0;
    player2_win = 0;
    # create an isolation board (by default 7x7)
    while(player1_win+player2_win)<1:
        player2 = AlphaBetaPlayer(score_fn = improved_score);
        player1 = MinimaxPlayer(score_fn = improved_score);
        game = Board(player1, player2);
    
        # place player 1 on the board at row 3, column 3, then place player 2 on
        # the board at row 0, column 5; display the resulting board state.  Note
        # that the .apply_move() method changes the calling object in-place.
        game.apply_move((3, 3))
#        game.apply_move((2, 3))
    #    print(game.to_string())
    
        # players take turns moving on the board, so player1 should be next to move
    #    assert(player1 == game.active_player)
    
        # get a list of the legal moves available to the active player
    #    print(game.get_legal_moves())
    #
    #    # get a successor of the current state by making a copy of the board and
    #    # applying a move. Notice that this does NOT change the calling object
    #    # (unlike .apply_move()).
    #    new_game = game.forecast_move((1, 1))
    #    assert(new_game.to_string() != game.to_string())
    #    print("\nOld state:\n{}".format(game.to_string()))
    #    print("\nNew state:\n{}".format(new_game.to_string()))
    
        # play the remainder of the game automatically -- outcome can be "illegal
        # move", "timeout", or "forfeit"
        winner, history, outcome = game.play()
        
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))
        if winner == player1:
            print('Player 1 is the winner')
            player1_win += 1;
        else:
            print('Player 2 is the winner')
            player2_win += 1;
    print('player1 win % = ')
    print(player1_win/(player1_win+player2_win))
    print('player2 win % = ')
    print(player2_win/(player1_win+player2_win))
