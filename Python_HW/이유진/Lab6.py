def calculate_character_frequencies(string):
    # 입력 문자열을 소문자로 변환
    string = string.lower()

    # 문자 개수를 세기 위한 딕셔너리 초기화
    character_counts = {}

    # 문자열을 순회하며 개수를 세기
    for char in string:
        if char != ' ':
            character_counts[char] = character_counts.get(char, 0) + 1

    # 문자들의 총 개수 계산
    total_characters = sum(character_counts.values())

    # 문자의 빈도수 비율 계산
    frequencies = {}
    for char, count in character_counts.items():
        frequency = (count / total_characters)
        frequencies[char] = frequency

    # 가장 큰 빈도수 값을 찾아 소수점 이하 두 자리까지 출력
    max_frequency = max(frequencies.values())
    max_frequency = "{:.2f}".format(max_frequency)

    # 최대 빈도수 값 출력
    print("Max Frequency: {}".format(max_frequency))


# 문자열 입력 받기
input_string = input("문자열을 입력하세요: ")

# 문자열의 문자 빈도수 계산 및 최대 빈도수 출력
calculate_character_frequencies(input_string)
