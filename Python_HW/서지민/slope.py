import sys
x = []
y = []

for line in sys.stdin.readlines():
    if line == "\n": #\n 개행라인
        break
    else:
        line = line.rstrip()
        boom = line.split()

        for i in range(0, len(boom), 2):
            inp_x = float(boom[i])
            inp_y = float(boom[i + 1])
            x.append(inp_x)
            y.append(inp_y)

re_x = 0
re_y = 0

for i in range(len(x)-1):
    re_x = x[i] - x[i+1]
    re_y = y[i] - y[i+1]

if re_x != 0:
    result = re_y/re_x
    print("{:.2f}".format(result))

else:
    result = re_y
    print("({:.2f})".format(result))
