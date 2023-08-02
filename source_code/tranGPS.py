import math
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Proj, transform

def rotate_vector(vec, angle):
    """Rotate a vector by a given angle (in radians)"""
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    rot_matrix = np.array([[cos_angle, -sin_angle],
                           [sin_angle,  cos_angle]])
    return np.dot(rot_matrix, vec)

def translate_to_origin(coords):
    """Translate a set of coordinates so that the first coordinate is at the origin."""
    return [(coord[0]-coords[0][0], coord[1]-coords[0][1]) for coord in coords]

def rotate_coords(coords, angle):
    """Rotate a set of coordinates by a given angle (in radians) around the origin."""
    return [rotate_vector(coord, angle) for coord in coords]

rect_coords = [(35.23218089999, 129.0792796),(35.2321492999,129.0793337), (35.2322719,129.07941599999),(35.2323047, 129.0793592)]

# ENU 좌표 변환을 위한 라이브러리 초기화 (적절한 UTM 존 선택 필요)
proj_utm = Proj(proj='utm', zone=52, ellps='WGS84', units='m', datum='WGS84')

# 직사각형 좌표를 ENU 좌표로 변환
enu_coords = [proj_utm(lon, lat) for lat, lon in rect_coords]

# 기울어진 직사각형의 두 변의 벡터 계산
vec1 = np.array(enu_coords[1]) - np.array(enu_coords[0])
vec2 = np.array(enu_coords[2]) - np.array(enu_coords[1])

# 90도 각도 보정 (라디안)
correction_angle = np.pi/2 - math.atan2(vec2[1], vec2[0]) + math.atan2(vec1[1], vec1[0])

# vec2를 회전시켜 vec1에 수직이 되도록 만든다.
vec2_rotated = rotate_vector(vec2, correction_angle)

# 보정된 직사각형의 꼭짓점 계산
corrected_coords = [enu_coords[0],
                    enu_coords[0] + vec1,
                    enu_coords[0] + vec1 + vec2_rotated,
                    enu_coords[0] + vec2_rotated]

# 좌표를 원점으로 이동
translated_coords = translate_to_origin(corrected_coords)

# 현재 기울어진 정도를 계산 (라디안)
tilt_angle = math.atan2(corrected_coords[2][1] - corrected_coords[1][1], corrected_coords[2][0] - corrected_coords[1][0])

# 90도에서 현재 기울어진 정도를 뺀다 (라디안)
rotation_angle = np.pi/2 - tilt_angle

# 좌표를 추가로 회전 (반시계 방향)
final_coords = rotate_coords(translated_coords, rotation_angle)

# 보정된 ENU 좌표에서 East, North 값 추출
east_coords, north_coords = zip(*final_coords)
east_coords = list(east_coords)
north_coords = list(north_coords)

# 그래프 그리기
plt.figure()
plt.plot(east_coords + [east_coords[0]], north_coords + [north_coords[0]], marker='o')  # 직사각형 그리기
plt.xlabel('East (m)')
plt.ylabel('North (m)')
plt.title('ENU Coordinates of Tilted Rectangle')
plt.grid(True)
plt.axis('equal')  # x, y 축 비율 동일하게 설정
plt.show()
