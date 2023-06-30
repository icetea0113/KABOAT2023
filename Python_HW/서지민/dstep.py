num = int(input())

def sq():
    print("+--+")
    print("|ㅤ|")

if num == 1 :
    sq()
    print("+--+")

else:
    i = int(2)
    sq()
    while i <= num:
        print("+--+"+("--+"*(i-1)))
        print("|ㅤ|"+("ㅤ|"*(i-1)))
        i +=1
    print("+--+"+("--+"*(i-2)))
