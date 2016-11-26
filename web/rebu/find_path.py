import itertools
import math
import json
import logging
import heapq

from .serializers import MapLayerSerializer
from .models import MapLayer

EMPTY = 0
WALL = 1
ELEVATOR = 2


class PathNotFoundException(Exception):
    pass


def convert_coordinates_from_geo_to_local(geo_position):
    coord_start = [(299, 198), (270, 168)]
    real_coord = [(60.484129, 15.418381), (60.484351, 15.417935)]
    scale = [(coord_start[1][0] - coord_start[0][0]) / (real_coord[1][0] - real_coord[0][0]),
                   (coord_start[1][1] - coord_start[0][1]) / (real_coord[1][1] - real_coord[0][1])]

    position_y, position_x = geo_position
    return int(coord_start[0][0] + (position_y - real_coord[0][0]) * scale[0]),\
           int(coord_start[0][1] + (position_x - real_coord[0][1]) * scale[1])


def convert_coordinates_from_local_to_geo(local_position):
    coord_start = [(299, 198), (270, 168)]
    real_coord = [(60.484129, 15.418381), (60.484351, 15.417935)]
    scale = [(coord_start[1][0] - coord_start[0][0]) / (real_coord[1][0] - real_coord[0][0]),
                   (coord_start[1][1] - coord_start[0][1]) / (real_coord[1][1] - real_coord[0][1])]

    position_y, position_x = local_position
    return round(real_coord[0][0] + (position_y - coord_start[0][0]) / scale[0], 6),\
           round(real_coord[0][1] + (position_x - coord_start[0][1]) / scale[1], 6)


def convert_path_from_local_to_geo(local_path):
    return [(floor, convert_coordinates_from_local_to_geo(crd)) for floor, crd in local_path]


def extract_path(previous, to_floor, to_position_y, to_position_x):
    path = []

    current_floor = to_floor
    current_position_x = to_position_x
    current_position_y = to_position_y

    while current_floor != -1:
        path.append((current_floor, (current_position_y, current_position_x)))

        current_floor, current_position_y, current_position_x = \
            previous[current_floor][current_position_y][current_position_x]

    return path[::-1]


def count_distance(from_y, from_x, to_y, to_x):
    return math.hypot(from_x - to_x, from_y - to_y)


def compare_floors(floor):
    return floor['floor']


def get_floors():
    layers = MapLayer.objects.filter(title='Kupolen')
    serializer = MapLayerSerializer(layers, many=True)
    sorted_floors = serializer.data
    sorted_floors.sort(key=compare_floors)
    floors = [json.loads(floor['field']) for floor in sorted_floors]
    # logging.error(floors)
    return floors


def find_shortest_path_in_locals(floors, from_floor, from_position, to_floor, to_position):
    if from_position == to_position and from_floor == to_floor:
        return [(from_floor, from_position)]

    from_position_y, from_position_x = from_position
    to_position_y, to_position_x = to_position

    dpos = [-1, 0, 1]

    min_distance = [[[float('inf') for x in row] for row in floor] for floor in floors]
    previous = [[[(-1, -1, -1) for x in row] for row in floor] for floor in floors]

    queue = []  # FIXME to prior queue?
    heapq.heappush(queue, (0, from_floor, from_position_y, from_position_x))
    logging.error(from_floor)
    logging.error(from_position_y)
    logging.error(from_position_x)
    min_distance[from_floor][from_position_y][from_position_x] = 0

    finish_point_x = -1
    finish_point_y = -1
    finish_distance = float('inf')

    while len(queue) > 0:
        distance, floor, position_y, position_x = heapq.heappop(queue)

        # logging.error('{} {} {} {}'.format(distance, floor, position_y, position_x))

        if distance > min_distance[floor][position_y][position_x] + 1e-6:
            continue

        if floor == to_floor and count_distance(position_y, position_x,
            to_position_y, to_position_x) < finish_distance:
            finish_point_x = position_x
            finish_point_y = position_y
            finish_distance = count_distance(position_y, position_x, to_position_y, to_position_x)

        if floors[floor][position_y][position_x] == ELEVATOR:
            for df in (-1, 1):
                next_floor = floor + df
                if next_floor < 0 or next_floor >= len(floors):
                    continue

                if floors[next_floor][position_y][position_x] == WALL:
                    continue

                if min_distance[next_floor][position_y][position_x] < distance + 1:
                    continue

                min_distance[next_floor][position_y][position_x] = distance + 1
                previous[next_floor][position_y][position_x] = (floor, position_y, position_x)
                heapq.heappush(queue, (distance + 1, next_floor, position_y, position_x))

                if (position_y, position_x) == to_position and next_floor == to_floor:
                    break

        for dy, dx in itertools.product(dpos, repeat=2):
            if dx == 0 and dy == 0:
                continue

            next_position_y = position_y + dy
            next_position_x = position_x + dx
            next_distance = distance + count_distance(position_y, position_x, next_position_y, next_position_x)

            # print(' ', next_position_y, next_position_x, next_distance)

            if next_position_y < 0 or next_position_y >= len(floors[floor]):
                continue
            if next_position_x < 0 or next_position_x >= len(floors[floor][next_position_y]):
                continue

            if min_distance[floor][next_position_y][next_position_x] < next_distance + 1e-6:
                continue

            if floors[floor][next_position_y][next_position_x] == WALL:
                continue

            min_distance[floor][next_position_y][next_position_x] = next_distance
            previous[floor][next_position_y][next_position_x] = (floor, position_y, position_x)
            heapq.heappush(queue, (next_distance, floor, next_position_y, next_position_x))


    if finish_point_x != -1:
        return extract_path(previous, to_floor, finish_point_y, finish_point_x)
    else:
        raise PathNotFoundException()


def find_shortest_path(from_floor, from_position, to_floor, to_position):
    from_local_position = convert_coordinates_from_geo_to_local(from_position)
    logging.error(from_position)
    logging.error(from_local_position)
    to_local_position = convert_coordinates_from_geo_to_local(to_position)
    local_shortes_path = find_shortest_path_in_locals(get_floors(),
        from_floor, from_local_position, to_floor, to_local_position)

    shortest_path = convert_path_from_local_to_geo(local_shortes_path)
    return shortest_path
