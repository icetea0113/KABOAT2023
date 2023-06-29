def find_earliest_sign(years):
    zodiac_signs = {
        4: "쥐",
        5: "소",
        6: "호랑이",
        7: "토끼",
        8: "용",
        9: "뱀",
        10: "말",
        11: "양",
        0: "원숭이",
        1: "닭",
        2: "개",
        3: "돼지"
    }
    
    unique_signs = set()
    earliest_sign = None
    
    for year in years:
        sign = year % 12
        unique_signs.add(sign)
        if earliest_sign is None or sign < earliest_sign:
            earliest_sign = sign
    
    return len(unique_signs), zodiac_signs[earliest_sign]

# 입력을 받습니다.
years = list(map(int, input().split()))

# 결과를 계산합니다.
num_signs, earliest_sign = find_earliest_sign(years)

# 결과를 출력합니다.
print(f"{num_signs} {earliest_sign}")