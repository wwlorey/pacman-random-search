import random

def find_path(starting_coord, coords_to_find, get_adj_coords, wall_coords):
    neighbors_queue = [starting_coord]
    found_coords = set([])

    while neighbors_queue:
        c = neighbors_queue.pop()

        for adj_c in [adj_c for adj_c in get_adj_coords(c) if not adj_c in wall_coords]:
            if not adj_c in found_coords:
                found_coords.add(adj_c)
                neighbors_queue.append(adj_c)

    return found_coords == coords_to_find


def all_cells_reachable(wall_coords, get_adj_coords, pacman_coord, all_coords):
    """Returns True if there is a path from pacman's starting cell
    to every other non-wall cell. Returns False otherwise.
    """
    # Construct a set of coordinates to find
    coords_to_find = all_coords.difference(wall_coords)

    # Determine if a path exists
    return find_path(pacman_coord, coords_to_find, get_adj_coords, wall_coords)


def can_add_wall(coord, wall_coords, can_move_to, get_adj_coords, pacman_coord, all_coords):
    """Determines if a wall can be added to the world at coord.

    A wall placement is unsuccessful if it blocks a portion of the world
    from being reachable from any arbitrary coordinate in the world.

    Reachability is guaranteed by finding a path from pacman's beginning cell 
    to every cell in the world.

    Returns True if a wall can be added, False otherwise.
    """
    return can_move_to(coord) and all_cells_reachable(wall_coords.union(set([coord])), get_adj_coords, pacman_coord, all_coords)


def get_walls(all_coords, pacman_coord, ghost_coords, wall_coords, wall_density, get_adj_coords, can_move_to):
    """Returns a list of walls that can safely be added to the world while maintaining
    reachability of all non-wall cells.
    """
    walls = []

    for c in all_coords.difference(set([pacman_coord])).difference(set([ghost_coords[0]])):
        if random.random() < wall_density and can_add_wall(c, wall_coords, can_move_to, get_adj_coords, pacman_coord, all_coords):
            walls.append(c)

    return walls

