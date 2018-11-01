import controllers.direction as d
import random


class GhostsController:
    def __init__(self):
        """Initializes the GhostsController class."""
        self.POSSIBLE_MOVES = [d.Direction.UP, d.Direction.DOWN, d.Direction.LEFT,
            d.Direction.RIGHT]


    def get_move(self, game_state):
        """Produces a move based on game_state.

        Note: for assignment 2a, the move is randomized.
        """
        # Choose a random direction
        return random.choice(self.POSSIBLE_MOVES)

