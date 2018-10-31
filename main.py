#!/usr/bin/env python3

import gp.gp_driver as gp_driver_class
import util.args as args_class
import util.config as config_class

if __name__ == '__main__':

    # Process command line arguments
    args = args_class.Arguments(1, ['config/default.cfg'])
    config_file = args.get_args()[0]


    # Setup configuration
    config = config_class.Config(config_file)


    # Initialize the GP driver and its run variables
    gp_driver = gp_driver_class.GPDriver(config)


    # Run the GP
    while gp_driver.run_count <= int(config.settings['num experiment runs']):

        gp_driver.log.write_run_header(gp_driver.run_count)

        while gp_driver.decide_termination():
            # Execute a turn
            gp_driver.move_units()

            gp_driver.update_world_state()
            
        gp_driver.check_update_world_file()

        gp_driver.init_run_variables()
        gp_driver.increment_run_count()

