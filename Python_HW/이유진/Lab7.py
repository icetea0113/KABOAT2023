def calculate_change(coin_types, amount):
    coin_types = sorted(coin_types, reverse=True)  # 동전 종류를 내림차순으로 정렬
    quotient_list = []  # 몫들을 저장할 리스트

    for coin in coin_types:
        quotient = amount // coin  # 현재 동전으로 변경할 수 있는 최대 개수 계산
        quotient_list.append(str(quotient))  # 몫을 문자열로 변환하여 리스트에 추가
        amount %= coin  # 현재 동전으로 변경한 나머지 금액

    return ' '.join(quotient_list)  # 몫들을 공백으로 구분하여 문자열로 반환

# 동전 종류 입력 받기
coin_input = input("동전 종류를 입력하세요 (공백으로 구분): ")
coin_types = list(map(int, coin_input.split()))

# 변경 금액 입력 받기
amount = int(input("변경 금액을 입력하세요: "))

# 몫들 계산하여 출력하기
result = calculate_change(coin_types, amount)
print("변경에 필요한 동전의 개수: " + result)