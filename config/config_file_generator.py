#!/usr/bin/env python3

config_template = '[DEFAULT]\n\
\n\
###################################\n\
# GP Parameters\n\
###################################\n\
num experiment runs = 3\n\
num fitness evals = 2000\n\
\n\
###################################\n\
# World Generation Parameters\n\
###################################\n\
width = {width}\n\
height = {height}\n\
pill density = {pill density}\n\
wall density = {wall density}\n\
num ghosts = 3\n\
\n\
num wall carvers = {num wall carvers}\n\
max wall carver travel distance = 10\n\
min wall carver travel distance = 3\n\
\n\
use external seed = False\n\
default seed = 123456789\n\
\n\
###################################\n\
# Score \n\
###################################\n\
fruit spawn prob = {fruit spawn prob}\n\
fruit score = {fruit score}\n\
\n\
###################################\n\
# Timing\n\
###################################\n\
time multiplier = {time multiplier}\n\
\n\
###################################\n\
# Output Files\n\
###################################\n\
log file path = output/{experiment name}_log.txt\n\
world file path = output/highest_score_game_sequence_all_time_step_world_file_{experiment name}.txt\n'

config_data = \
[
    (10, 10, 50, 25, 0.05, 10, 2, 'small', 4), 
    (30, 20, 20, 30, 0.05, 10, 2, 'med_small', 4), 
    (40, 50, 70, 35, 0.05, 10, 2, 'med_large', 5), 
    (80, 80, 30, 30, 0.05, 10, 2, 'large', 5)
]

FILE_NAME_INDEX = 7

config_data_key = ['width', 'height', 'pill density', 'wall density', 'fruit spawn prob', 'fruit score', 'time multiplier', 'experiment name', 'num wall carvers']


# Populate new config files
for tup in config_data:
    config_str = config_template

    for i in range(len(tup)):
        search_str = '{' + config_data_key[i] + '}'

        insertion_index = config_str.find(search_str)

        while insertion_index >= 0:
            config_str = config_str[:insertion_index] + str(tup[i]) + config_str[insertion_index + len(search_str):]

            insertion_index = config_str.find(search_str)

    # Create config file
    file_name = tup[FILE_NAME_INDEX] + '.cfg'

    f = open(file_name, 'w')

    f.write(config_str)
    f.close()

