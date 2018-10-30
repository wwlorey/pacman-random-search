import copy
import gp.log as log_class
import math
import random
import util.seed as seed_class


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


    def evaluate(self, log_run=True):
        """Evaluates all members of the population, updating their fitness values, the average 
        fitness value, and the best fitness seen so far.

        If log_run is True, the state of the experiment is written to the log file.
        """ 
        # TODO: Implement

        if log_run:
            self.log.write_run_data(self.eval_count, self.highest_score)


    def decide_termination(self):
        """Returns False if the program will terminate, True otherwise.

        The program will terminate if any of the following conditions are True:
            1. The number of evaluations specified in config has been reached.
        """
        if self.eval_count >= int(self.config.settings['num fitness evals']):
            # The number of desired evaluations has been reached
            return False

        return True


    def increment_run_count(self):
        """Increments the run count by one."""
        self.run_count += 1
    
