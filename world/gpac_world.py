from enum import Enum
import copy
import random
import world.coordinate as coord_class
import world.world_file as world_file_class


class Direction(Enum):
    NONE  = 0  # Applicable to pacman only
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4
    RAND  = 5  # A random direction should be chosen


# Define movement possibilities using Direction class
POSSIBLE_PACMAN_MOVES = [Direction.NONE, Direction.UP, Direction.DOWN,
    Direction.LEFT, Direction.RIGHT]

POSSIBLE_GHOST_MOVES = [Direction.UP, Direction.DOWN, Direction.LEFT,
    Direction.RIGHT]


class GPacWorld:
    def __init__(self, config):
        """Initializes the GPacWorld class.
        
        Where config is a Config object for the GPac problem.
        """
        self.config = config

        # Load configuration file settings
        self.width = int(self.config.settings['width'])
        self.height = int(self.config.settings['height'])
        self.pill_density = float(self.config.settings['pill density'])
        self.wall_density = float(self.config.settings['wall density'])
        self.num_ghosts = int(self.config.settings['num ghosts'])
        self.fruit_spawn_prob = float(self.config.settings['fruit spawn prob'])
        self.fruit_score = int(self.config.settings['fruit score'])
        self.time_multiplier = float(self.config.settings['time multiplier'])

        # Create initial world attributes
        self.pacman_coord = coord_class.Coordinate(0, self.height - 1)
        self.prev_pacman_coord = self.pacman_coord
        self.ghost_coords = [coord_class.Coordinate(self.width - 1, 0) for _ in range(self.num_ghosts)]
        self.prev_ghost_coords = copy.deepcopy(self.ghost_coords)
        self.wall_coords = set([])
        self.pill_coords = set([])
        self.fruit_coords = set([])
        self.time_remaining = self.time_multiplier * self.width * self.height
        self.total_time = self.time_remaining
        self.num_pills_consumed = 0
        self.num_fruit_consumed = 0
        self.score = 0
        
        # Create helper set of all coordinates
        self.all_coords = set([])

        for x in range(self.width):
            for y in range(self.height):
                self.all_coords.add(coord_class.Coordinate(x, y))

        # Place walls and pills in the world
        self.generate_world()

        # Create & write to world file
        self.world_file = world_file_class.WorldFile(self.config)
        self.world_file.save_first_snapshot(self.width, self.height, self.pacman_coord,
            self.wall_coords, self.ghost_coords, self.pill_coords, self.time_remaining)


    def generate_world(self):
        """Randomly generates a GPac world (in place) by placing walls and pills
        with densities found in self.config.
        """

        def add_wall(coord):
            """Attempts to add a wall to the world at coord.

            A wall placement is unsuccessful if it blocks a portion of the world
            from being reachable from any arbitrary coordinate in the world.

            Reachability is guaranteed by finding a path from pacman's beginning cell 
            to every cell in the world.

            Returns True if successful, False otherwise.
            """

            def all_cells_reachable(wall_coords):
                """Returns True if there is a path from pacman's starting cell
                to every other non-wall cell. Returns False otherwise.
                """
                
                def find_path_recursive(coord):
                    """Recursively attempts to 'travel' to all non-wall coordinates 
                    (denoted by wall_coords) and returns True if possible, 
                    False otherwise.
                    """
                    coords_to_find.remove(coord)

                    if not len(coords_to_find):
                        # All coordinates have been reached
                        return True 

                    # There are still coordinates to reach
                    # Explore all adjacent coordinates that have not already been found
                    for c in [adj_coord for adj_coord in self.get_adj_coords(coord) if not adj_coord in wall_coords]:
                        if c in coords_to_find:
                            if find_path_recursive(c):
                                return True

                    return False


                # Construct a set of coordinates to find
                coords_to_find = set([])

                for c in self.all_coords:
                    if not c in wall_coords:
                        coords_to_find.add(c)

                starting_coord = coord_class.Coordinate(0, self.height - 1)

                return find_path_recursive(starting_coord)


            if self.can_move_to(coord) and all_cells_reachable(self.wall_coords.union(set([coord]))):
                self.wall_coords.add(coord)
                return True

            return False
                

        # Select coordinates to be walls
        wall_coords_to_add = []
        
        for c in self.all_coords.difference(set([self.pacman_coord])).difference(set([self.ghost_coords[0]])):
            if random.random() < self.wall_density:
                wall_coords_to_add.append(coord_class.Coordinate(c.x, c.y))

        # Add walls to the world
        # Note that adding walls after finding all wall candidates avoids issues with
        # pathfinding checks and iterating through self.all_coords
        for c in wall_coords_to_add:
            add_wall(c)

        # Add pills to the world
        for c in self.all_coords.difference(set([self.pacman_coord])).difference(self.wall_coords):
            if random.random() < self.pill_density:
                self.pill_coords.add(c)


    def move_pacman(self, direction=Direction.RAND):
        """Attempts to move pacman in the given direction.

        Returns True if the move is successful, False otherwise.
        """
        if direction == Direction.RAND:
            # Choose a random direction
            direction = random.choice(POSSIBLE_PACMAN_MOVES)

        if direction == Direction.NONE:
            # No action needed
            return True

        new_coord = copy.deepcopy(self.pacman_coord)
        
        # Adjust new_coord depending on pacman's desired direction
        if direction == Direction.UP:
            new_coord.y += 1

        elif direction == Direction.DOWN:
            new_coord.y -= 1

        elif direction == Direction.LEFT:
            new_coord.x -= 1

        elif direction == Direction.RIGHT:
            new_coord.x += 1
        
        if self.can_move_to(new_coord):
            self.prev_pacman_coord = copy.deepcopy(self.pacman_coord)
            self.pacman_coord = copy.deepcopy(new_coord)
            return True

        return False


    def move_ghost(self, ghost_id, direction=Direction.RAND):
        """Attempts to move ghost with ghost_id (index for self.ghost_coords) 
        in the given direction.

        Returns True if the move is successful, False otherwise.
        """
        if ghost_id >= len(self.ghost_coords):
            # This ghost does not exist
            return False

        if direction == Direction.RAND:
            # Choose a random direction
            direction = random.choice(POSSIBLE_GHOST_MOVES)

        new_coord = copy.deepcopy(self.ghost_coords[ghost_id])
        
        # Adjust new_coord depending on pacman's desired direction
        if direction == Direction.UP:
            new_coord.y += 1

        elif direction == Direction.DOWN:
            new_coord.y -= 1

        elif direction == Direction.LEFT:
            new_coord.x -= 1

        elif direction == Direction.RIGHT:
            new_coord.x += 1
        
        if self.can_move_to(new_coord):
            self.prev_ghost_coords[ghost_id] = copy.deepcopy(self.ghost_coords[ghost_id])
            self.ghost_coords[ghost_id] = copy.deepcopy(new_coord)
            return True

        return False


    def check_game_over(self):
        """Returns True if the game is over, False otherwise.

        The game is over if any of the following is true:
            1. pacman and a ghost are in the same cell
            2. pacman collided with a ghost
            3. all pills are gone
            4. time remaining is equal to zero
        """
        if self.pacman_coord in self.ghost_coords:
            return True

        if self.prev_pacman_coord in self.prev_ghost_coords:
            return True

        if not len(self.pill_coords):
            return True

        if not self.time_remaining:
            return True

        return False # The game continues


    def can_move_to(self, coord):
        """Returns True if coord can be moved to (either by ghosts or by pacman),
        and False otherwise.

        A movable coordinate is one that does not contain a wall and that is in the world.
        """
        return not coord in self.wall_coords and coord.x >= 0 and coord.y >= 0 and coord.x < self.width and coord.y < self.height


    def visualize(self):
        """Prints the world and its contents to the screen."""
        
        class GPacChars(Enum):
            EMPTY  = '_'
            PACMAN = 'P'
            GHOST  = 'G'
            WALL   = 'X'
            PILL   = 'p'
            FRUIT  = 'F'

        world = [[GPacChars.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        
        world[self.pacman_coord.x][self.pacman_coord.y] = GPacChars.PACMAN
        
        for c in self.ghost_coords:
            world[c.x][c.y] = GPacChars.GHOST

        for c in self.wall_coords:
            world[c.x][c.y] = GPacChars.WALL

        for c in self.pill_coords:
            world[c.x][c.y] = GPacChars.PILL

        for c in self.fruit_coords:
            world[c.x][c.y] = GPacChars.FRUIT

        # Flip each row in the world matrix for correct printing 
        # TODO: re-evaluate this
        for row_index in range(len(world)):
            world[row_index] = world[row_index][::-1]

        for row in range(self.width):
            for col in range(self.height):
                print(world[row][col].value, end=' ')

            print('\n')

        print('\n')

    
    def get_adj_coords(self, coord):
        """Returns a list of coordinates adjacent to coord.

        Where the returned coordinate list includes only valid coordinates.
        """
        adj_coords = []

        if not coord.x == 0:
            adj_coords.append(coord_class.Coordinate(coord.x - 1, coord.y))

        if not coord.x == self.width - 1:
            adj_coords.append(coord_class.Coordinate(coord.x + 1, coord.y))
        
        if not coord.y == 0:
            adj_coords.append(coord_class.Coordinate(coord.x, coord.y - 1))
        
        if not coord.y == self.height - 1:
            adj_coords.append(coord_class.Coordinate(coord.x, coord.y + 1))
        
        return adj_coords


    def update_score(self):
        self.score = int((self.num_pills_consumed / (self.num_pills_consumed + len(self.pill_coords))) * 100) + (self.num_fruit_consumed * self.fruit_score)

        if not len(self.pill_coords):
            # No more pills in the world
            self.score += self.time_remaining // self.total_time
        
