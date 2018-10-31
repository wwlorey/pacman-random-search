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

        self.global_best_score = -1


    def init_run_variables(self):
        """Initializes run specific variables.

        This function should be called before each run.
        """
        self.eval_count = 0
        self.local_best_score = -1
        self.gpac_world = gpac_world_class.GPacWorld(self.config)


    def move_units(self):
        """Moves all units in self.gpac_world in a random direction.
        
        This function implements the random controllers for each unit.

        Before units are moved, a fruit probabilistically spawns.
        """
        self.gpac_world.randomly_spawn_fruit()

        self.gpac_world.move_pacman()

        for ghost_id in range(len(self.gpac_world.ghost_coords)):
            self.gpac_world.move_ghost(ghost_id)


    def update_world_state(self):
        """Updates the state of the world *after* all characters have moved."""
        # Update time remaining
        self.gpac_world.time_remaining -= 1

        # Update pills
        if self.gpac_world.pacman_coord in self.gpac_world.pill_coords:
            self.gpac_world.pill_coords.remove(self.gpac_world.pacman_coord)
            self.gpac_world.num_pills_consumed += 1

        # Update fruit
        if self.gpac_world.pacman_coord in self.gpac_world.fruit_coord:
            self.gpac_world.fruit_coord.remove(self.gpac_world.pacman_coord)
            self.gpac_world.num_fruit_consumed += 1

        # Update score
        self.gpac_world.update_score()

        # Update the world state
        self.gpac_world.world_file.save_snapshot(self.gpac_world.pacman_coord,
            self.gpac_world.ghost_coords, self.gpac_world.fruit_coord, 
            self.gpac_world.time_remaining, self.gpac_world.score)

        # Increment evaluation count
        self.eval_count += 1
        
        # Determine if a new local best score (fitness) has been found
        if self.gpac_world.score > self.local_best_score:
            self.local_best_score = self.gpac_world.score

            # Write log file row
            self.log.write_run_data(self.eval_count, self.local_best_score)
    

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


    def check_update_world_file(self):
        """Writes a transcript of this run to the world file iff it had the 
        global best score."""
        if self.gpac_world.score > self.global_best_score:
            self.global_best_score = self.gpac_world.score

            # Write to world file
            self.gpac_world.world_file.write_to_file()


    def increment_run_count(self):
        """Increments the run count by one."""
        self.run_count += 1

