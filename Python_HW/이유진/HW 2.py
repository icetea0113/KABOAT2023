n = int(input())

total_boxes = sum(range(1, n+1))  # 1부터 n까지의 숫자를 모두 더한 값

# 내리막 계단 출력
for i in range(1, n+1):
    print("+--" * i + "+")  # 상단부 출력
    print("|  " * i + "|")  # 내리막 부분 출력

# 하단부 출력
print("+--" * (n)+ "+")

print(f"총 {total_boxes}개의 박스를 사용하여 내리막 계단을 만들었습니다.")
