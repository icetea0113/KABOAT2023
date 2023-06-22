def repeat(a,b, w):
    s1 = a+b
    s1= s1*w + a

    print(s1)






h = int(input())
w = int(input())
while(h>0):
    repeat('+','-', w)
    h -=1

repeat('+','-', w)