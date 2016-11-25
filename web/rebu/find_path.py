
import itertools
import json
import logging

from .serializers import MapLayerSerializer
from .models import MapLayer

EMPTY = 0
WALL = 1
ELEVATOR = 2


class PathNotFoundException(Exception):
    pass


def convert_coordinates_from_geo_to_local(geo_position):
    local_position = geo_position
    return local_position


def convert_coordinates_from_local_to_geo(geo_position):
    local_position = geo_position
    return local_position


def convert_path_from_local_to_geo(local_path):
    return [convert_coordinates_from_local_to_geo(crd) for crd in local_path]


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

def compare_floors(floor):
    return floor['floor']

def find_shortest_path_in_locals(from_floor, from_position, to_floor, to_position):
    if from_position == to_position and from_floor == to_floor:
        return [(from_floor, from_position)]

    from_position_y, from_position_x = from_position
    to_position_y, to_position_x = to_position

    layers = MapLayer.objects.all()
    serializer = MapLayerSerializer(layers, many=True)
    sorted_floors = serializer.data
    sorted_floors.sort(key=compare_floors)
    floors = [json.loads(floor['field']) for floor in sorted_floors]
    logging.error(floors)
    dpos = [-1, 0, 1]

    is_visited = [[[False for x in row] for row in floor] for floor in floors]
    previous = [[[(-1, -1, -1) for x in row] for row in floor] for floor in floors]

    queue = []  # FIXME to prior queue?
    queue.append((from_floor, from_position_y, from_position_x))
    is_visited[from_floor][from_position_y][from_position_x] = True

    while len(queue) > 0:
        floor, position_y, position_x = queue.pop()

        for df, dy, dx in itertools.product(dpos, repeat=3):
            next_floor = floor + df
            next_position_y = position_y + dy
            next_position_x = position_x + dx

            if next_floor < 0 or next_floor >= len(floors):
                continue

            if next_position_y < 0 or next_position_y >= len(floors[next_floor]):
                continue
            if next_position_x < 0 or next_position_x >= len(floors[next_floor][next_position_y]):
                continue

            if is_visited[next_floor][next_position_y][next_position_x]:
                continue

            if df != 0 and floors[floor][position_y][position_x] != 2:
                continue
            if floors[next_floor][next_position_y][next_position_x] == 1:
                continue

            if (dx != 0 and dy != 0) or (dx != 0 and df != 0) or (dy != 0 and df != 0):
                continue

            is_visited[next_floor][next_position_y][next_position_x] = True
            previous[next_floor][next_position_y][next_position_x] = (floor, position_y, position_x)
            queue.append((next_floor, next_position_y, next_position_x))

            if (next_position_y, next_position_x) == to_position and next_floor == to_floor:
                break

    if is_visited[to_floor][to_position_y][to_position_x]:
        return extract_path(previous, to_floor, to_position_y, to_position_x)
    else:
        raise PathNotFoundException()


def find_shortest_path(from_floor, from_position, to_floor, to_position):
    from_local_position = convert_coordinates_from_geo_to_local(from_position)
    to_local_position = convert_coordinates_from_geo_to_local(to_position)
    local_shortes_path = find_shortest_path_in_locals(
        from_floor, from_local_position, to_floor, to_local_position)

    shortest_path = convert_path_from_local_to_geo(local_shortes_path)
    return shortest_path
