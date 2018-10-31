import copy
import gp.log as log_class
import math
import random
import util.seed as seed_class
import world.gpac_world as gpac_world_class


class GPDriver:
    def __init__(self, config):
        """Initializes the GPDriver class.
        
        Where config is a Config object. 
        """
        self.config = config

        self.seed = seed_class.Seed(self.config)

        self.run_count = 1
        self.init_run_variables()

        self.log = log_class.Log(self.config, self.seed, overwrite=True)


    def init_run_variables(self):
        """Initializes run specific variables.

        This function should be called before each run.
        """
        self.eval_count = 0
        self.gpac_world = gpac_world_class.GPacWorld(self.config)


    def decide_termination(self):
        """Returns False if the program will terminate, True otherwise.

        The program will terminate if any of the following conditions are True:
            1. The number of evaluations specified in config has been reached.
            2. The GPac game is over (see check_game_over() in the GPacWorld 
               class for details).
        """
        if self.eval_count >= int(self.config.settings['num fitness evals']):
            # The number of desired evaluations has been reached
            return False

        if self.gpac_world.check_game_over():
            return False

        return True


    def increment_run_count(self):
        """Increments the run count by one."""
        self.run_count += 1
    

    def move_units(self):
        """Moves all units in self.gpac_world in a random direction."""
        self.gpac_world.move_pacman()

        for ghost_id in range(len(self.gpac_world.ghost_coords)):
            self.gpac_world.move_ghost(ghost_id)


    def update_world_state(self):
        """Updates the state of the world *after* all characters have
        moved.
        """
        # Update time remaining
        self.gpac_world.time_remaining -= 1

        # Update pills
        if self.gpac_world.pacman_coord in self.gpac_world.pill_coords:
            self.gpac_world.pill_coords.remove(self.gpac_world.pacman_coord)
            self.gpac_world.num_pills_consumed += 1

        # Update fruit
        if self.gpac_world.pacman_coord in self.gpac_world.fruit_coords:
            self.gpac_world.fruit_coords.remove(self.gpac_world.pacman_coord)
            self.gpac_world.num_fruit_consumed += 1

        # Update score
        self.gpac_world.update_score()

        # Write to world file
        self.gpac_world.world_file.write_snapshot(self.gpac_world.pacman_coord,
            self.gpac_world.ghost_coords, self.gpac_world.fruit_coords, 
            self.gpac_world.time_remaining, self.gpac_world.score)
    
