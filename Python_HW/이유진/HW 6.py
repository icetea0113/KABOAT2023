def calculate_weight_ratio(sentence):
    # 문장을 소문자로 변환합니다.
    sentence = sentence.lower()

    # 각 문자의 빈도를 계산합니다.
    character_count = {}
    vowel_weight = 2  # 모음의 무게를 2배로 설정합니다.
    wy_weight = 1.5  # 'w'와 'y'의 무게를 1.5배로 설정합니다.
    for char in sentence:
        if char.isalpha():
            if char in 'aeiou':
                character_count[char] = character_count.get(char, 0) + vowel_weight
            elif char in 'wy':
                character_count[char] = character_count.get(char, 0) + wy_weight
            else:
                character_count[char] = character_count.get(char, 0) + 1

    # 가장 무거운 문자를 찾습니다.
    가장무거운_문자 = max(character_count, key=character_count.get)
    가장무거운_무게 = character_count[가장무거운_문자]

    # 무게 비율을 계산합니다.
    전체_무게 = sum(character_count.values())
    무게_비율 = 가장무거운_무게 / 전체_무게

    return round(무게_비율, 3)

# 사용자로부터 입력 문장을 받습니다.
입력_문장 = input("문장을 입력하세요: ")

# 무게 비율을 계산하고 출력합니다.
무게_비율 = calculate_weight_ratio(입력_문장)
print("무게 비율:", 무게_비율)
