#입력된 sentence에서 대체시키는 함수
def replace_vowels_with_dash(sentence: str) -> str:
    vowels = ['a', 'e', 'i', 'o', 'u']
    replaced_sentence = ''.join(['-' if word.lower() in vowels else word for word in sentence])
    return replaced_sentence
    #입력 받은 문자열을 일단 다 소문자로 바꾸고, 변환된 소문자에 모음 리스트에 있는지 확인
    #포함되어 있으면 -로 대체, 포함되어 있지 않으면 그대로 유지
    #변환된 문자열들을 list 집합으로 생성
    #''.join() 함수는 문자열로 결합시키는 함수임
    #retrun을 사용해서 변환된 문자열을 replaced_sentence 변수에 저장 및 반환 
    #word는 sentence에서 문자열 하나씩 대표하는 변수로 사용됨
    #함수가 실행될 때 sentence에서 문자 하나씩 읽어들이는 반목분 실행하는데 이때 문자 하나씩 읽으면서 word에 할당?되는거
    
def replace_consonants_with_star(sentence: str) -> str:
    vowels = ['a', 'e', 'i', 'o', 'u']
    replaced_sentence = ''.join(['*' if word.lower() not in vowels and word.isalpha() else word for word in sentence])
    return replaced_sentence

# 문장 입력 받기
option = input("v나 c 중에 하나 선택: ")
input_sentence = input("문장을 입력하세요: ")

# 대체된 결과 출력
if option == 'v':
    result = replace_vowels_with_dash(input_sentence)
elif option == 'c':
    result = replace_consonants_with_star(input_sentence)
else:
    result = "잘못된 옵션을 선택하셨습니다."

print(result)