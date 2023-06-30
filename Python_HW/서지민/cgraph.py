ch = str(input())
soo = []
soo = list(map(int, input().split()))
num = len(soo)

if ch == '#':
    i = 0
    j = 1
    while num > 0:
        while j <= soo[i]:
            print(" "*i+"#"*num)
            j += 1
        j = 1
        num -= 1
        i += 1

elif ch == '$':
    reversed_soo = soo[::-1]
    print(reversed_soo)
    i = 0
    j = 1
    while num > 0:
        while j <= reversed_soo[i]:
            print(" "*num+"$"*(i+1))
            j += 1
        j = 1
        num -= 1
        i += 1


