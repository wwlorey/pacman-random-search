from enum import Enum


class CellContents(Enum):
    """Enumerates the possible contents of a cell."""
    EMPTY  = 0
    WALL   = 1
    PILL   = 2
    FRUIT  = 3
    PACMAN = 4
    GHOST  = 5
    

class Cell:
    def __init__(self, contents=CellContents.EMPTY, pacman_start=False, ghost_start=False):
        """Initializes the Cell class."""
        self.contents = contents
        self.is_starting_cell = pacman_start or ghost_start


    def is_wall(self):
        """Returns True is this cell contains a wall, False otherwise."""
        return self.contents == CellContents.WALL


    def is_empty(self):
        """Returns True if this cell is empty, False otherwise."""
        return self.contents == CellContents.EMPTY


    def has_pill(self):
        """Returns True if this cell is pill, False otherwise."""
        return self.contents == CellContents.PILL


    def is_fruit(self):
        """Returns True if this cell is empty, False otherwise."""
        return self.contents == CellContents.EMPTY



    
    def put_wall(self):
        """Attempts to place a wall on this cell.

        Returns True if successful, False otherwise.
        """
        if self.contents == CellContents.EMPTY:
            self.contents = CellContents.WALL
            return True

        return False
    

    def put_pill
