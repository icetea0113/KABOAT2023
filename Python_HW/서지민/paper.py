x = []
y = []
while True:
    try:
        boom = list(map(int, input().split()))

        for i in range(0, len(boom), 2):
            inp_x = int(boom[i])
            inp_y = int(boom[i + 1])
            x.append(inp_x)
            y.append(inp_y)
    except:
        break

def make_result_x(x):
    result_x = []

    if x[0] < x[2]:
        num_x = x[1] - x[2]
        result_x.append(x[2]) #min_x
        result_x.append(x[1]) #max_x

    elif x[0] > x[2]:
        num_x = x[3] - x[0]
        result_x.append(x[0]) #min_x
        result_x.append(x[3]) #max_x

    elif x[0] == x[2]:
        if x[1] > x[3]:
            num_x = x[3] - x[0]
            result_x.append(x[0])
            result_x.append(x[3])

        elif x[1] < x[3]:
            num_x = x[0] - x[3]
            result_x.append(x[0])
            result_x.append(x[1])
        else:
            num_x = x[1] - x[0]
            result_x.append(x[0])
            result_x.append(x[1])
    return result_x , num_x

def make_result_y(y):
    result_y = []
    if y[1] < y[3]:
        if y[0] < y[2]:
            num_y = y[1] - y[2]
            result_y.append(y[2]) #min_y
            result_y.append(y[1]) #max_y
        elif y[0] > y[2]:
            num_y = y[1] - y[0]
            result_y.append(y[0]) #min_y
            result_y.append(y[1]) #max_y

    elif y[1] > y[3]:
        if y[0] > y[2]:
            num_y = y[3] - y[0]
            result_y.append(y[0]) #min_y
            result_y.append(y[3]) #max_y
        elif y[0] < y[2]:
            num_y = y[3] - y[2]
            result_y.append(y[2]) #min_y
            result_y.append(y[3]) #max_y

    elif y[0] == y[2]:
        if y[1] > y[3]:
            num_y = y[3] - y[0]
            result_y.append(y[0])
            result_y.append(y[3])

        elif y[1] < y[3]:
            num_y = y[0] - y[3]
            result_y.append(y[0])
            result_y.append(y[1])
        else:
            num_y = y[1] - y[0]
            result_y.append(y[0])
            result_y.append(y[1])
    #y 범위 구분 완료
    return result_y ,num_y

if len(x) == 4 : #네모가 2개일 경우
    result_x, num_x = make_result_x(x)
    result_y, num_y = make_result_y(y)

elif len(x) == 6:
    result_x, num_x = make_result_x(x)
    result_y, num_y = make_result_y(y)

    x[0] = result_x[0]
    x[1] = result_x[1]
    del x[2]
    del x[2]
    y[0] = result_y[0]
    y[1] = result_y[1]
    del y[2]
    del y[2]

    result_x, num_x = make_result_x(x)
    result_y, num_y = make_result_y(y)

jjin_result = num_x * num_y
print(jjin_result)

            