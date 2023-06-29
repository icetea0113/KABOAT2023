# 직사각형의 좌표를 입력받습니다.
xL, yL, xR, yR = map(int, input().split())

# 직사각형 위에 있는 점의 개수를 세는 변수를 초기화합니다.
count = 0

# 점을 입력받고, 직사각형 위에 있는 점인지 확인하여 개수를 세줍니다.
while True:
    try:
        x, y = map(int, input().split())
        if xL <= x <= xR and yL <= y <= yR:
            count += 1
    except ValueError:
        break

# 직사각형 위에 있는 점의 개수를 출력합니다.
print("직사각형 위에 있는 점의 개수:", count)
