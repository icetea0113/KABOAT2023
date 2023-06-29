#박스출력하는 함수 만들자
#가로는 +--를 n번 반복인데 마지막에 +추가
#세로는 |  (공백2번)을 n번 반복인데 마지막에 |추가
#그러면 m개의 박스를 한 줄 만들 수 있음

def print_box(n: int, m: int):
    horizontal_line = "+--" * m + "+"
    vertical_line = "|  " * m + "|"

#반복문 통해 m번 반복하면 n개의 가로?박스 만들게
    for _ in range(n):
        print(horizontal_line)
        print(vertical_line)

#근데 무조건 맨 밑에 가로줄 추가해야됨
    print(horizontal_line)

# 입력 받은 n과 m에 따라 박스 출력
n = int(input("가로 크기를 입력하세요: "))
m = int(input("세로 크기를 입력하세요: "))

#출력할 땐 반대로 해야됨
print_box(n, m)
