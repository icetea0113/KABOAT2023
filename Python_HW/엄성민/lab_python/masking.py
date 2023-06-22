input_str = input()  # 사용자 입력 받기
input_list = input_str.split()  # 공백으로 입력 문자열 분리하여 리스트로 저장
input_sentence = input()

string_list = []

volv = "aeiouAEIOU"
volv2 = ".!?"

print(input_list[1])

for c in input_sentence:
    if input_list[0] == 'v':
        if c in volv:
            if(input_list[1]=='-'):
                string_list.append('-')
            else:
                string_list.append('*')
        else:
            string_list.append(c)
    else:
        if c in volv or c in volv2 or c == ' ':
            string_list.append(c)    
        else:
            if(input_list[1]=='-'):
                string_list.append('-')
            else:
                string_list.append('*')
result_string = ' '.join(string_list)
print(result_string)  # "apple banana cherry" 출력
## 일단 string으로 변환 해줘야하고, 확인하려면 f10으로 해야하는데 어딨지?