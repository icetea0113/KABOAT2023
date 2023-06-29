def calculate_overlap_area(rectangles):
    x_coords = []
    y_coords = []

    # 모든 직사각형의 x, y 좌표를 수집합니다.
    for rect in rectangles:
        x_coords.append(rect[0])  # x 좌표의 왼쪽 변
        x_coords.append(rect[2])  # x 좌표의 오른쪽 변
        y_coords.append(rect[1])  # y 좌표의 아래쪽 변
        y_coords.append(rect[3])  # y 좌표의 위쪽 변

    # x 좌표 리스트를 정렬하여 두 번째로 큰 값을 찾습니다.
    x_coords.sort()
    second_largest_x = x_coords[-2]
    third_largest_x = x_coords[-3]
    # y 좌표 리스트를 정렬하여 세 번째로 큰 값을 찾습니다.
    y_coords.sort()
    second_largest_y = y_coords[-2]
    third_largest_y = y_coords[-3]

    # 겹치는 영역의 가로와 세로 길이를 계산합니다.
    width = second_largest_x - third_largest_x
    height = second_largest_y - third_largest_y

    # 겹치는 영역의 면적을 계산합니다.
    overlap_area = max(0, width) * max(0, height)

    return overlap_area


# n개의 직사각형 정보를 입력받습니다.
n = int(input("직사각형의 개수를 입력하세요: "))
rectangles = []
for i in range(n):
    print(f"직사각형 {i+1}의 좌하단과 우상단 좌표를 입력하세요: ")
    xL, yL, xR, yR = map(int, input().split())
    rectangles.append((xL, yL, xR, yR))

# 겹치는 영역의 면적을 계산하고 출력합니다.
overlap_area = calculate_overlap_area(rectangles)
print("겹치는 영역의 면적은:", overlap_area)
