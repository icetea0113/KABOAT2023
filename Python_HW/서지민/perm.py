from itertools import combinations, permutations

sti = str(input())
num = int(input())
num = num -1

word = sti.split() #띄어쓰기 기준으로 나눠둠

for i in range(0, len(word)):
    if word[i] == 'three':
        word[i] = 3
    elif word[i] == 'two':
        word[i] = 2
    elif word[i] == 'one':
        word[i] = 1
    elif word[i] == 'zero':
        word[i] = 0   
word.sort()

perm = list(permutations(word, len(word)))
result = list(perm[num])

for i in range(0, len(result)):
    if result[i] == 3:
        result[i] = 'three'
    elif result[i] == 2:
        result[i] = 'two'
    elif result[i] == 1:
        result[i] = 'one'
    elif result[i] == 0:
        result[i] = 'zero'

str = " ".join(result)
print(str)