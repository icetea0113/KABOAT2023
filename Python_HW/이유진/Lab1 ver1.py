a = int(input())
b = int(input())
c = int(input())

side = [a, b, c]
max = max(side)
side.remove(max)

list = side

if (sum(list)-max) > 0:
    print("True")
else:
    print("No")
