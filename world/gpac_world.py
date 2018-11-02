import controllers.direction as d
import copy
import gp.world_file as world_file_class
import random
import world.coordinate as coord_class
import world.gpac_chars as chars
import world.wall_carver as wall_carver_class


class GPacWorld:
    def __init__(self, config, initial_instance=False):
        """Initializes the GPacWorld class.
        
        Where config is a Config object for the GPac problem and initial_instance
        determines if a random world should be generated yet.
        """
        self.config = config

        # Load configuration file settings
        self.width = int(self.config.settings['width'])
        self.height = int(self.config.settings['height'])
        self.pill_density = float(self.config.settings['pill density']) / 100
        self.wall_density = float(self.config.settings['wall density']) / 100
        self.num_ghosts = int(self.config.settings['num ghosts'])
        self.fruit_spawn_prob = float(self.config.settings['fruit spawn prob'])
        self.fruit_score = int(self.config.settings['fruit score'])
        self.time_multiplier = int(self.config.settings['time multiplier'])

        # Create initial world attributes
        self.pacman_coord = coord_class.Coordinate(0, self.height - 1)
        self.prev_pacman_coord = self.pacman_coord
        self.ghost_coords = [coord_class.Coordinate(self.width - 1, 0) for _ in range(self.num_ghosts)]
        self.prev_ghost_coords = copy.deepcopy(self.ghost_coords)
        self.wall_coords = set([])
        self.pill_coords = set([])
        self.fruit_coord = set([])
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
        # Only do this if the world is not being created for the first time
        # Subsequent runs of the GP will ensure random board generation
        if not initial_instance:
            self.generate_world()

        # Create & write to world file
        self.world_file = world_file_class.WorldFile(self.config)
        self.world_file.save_first_snapshot(self.width, self.height, self.pacman_coord,
            self.wall_coords, self.ghost_coords, self.pill_coords, self.time_remaining)


    def generate_world(self):
        """Randomly generates a GPac world (in place) by placing walls and pills
        with densities found in self.config.
        """

        def add_walls():
            """Places (carves out) walls in the world such that every non-wall cell is 
            accessible from every other non-wall cell.
            """

            def assign_unit_starting_coords(wall_carver_list):
                """Assigns the first two WallCarvers in wall_carver_list to have 
                the unit (pacman & ghosts) starting coords, ensuring these
                coords are carved out.
                """
                wall_carver_list[0].coord = self.pacman_coord
                wall_carver_list[1].coord = self.ghost_coords[0]


            # Create WallCarver population
            # Note: num wall carvers should be greater than or equal to two
            wall_carvers = [wall_carver_class.WallCarver(random.randint(0, self.width), random.randint(0, self.height), self.config) for _ in range(int(self.config.settings['num wall carvers']))]
            assign_unit_starting_coords(wall_carvers)

            # Get walls to carve
            walls_to_carve = copy.deepcopy(self.all_coords)

            # Calculate wall density
            num_coords = len(walls_to_carve)
            num_walls = num_coords
            wall_density = num_walls / num_coords

            while wall_density > self.wall_density:
                if len(wall_carvers) <= 1:
                    # Re-spawn WallCarvers
                    wall_carvers = [wall_carver_class.WallCarver(random.randint(0, self.width), random.randint(0, self.height), self.config) for _ in range(int(self.config.settings['num wall carvers']))]

                for wall_carver in wall_carvers:
                    if wall_carver.coord_already_carved(wall_carvers):
                        # This coord has already been seen by another WallCarver
                        wall_carver.mark_for_death()

                    elif wall_carver.coord in walls_to_carve:
                        # This is a new coord. Remove the wall
                        walls_to_carve.remove(wall_carver.coord)
                        wall_carver.seen_coords.add(wall_carver.coord)
                        num_walls -= 1

                    wall_carver.move()

                # Kill WallCarvers marked for death
                wall_carvers = [wall_carver for wall_carver in wall_carvers if not wall_carver.marked_for_death]

                wall_density = num_walls / num_coords

            self.wall_coords = walls_to_carve


        # Add walls to the world
        add_walls()

        # Add pills to the world
        for c in self.all_coords.difference(set([self.pacman_coord])).difference(self.wall_coords):
            if random.random() < self.pill_density:
                self.pill_coords.add(c)

        # Ensure at least one pill was placed
        if not len(self.pill_coords):
            for c in self.all_coords.difference(set([self.pacman_coord])).difference(self.wall_coords):
                self.pill_coords.add(c)
                break


    def move_pacman(self, direction):
        """Attempts to move pacman in the given direction.

        Returns True if the move is successful, False otherwise.
        """
        if direction == d.Direction.NONE:
            # No action needed
            return True

        new_coord = copy.deepcopy(self.pacman_coord)
        
        # Adjust new_coord depending on pacman's desired direction
        if direction == d.Direction.UP:
            new_coord.y += 1

        elif direction == d.Direction.DOWN:
            new_coord.y -= 1

        elif direction == d.Direction.LEFT:
            new_coord.x -= 1

        elif direction == d.Direction.RIGHT:
            new_coord.x += 1
        
        if self.can_move_to(new_coord):
            self.prev_pacman_coord = copy.deepcopy(self.pacman_coord)
            self.pacman_coord = copy.deepcopy(new_coord)
            return True

        return False


    def move_ghost(self, ghost_id, direction):
        """Attempts to move ghost with ghost_id (index for self.ghost_coords) 
        in the given direction.

        Returns True if the move is successful, False otherwise.
        """
        if ghost_id >= len(self.ghost_coords):
            # This ghost does not exist
            return False

        new_coord = copy.deepcopy(self.ghost_coords[ghost_id])
        
        # Adjust new_coord depending on pacman's desired direction
        if direction == d.Direction.UP:
            new_coord.y += 1

        elif direction == d.Direction.DOWN:
            new_coord.y -= 1

        elif direction == d.Direction.LEFT:
            new_coord.x -= 1

        elif direction == d.Direction.RIGHT:
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


    def visualize(self, wall_coords=None):
        """Prints the world and its contents to the screen, with an option
        to pass in alternate wall coordinates.
        """
        

        if not wall_coords:
            wall_coords = self.wall_coords

        world = [[chars.GPacChars.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        
        for c in self.pill_coords:
            world[c.x][c.y] = chars.GPacChars.PILL

        for c in self.fruit_coord:
            world[c.x][c.y] = chars.GPacChars.FRUIT

        for c in self.ghost_coords:
            world[c.x][c.y] = chars.GPacChars.GHOST

        for c in wall_coords:
            world[c.x][c.y] = chars.GPacChars.WALL

        world[self.pacman_coord.x][self.pacman_coord.y] = chars.GPacChars.PACMAN

        for row in range(self.width):
            for col in range(self.height - 1, -1, -1):
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
        

    def randomly_spawn_fruit(self):
        """Probabilistically spawns a fruit in the world.

        Note that if a fruit already exists, another cannot be spawned.

        A fruit can only spawn in cell that is not occupied by pacman, not
        occupied by a wall, and not occupied by a pill.
        """
        if len(self.fruit_coord):
            # A fruit already exists
            return

        if random.random() <= self.fruit_spawn_prob:
            possible_coords = copy.deepcopy(list(self.all_coords.difference(set([self.pacman_coord])).difference(self.wall_coords).difference(self.pill_coords)))
            random.shuffle(possible_coords)

            for possible_fruit_coord in possible_coords:
                self.fruit_coord.add(possible_fruit_coord)
                break

