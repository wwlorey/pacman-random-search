class GameState:
    def __init__(self, pacman_coord, ghost_coords, pill_coords):
        """Initializes the GameState class."""
        self.update(pacman_coord, ghost_coords, pill_coords)

    def update(self, pacman_coord, ghost_coords, pill_coords):
        """Updates the GameState class."""
        self.pacman_coord = pacman_coord
        self.ghost_coords = ghost_coords
        self.pill_coords = pill_coords

