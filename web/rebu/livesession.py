import logging

import numpy as np

def distance(x, y):
    return sum((np.array(x) - np.array(y)) ** 2) ** 0.5


def iterate(pos, route, spd, tick):
    pos = np.array(pos)
    route = np.array(route)
    new_pos = pos
    max_dist = spd * tick
    cur_dist = distance(pos, route[0])
    logging.error(pos)
    logging.error(route[0])
    while max_dist > 0:
        if cur_dist > max_dist:
            new_pos = new_pos + (route[0] - new_pos) * max_dist / cur_dist
        else:
            new_pos = route[0]
            route = route[1:]
        max_dist -= cur_dist
        if len(route) > 0:
            cur_dist = distance(new_pos, route[0])
        else:
            return new_pos.tolist(), route.tolist()
    return new_pos.tolist(), route.tolist()