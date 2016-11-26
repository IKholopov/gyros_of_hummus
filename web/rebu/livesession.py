import logging

import numpy as np

def distance(x, y):
    return sum((np.array(x) - np.array(y)) ** 2) ** 0.5


def iterate(pos, floor, route, spd, tick):
    new_pos = np.array(pos)
    max_dist = spd * tick
    if len(route) == 0:
        return new_pos, floor, route
    if route[0][0] == floor:
        cur_dist = distance(pos, route[0][1])
    else:
        cur_dist = 2
    while max_dist > 0:
        if cur_dist > max_dist:
            new_pos = new_pos + (np.array(route[0][1]) - new_pos) * max_dist / cur_dist
        else:
            new_pos = np.array(route[0][1])
            floor = route[0][0]
            route = route[1:]
        max_dist -= cur_dist
        if len(route) > 0:
            if route[0][0] == floor:
                cur_dist = distance(new_pos, route[0][1])
            else:
                if max_dist < 0:
                    floor = route[0][0]
                cur_dist = 2
        else:
            return new_pos.tolist(), floor, route
    return new_pos.tolist(), floor, route
