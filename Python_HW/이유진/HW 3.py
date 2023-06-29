# 문자 입력해놓기
character = input("문자선택 (# 또는 $): ")

# 숫자열 입력 받고 공백으로 쪼개기
numbers = list(map(int, input("숫자열 입력: ").split()))

# 누적 그래프 생성
cumulative_graph = []
cumulative_sum = 0

# 누적 그래프 계산
for num in numbers:
    cumulative_sum += num
    cumulative_graph.append(cumulative_sum)

# 그래프 정렬 방향 결정
if character == '#':
    cumulative_graph = cumulative_graph[::-1]  # 그래프를 뒤집어 위쪽 정렬
elif character == '$':
    pass  # 그래프를 그대로 유지하여 아래쪽 정렬

# 누적 그래프 출력 (오른쪽으로 90도 회전)
max_value = max(cumulative_graph)
if character == '$':
    for i in range(max_value, 0, -1):
        for value in cumulative_graph:
            if value >= i:
                print(character, end='')
            else:
                print(' ', end='')
        print()
elif character == '#':
    reversed_graph = cumulative_graph[::-1]
    for i in range(1, max_value+1):
        for value in reversed_graph:
            if value >= i:
                print(character, end='')
            else:
                print(' ', end='')
        print()