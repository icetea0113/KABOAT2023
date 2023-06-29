def move_bar_right(bar_string):
    bar_index = bar_string.index('|')  # 막대기 기호 위치
    new_bar_string = bar_string[:bar_index] + bar_string[bar_index + 1:] + '|'  # 오른쪽으로 이동
    return new_bar_string

def replace_consonant_on_left(bar_string):
    bar_index = bar_string.index('|')  # 막대기 기호 위치
    left_char = bar_string[bar_index - 1]  # 막대기 기호 왼쪽 문자
    if left_char.isalpha() and left_char.lower() not in 'aeiou':  # 자음인 경우 *로 대체
        bar_string = bar_string[:bar_index - 1] + '*' + bar_string[bar_index:]
    return bar_string

def replace_vowel_on_right(bar_string):
    bar_index = bar_string.index('|')  # 막대기 기호 위치
    right_char = bar_string[bar_index + 1]  # 막대기 기호 오른쪽 문자
    if right_char.isalpha() and right_char.lower() in 'aeiou':  # 모음인 경우 #으로 대체
        bar_string = bar_string[:bar_index] + '#' + bar_string[bar_index + 1:]
    return bar_string

def replace_vowel_on_right(bar_string):
    bar_index = bar_string.index('|')  # 막대기 기호 위치
    if bar_index < len(bar_string) - 1:  # 막대기 기호 오른쪽에 문자가 있는 경우에만 실행
        right_char = bar_string[bar_index + 1]  # 막대기 기호 오른쪽 문자
        if right_char.isalpha() and right_char.lower() in 'aeiou':  # 모음인 경우 #으로 대체
            bar_string = bar_string[:bar_index] + '#' + bar_string[bar_index + 1:]
    return bar_string

def replace_vowel_on_right(bar_string):
    bar_index = bar_string.index('|')  # 막대기 기호 위치
    if bar_index < len(bar_string) - 1:  # 막대기 기호 오른쪽에 문자가 있는 경우에만 실행
        right_char = bar_string[bar_index + 1]  # 막대기 기호 오른쪽 문자
        if right_char.isalpha() and right_char.lower() in 'aeiou':  # 모음인 경우 #으로 대체
            bar_string = bar_string[:bar_index] + '#' + bar_string[bar_index + 1:]
    return bar_string


def process_bar_string(bar_string):
    length = len(bar_string)
    bar_index = bar_string.index('|')  # 막대기 기호 위치

    while True:
        if bar_index == 0:  # 막대기 기호가 문자열의 첫 번째 자리에 도달한 경우
            bar_string = move_bar_right(bar_string)  # 오른쪽으로 이동
            bar_string = replace_consonant_on_left(bar_string)  # 왼쪽 자음 대체
            print(bar_string)
            if bar_string[bar_index + 1].lower() in 'aeiou':  # 막대기 기호 오른쪽 문자가 모음인 경우
                bar_string = replace_vowel_on_right(bar_string)  # 오른쪽 모음 대체
                print(bar_string)
                break  # 종료

        elif bar_index == length - 1:  # 막대기 기호가 문자열의 마지막 자리에 도달한 경우
            bar_string = move_bar_left(bar_string)  # 왼쪽으로 이동
            bar_string = replace_vowel_on_right(bar_string)  # 오른쪽 모음 대체
            print(bar_string)
            if bar_string[bar_index - 1].lower() in 'bcdfghjklmnpqrstvwxyz':  # 막대기 기호 왼쪽 문자가 자음인 경우
                bar_string = replace_consonant_on_left(bar_string)  # 왼쪽 자음 대체
                print(bar_string)
                break  # 종료

        else:  # 막대기 기호가 문자열 내부에 있는 경우
            bar_string = move_bar_right(bar_string)  # 오른쪽으로 이동
            bar_string = replace_consonant_on_left(bar_string)  # 왼쪽 자음 대체
            print(bar_string)

    return bar_string

bar_string = input("막대 문자열을 입력하세요: ")
processed_bar_string = process_bar_string(bar_string)
print("최종 결과:", processed_bar_string)
