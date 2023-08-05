import math
import pymap3d as pm
import heapq
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def get_xy(e, n, angle):
    x = e * math.cos(angle) + n * math.sin(angle)
    y = -e * math.sin(angle) + n * math.cos(angle)
    return x,y

stadium_gps = [(35.2323047, 129.0793592),(35.23218089999, 129.0792796),(35.2321492999,129.0793337), (35.2322719,129.07941599999)]

stadium_enu = [[0, 0]]
angle = -10000
for value in stadium_gps[1:]:
    e, n, _ = pm.geodetic2enu(value[0], value[1], 0, stadium_gps[0][0], stadium_gps[0][1], 0)
    if angle == -10000:
        angle = math.atan2(n,e)
    e, n = get_xy(e, n, angle)
    stadium_enu.append([e, n])

polygon = Polygon(stadium_enu)

# 다각형을 그리기 위해 x, y 좌표를 얻습니다.
x,y = polygon.exterior.xy

# 그래프에 다각형을 그립니다.
plt.plot(x, y)
plt.axis('equal')
plt.show()