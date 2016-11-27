# public void processTrajectory(Gyro gyro) {
#         List<Position> trajectory;
#         Position speed; // (pixel / tick?)
#         int curTime = MILLISECONDS_IN_TICK;
#         while(curTime > 0 && trajectory.size() > 1) {
#             Double distance = calculateDistance(trajectory.get(1), trajectory.get(0));
#             if (distance == 0) {
#                 //лифт
#             }
#             else {
#                 Double deltaDistance = speed * MILLISECONDS_IN_TICK;
#                 if (distance > deltaDistance) {
#                     Position newPosition = trajectory.get(0) + (trajectory.get(1) - trajectory.get(0)) * deltaDistance / distance;
#                     trajectory.remove(0);
#                     trajectory.add(0, newPosition);
#                 } else if (distance == deltaDistance) {
#                     trajectory.remove(0);
#                 } else if (distance < deltaDistance) {
#                     curTime = curTime - distance / speed;
#                     trajectory.remove(0);
#                 }
#             }
#         }
#     }

import numpy as np


def distance(x, y):
    return sum((x - y) ** 2) ** 0.5


def iterate(pos, route, spd, tick):
    new_pos = pos
    max_dist = spd * tick
    cur_dist = distance(pos, route[0])
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
            return new_pos, route
    return new_pos, route


pos = np.array([0,0])
route = np.array([(0,10),(10,10),(10,20)])
while(True):
    pos, route = iterate(pos,
                  route,
                  11,
                  1)
    print(pos)
    if len(route) == 0:
        break