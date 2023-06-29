def move_bar_left(input_string: str) -> None:
    bar_index = input_string.index('|') if '|' in input_string else -1

    if bar_index == -1:
        print("막대기(|)가 입력된 문자열에 존재하지 않습니다.")
        return

    direction = 1  # 막대 이동 방향 (1: 오른쪽, -1: 왼쪽)

    while 0 <= bar_index < len(input_string):
        for index in range(len(input_string)):
            if index == bar_index:
                print(f"{input_string[:bar_index]}|{input_string[bar_index+1:]}")

        if bar_index == len(input_string) - 1:
            direction = -1

        bar_index += direction

    direction = 1  # 다시 오른쪽으로 이동
    bar_index = len(input_string) - 2  # 막대를 제외한 가장 오른쪽 문자 인덱스

    while 0 <= bar_index < len(input_string):
        for index in range(len(input_string)):
            if index == bar_index:
                print(f"{input_string[:bar_index]}|{input_string[bar_index+1:]}")

        if bar_index == 0:
            direction = 1

        bar_index -= direction

    print(input_string)  # 최종 변환된 문자열 출력

# 입력 받은 문자열에 막대기(|)가 포함되어 있다고 가정
input_string = input("문자열을 입력하세요: ")
move_bar_left(input_string)
