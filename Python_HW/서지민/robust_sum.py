import sys

for line in sys.stdin.readlines():
    if line == "\n": #\n 개행라인
        break
    else:
        line = line.rstrip()
        boom = line.split()
        num = 0 
        count = True

        for i in range(0, len(boom)):
            if str.isdigit(boom[i]):
                num += int(boom[i])
            else :
                count = False
                break
            
        if count == True:
            print(num)
        else : 
            print("({})".format(num))
            