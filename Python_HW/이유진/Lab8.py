def count_369(n, m):
    count = 0
    for num in range(n, m + 1):
        num_str = str(num)
        count += num_str.count('3') + num_str.count('6') + num_str.count('9')
    return count

# 시작 숫자와 끝나는 숫자를 입력 받습니다.
start_num, end_num = map(int, input("시작 숫자와 끝나는 숫자를 입력하세요: ").split())

# 369 게임에서 3, 6, 9가 등장하는 횟수를 계산합니다.
result = count_369(start_num, end_num)

# 결과를 출력합니다.
print("369 게임 결과:", result)
