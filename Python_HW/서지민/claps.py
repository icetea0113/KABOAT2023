a, b = map(int, input().split())
count = 0
soo = []
for i in range(a, b+1):
    if i < 10:
        soo.append(i)
    else :
        if i % 10 == 0:
            soo.append(i//10)
        else:
            soo.append(i//10)
            soo.append(i%10)
num1 = soo.count(3)
num2 = soo.count(6)
num3 = soo.count(9)
count = num1 + num2 + num3

print(count)