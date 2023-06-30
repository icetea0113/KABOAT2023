word = str(input())
sp = list(word)
ah = ['a','e','i','o','u','|']
sp_c = list.copy(sp)
str = "".join(sp)
print(str)
if sp[0] == '|':
    i = 1
    while i < len(sp):
        if sp[i] not in ah:
            sp[i] = '*'
        sp[i-1], sp[i] = sp[i], sp[i-1]
        i += 1
        str = "".join(sp)
        print(str)
        # print("가보자")
    j=i-2
    while j > -1:
        # print(j)
        if sp[j] in ah :
            sp[j] = '#'
        elif sp[j] == '*':
            sp[j] = sp_c[j+1]
        sp[j], sp[j+1] = sp[j+1], sp[j]
        j -= 1
        str = "".join(sp)
        print(str)
    
elif sp[-1] == '|':
    i = len(sp) - 1
    while i > 0 :
        if sp[i-1] in ah:
            sp[i-1] = '#'
        sp[i-1], sp[i] = sp[i], sp[i-1]
        i -= 1
        str = "".join(sp)
        print(str)
    j = i+1
    while j < len(sp):
        if sp[j] not in ah and not (sp[j] == '#'):
            sp[j] = '*'
        elif sp[j] == '#':
            sp[j] = sp_c[j-1]
        sp[j-1], sp[j] = sp[j], sp[j-1]
        j += 1
        str = "".join(sp)
        print(str)
