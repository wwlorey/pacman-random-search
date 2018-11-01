import controllers.direction as d
import random


class PacmanController:
    def __init__(self):
        """Initializes the PacmanController class."""
        self.POSSIBLE_MOVES = [d.Direction.NONE, d.Direction.UP, d.Direction.DOWN, 
            d.Direction.LEFT, d.Direction.RIGHT]
    

    def get_move(self, game_state):
        """Produces a move based on game_state.

        Note: for assignment 2a, the move is randomized.
        """
        # Choose a random direction
        return random.choice(self.POSSIBLE_MOVES)

