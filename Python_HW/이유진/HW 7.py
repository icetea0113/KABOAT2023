import itertools

def get_nth_permutation(words, n):
    # 단어 시퀀스의 순열을 생성합니다.
    permutations = list(itertools.permutations(words))
    
    # n번째 순열을 가져옵니다.
    nth_permutation = permutations[n - 1]
    
    return ' '.join(nth_permutation)

# 입력을 받습니다.
word_sequence = input().split()
n = int(input())

# n번째 순열을 계산합니다.
result = get_nth_permutation(word_sequence, n)

# 결과를 출력합니다.
print(result)
