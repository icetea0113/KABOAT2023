# 숫자열을 두 번 입력 받습니다.
num1 = input("첫 번째 숫자열을 입력하세요: ")
num2 = input("두 번째 숫자열을 입력하세요: ")

# 숫자열을 공백을 기준으로 분리합니다.
num1_list = num1.split()
num2_list = num2.split()

# 두 숫자열의 길이를 비교하여 짧은 숫자열에 0을 추가합니다.
if len(num1_list) < len(num2_list):
    num1_list = ['0'] * (len(num2_list) - len(num1_list)) + num1_list
elif len(num1_list) > len(num2_list):
    num2_list = ['0'] * (len(num1_list) - len(num2_list)) + num2_list

# 숫자열의 각 원소를 정수로 변환하고, 같은 위치에 있는 숫자끼리 더합니다.
result_list = []
for x, y in zip(num1_list, num2_list):
    if x.startswith('-'):
        result_list.append(str(int(y)-int(x)))
    elif y.startswith('-'):
        result_list.append(str(int(x)-int(y)))
    elif x.startswith('-') and y.startswith('-'):
        result_list.append('-', str(int(x)+int(y)))
    else:
        result_list.append(str(int(x)+int(y)))
        
result_list = [str(int(x) + int(y)) for x, y in zip(num1_list, num2_list)]

# 결과를 공백을 통해 구분하여 출력합니다.
result = ' '.join(result_list)
print("덧셈 결과:", result)
