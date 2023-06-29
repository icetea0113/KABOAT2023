# 문자열 입력 받기
input_string = input()

# 모든 문자 소문자로 변환
input_string = input_string.lower()

# 단어들 분리하기
words = input_string.split()

# 첫 어절이 변수 유형인지 확인하고 변환하기
variable_types = {'bool': 'b', 'int': 'i', 'float': 'fp', 'complex': 'cplx', 'str': 'str', 'list': 'ls'}
if words[0] in variable_types:
    words[0] = variable_types[words[0]]

# 'in', 'at', 'on', 'to', 'of', 'by', 'the', 'a' 제거하기
# 전치사 자체를 제거하는 함수는 모르겠음 ㅠ
trivial_words = ['in', 'at', 'on', 'to', 'of', 'by', 'the', 'a']
words = [word for word in words if word not in trivial_words]

# 공백 '_'로 바꾸기
output_string = '_'.join(words)

# 결과 출력
print(output_string)
