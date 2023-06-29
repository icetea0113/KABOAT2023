# 문자열 입력 받기
input_str = input()

# 바 기호와 단어 분리
if input_str[0] == '|':
    bar_symbol = '|'
    word = input_str[1:]
else:
    bar_symbol = '|'
    word = input_str[:-1]

# 오른쪽 스캔
for i in range(len(word)):
    if bar_symbol == '|':
        if word[i].lower() in 'aeiou':
            print('#', end='')
        else:
            print(word[i], end='')
    else:
        print(word[i], end='')

# 왼쪽 스캔
for i in range(len(word) - 1, -1, -1):
    if bar_symbol == '|':
        print(word[i], end='')
    else:
        if word[i].lower() in 'aeiou':
            print('#', end='')
        else:
            print(word[i], end='')

print()
