import itertools
import math
import json
import logging
import heapq

from .serializers import MapLayerSerializer
from .models import MapLayer

EMPTY = 1
WALL = 0
ELEVATOR = 2


class PathNotFoundException(Exception):
    pass


def convert_coordinates_from_geo_to_local(geo_position):
    coord_start = [(198, 299), (168, 270)]
    real_coord = [(60.484129, 15.418381), (60.484351, 15.417935)]
    scale = [(coord_start[1][0] - coord_start[0][0]) / (real_coord[1][0] - real_coord[0][0]),
                   (coord_start[1][1] - coord_start[0][1]) / (real_coord[1][1] - real_coord[0][1])]

    position_y, position_x = geo_position
    return int(coord_start[0][0] + (position_y - real_coord[0][0]) * scale[0]),\
           int(coord_start[0][1] + (position_x - real_coord[0][1]) * scale[1])


def convert_coordinates_from_local_to_geo(local_position):
    coord_start = [(198, 299), (168, 270)]
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

    last_dx = 0
    last_dy = 0
    current_dx = 0
    current_dy = 0

    while current_floor != -1:
        if last_dx == current_dx and last_dy == current_dy and (current_dx, current_dy) != (0, 0):
            path[-1] = (current_floor, (current_position_y, current_position_x))
        else:
            path.append((current_floor, (current_position_y, current_position_x)))
        # path.append((current_floor, (current_position_y, current_position_x)))

        next_floor, next_position_y, next_position_x = \
            previous[current_floor][current_position_y][current_position_x]

        last_dx, last_dy = current_dx, current_dy
        current_dx = next_position_x - current_position_x
        current_dy = next_position_y - current_position_y

        current_floor, current_position_y, current_position_x = next_floor, next_position_y, next_position_x


    path = relax_path(path)
    return path[::-1]


def no_intersections(floor, from_y, from_x, to_y, to_x):
    points_num = max(1, abs(from_x - to_x) + abs(from_y - to_y))

    for i in range(points_num):
        cur_x = from_x + int(i * (to_x - from_x) / points_num)
        cur_y = from_y + int(i * (to_y - from_y) / points_num)

        if floors[floor][cur_y][cur_x] == WALL:
            return False

    return True


def relax_path(path):
    l = 0
    r = 1

    new_path = []

    while l < len(path):
        new_path.append(path[l])
        while r < len(path) and path[l][0] == path[r][0] and \
            no_intersections(path[l][0], path[l][1][0], path[l][1][1], path[r][1][0], path[r][1][1]):
            r += 1
        l = r

    if new_path[-1] != path[-1]:
        new_path.append(path[-1])

    return new_path


def count_distance(from_y, from_x, to_y, to_x):
    return math.hypot(from_x - to_x, from_y - to_y)


def count_floor_distance(from_y, from_x, from_floor, to_y, to_x, to_floor):
    # return math.hypot(from_x - to_x, from_y - to_y) + 10 * (to_floor - from_floor)
    if from_floor == to_floor:
        return math.hypot(from_x - to_x, from_y - to_y)

    # elev_y, elev_x = (199, 299)
    return ((to_floor - from_floor) + math.hypot(from_x - elev_x, from_y - elev_y) +
                    math.hypot(to_x - elev_x, to_y - elev_y))
    # return result
    # for elev_y, elev_x in elevators:
    #     result = min(result,
    #         100 * (to_floor - from_floor) + math.hypot(from_x - elev_x, from_y - elev_y) +
    #         math.hypot(to_x - elev_x, to_y - elev_y)
    #     )


def compare_floors(floor):
    return floor['floor']


def get_floors():
    layers = MapLayer.objects.filter(title='Kupolen3')
    serializer = MapLayerSerializer(layers, many=True)
    sorted_floors = serializer.data
    sorted_floors.sort(key=compare_floors)
    floors = [json.loads(floor['field']) for floor in sorted_floors]
    # floors = [floor['field'] for floor in sorted_floors]
    # logging.error(floors)
    return floors


def find_shortest_path_in_locals(from_floor, from_position, to_floor, to_position):
    for elev in elevators:
        logging.error(elev)


    if from_position == to_position and from_floor == to_floor:
        return [(from_floor, from_position)]

    from_position_y, from_position_x = from_position
    to_position_y, to_position_x = to_position

    dpos = (-1, 0, 1)

    min_distance = [[[float('inf') for x in row] for row in floor] for floor in floors]
    previous = [[[(-1, -1, -1) for x in row] for row in floor] for floor in floors]

    queue = []  # FIXME to prior queue?
    heapq.heappush(queue, (count_floor_distance(from_position_y, from_position_x, from_floor,
        to_position_y, to_position_x, to_floor), from_floor, from_position_y, from_position_x))
    # logging.error(from_floor)
    # logging.error(from_position_y)
    # logging.error(from_position_x)
    min_distance[from_floor][from_position_y][from_position_x] = 0

    finish_point_x = -1
    finish_point_y = -1
    finish_distance = float('inf')
    elevator_found = to_floor == from_floor

    while len(queue) > 0:
        est_distance, floor, position_y, position_x = heapq.heappop(queue)

        if elevator_found and floor != to_floor:
            continue

        distance = min_distance[floor][position_y][position_x]

        logging.error((distance, floor, position_y, position_x))

        # if distance > min_distance[floor][position_y][position_x] + 1e-6:
        if distance < 0:
            continue

        if floor == to_floor and count_distance(position_y, position_x,
            to_position_y, to_position_x) < finish_distance:
            finish_point_x = position_x
            finish_point_y = position_y
            finish_distance = count_distance(position_y, position_x, to_position_y, to_position_x)

        if not elevator_found and floors[floor][position_y][position_x] == ELEVATOR:
        # if not elevator_found and (position_y, position_x) == (199, 299):
            elevator_found = True
            for next_floor in range(len(floors)):
                if next_floor == floor:
                    continue

                if floors[next_floor][position_y][position_x] == WALL:
                    continue

                if min_distance[next_floor][position_y][position_x] < distance + 1:
                    continue

                min_distance[next_floor][position_y][position_x] = distance + abs(floor - next_floor)
                previous[next_floor][position_y][position_x] = (floor, position_y, position_x)
                heapq.heappush(queue, (distance + abs(floor - next_floor) + count_floor_distance(
                    position_y, position_x, next_floor, to_position_y, to_position_x, to_floor
                ), next_floor, position_y, position_x))

                if (position_y, position_x) == to_position and next_floor == to_floor:
                    break

        # for dy, dx in itertools.product(dpos, repeat=2):
        for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
        # for dy, dx in ((2, 2), (2, -2), (-2, 2), (-2, -2), (-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)):
        # for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if dx == 0 and dy == 0:
                continue

            next_position_y = position_y + dy
            next_position_x = position_x + dx
            next_distance = distance + count_distance(position_y, position_x, next_position_y, next_position_x)

            # logging.error((' ', next_position_y, next_position_x, next_distance))

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
            heapq.heappush(queue, (next_distance + count_floor_distance(
                next_position_y, next_position_x, floor, to_position_y, to_position_x, to_floor
            ), floor, next_position_y, next_position_x))

        min_distance[floor][position_y][position_x] = -1

    if finish_point_x != -1:
        return extract_path(previous, to_floor, finish_point_y, finish_point_x)
    else:
        raise PathNotFoundException()


def find_shortest_path(from_floor, from_position, to_floor, to_position):
    from_local_position = convert_coordinates_from_geo_to_local(from_position)
    logging.error(from_position)
    logging.error(from_local_position)
    to_local_position = convert_coordinates_from_geo_to_local(to_position)
    local_shortest_path = find_shortest_path_in_locals(
        from_floor, from_local_position, to_floor, to_local_position)

    shortest_path = convert_path_from_local_to_geo(local_shortest_path)
    # return shortest_path
    return local_shortest_path


floors = get_floors()

if len(floors) > 0:
    elevators = []
    for pos_y in range(len(floors[0])):
        for pos_x in range(len(floors[0][0])):
            if floors[0][pos_y][pos_x] == ELEVATOR:
                elevators.append((pos_y, pos_x))
    elev_y, elev_x = elevators[-1]
