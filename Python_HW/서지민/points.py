x_1, y_1, x_2, y_2 = map(int, input().split())
dot = []
do_x = []
do_y = []
count = 0
while True:
    try:
        A, B= map(int,input().split())
        do_x.append(A)
        do_y.append(B)
    except:
        break

for i in range(0, len(do_x)):
    if (x_1 <=do_x[i] <= x_2) and (y_1 <= do_y[i] <= y_2):
        count += 1

print(count)