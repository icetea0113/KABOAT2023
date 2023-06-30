ah = ['a','e','i','o','u']

cha, mas  = map(str, input().split())
word = str(input())
st = list(word)

for i in range (0, len(st)-1):
    if cha == 'v':
        if st[i] in ah :
            st[i] = mas
    else:
        if st[i] not in ah:
            st[i] = mas

str = "".join(st)
print(str)