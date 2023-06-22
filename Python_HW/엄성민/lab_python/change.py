lstNumbers = []

def change_cal(money,i):
    if(i==len(lstNumbers)-1):
        mone = money//lstNumbers[i]
        print(mone)
        if(money%lstNumbers[i] !=0):
            print("가진 동전으로 거스름돈 다 못준다")
    else:
        mone =  money//lstNumbers[i]
        print(mone, " ", end="")    
        exchange_now = money-mone*lstNumbers[i]
        i +=1
        change_cal(exchange_now,i)

if __name__ == "__main__":
    strName = input()
    lstNumbers = [int (num) for num in strName.split()]
    
    intNum = int(input())
    
    change_cal(intNum,0)