mon = list(map(int, input().split()))
money = int(input())

na = [] 
for i in range (0, len(mon)):
    na.append(int(money//mon[i]))
    money = money % mon[i]

print(' '.join(str(_) for _ in na))