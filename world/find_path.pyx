def find_path(starting_coord, coords_to_find, get_neighbors, wall_coords):
    neighbors_queue = [starting_coord]
    found_coords = set([])

    while neighbors_queue:
        c = neighbors_queue.pop()

        for adj_c in [adj_c for adj_c in get_neighbors(c) if not adj_c in wall_coords]:
            if not adj_c in found_coords:
                found_coords.add(adj_c)
                neighbors_queue.append(adj_c)

    return found_coords == coords_to_find

