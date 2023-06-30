#양수 3개를 입력받아 삼각형의 종류를 분석하라
import math

a = int(input())
b = int(input())
c = int(input())

tri = []
tri.append(a)
tri.append(b)
tri.append(c)

max_num = max(tri)
tri.remove(max(tri))
if max_num >= tri[0] + tri[1]:
    print("NO")
else :
    if (tri[0])**2 + (tri[1])**2 == (max_num)**2 :
        print("RI")
    elif (tri[0])**2 + (tri[1])**2 < (max_num)**2 :
        print("OB")
    else:
        print("AC")
