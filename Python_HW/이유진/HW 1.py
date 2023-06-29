side = list(map(int, input().split())) 

max_v = max(side)

side.remove(max_v)

nomax = side

if (sum(nomax)-max_v) > 0:
    sum_sq_nomax = sum([x**2 for x in nomax])

    if sum_sq_nomax - max_v**2 > 0:
        print("AC")
    elif sum_sq_nomax - max_v**2 == 0:
        print("IR")
    else:
        print("OB")

else:
    print("No")
