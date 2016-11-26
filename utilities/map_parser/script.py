from collections import Counter

import numpy as np
from PIL import Image

# im = Image.open("1.png")
# im.thumbnail()
# im = im.quantize(30)
# im.save('1quantized.png')
# print(im.size)
# width, height = im.size

# for tset case we use Kupolen Köpcentrum
# lift coordinates are 60.484129, 15.418381, it will be the start of coordinates
# this is the Kupolen coordinates in google maps 60.484351, 15.417935
# 43 255 57

# for i in range(1, 4):
#     im = Image.open(str(i) + "blacked.png")
#     im = im.resize((im.width // 6, im.height // 6))
#     im.save(str(i) + 'smaller.png')l

# def maptomatrix(x):
#     if x == (255, 255, 255, 255):
#         return 1
#     elif x == (0, 255, 0, 255):
#         return 2
#     else:
#         return 0

# matrix - матрица смежности графа получаемая по картинками
# coord_start[0] - лифт, coord_start[1] - вторая зеленая точка
# matrix = []
# for i in range(1, 4):
#     im = Image.open(str(i) + 'smaller.png')
#     data = [tuple(i) for i in list(im.getdata())]
#     matrix.append(np.array(list(map(maptomatrix, data))).reshape((im.width, im.height)))

coord_start = [(299, 198), (270, 168)]
real_coord = [(60.484129, 15.418381), (60.484351, 15.417935)]
scale = [(coord_start[1][0] - coord_start[0][0]) / (real_coord[1][0] - real_coord[0][0]),
               (coord_start[1][1] - coord_start[0][1]) / (real_coord[1][1] - real_coord[0][1])]
print(scale)

def getMatrixCoordinates(x):
    return int(coord_start[0][0] + (x[0] - real_coord[0][0]) * scale[0]),\
           int(coord_start[0][1] + (x[1] - real_coord[0][1]) * scale[0])

def getRealCoordinates(x):
    return round(real_coord[0][0] + (x[0] - coord_start[0][0]) / scale[0], 6),\
           round(real_coord[0][1] + (x[1] - coord_start[0][1]) / scale[0], 6)

print(getMatrixCoordinates((60.484250, 15.418000)))
print(getRealCoordinates((350, 150)))
