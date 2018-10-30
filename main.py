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


    # Testing
    import world.gpac_world as world_class

    world = world_class.GPacWorld(config)
    world.visualize()
    print(world.check_game_over())


    # Initialize the GP driver and its run variables
    gp_driver = gp_driver_class.GPDriver(config)


    # Run the GP
    while gp_driver.run_count <= int(config.settings['num experiment runs']):

        gp_driver.log.write_run_header(gp_driver.run_count)

        while gp_driver.decide_termination():
            # TODO: Run the GP
            gp_driver.eval_count += 1

        gp_driver.init_run_variables()
        gp_driver.increment_run_count()

