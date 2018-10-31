class WorldFile:
    def __init__(self, config):
        """Initializes the WorldFile class.

        Where config is a Config object.
        """
        self.config = config
        self.file = open(self.config.settings['world file path'], 'w')


    def write_first_snapshot(self, width, height, pacman, walls, ghosts, pills, remaining_time):
        """Writes the initial snapshot to the world file."""
        self.write_line(width)
        self.write_line(height)

        self.write_triplet('m', pacman.x, pacman.y)

        for c in walls:
            self.write_triplet('w', c.x, c.y)

        for ghost_id in range(len(ghosts)):
            self.write_triplet(ghost_id + 1, ghosts[ghost_id].x, ghosts[ghost_id].y)

        for c in pills:
            self.write_triplet('p', c.x, c.y)

        self.write_triplet('t', remaining_time, 0)

        
    def write_snapshot(self, pacman, ghosts, fruit, remaining_time, score):
        """Writes a non-initial snapshot to the world file."""
        self.write_triplet('m', pacman.x, pacman.y)     

        for ghost_id in range(len(ghosts)):
            self.write_triplet(ghost_id + 1, ghosts[ghost_id].x, ghosts[ghost_id].y)

        for c in fruit:
            self.write_triplet('f', c.x, c.y)

        self.write_triplet('t', remaining_time, score)


    def write_line(self, data):
        """Writes a single line (including newline char) to self.file."""
        self.file.write(str(data) + '\n')

    
    def write_triplet(self, data1, data2, data3):
        """Writes a space delimited, single line (including newline char) 
        containing the given triplet to self.file."""
        self.file.write(str(data1) + ' ' + str(data2) + ' ' + str(data3) + '\n')

