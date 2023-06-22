def three_count(num):
    global total_sum
    str_num = str(num)
    for i in str_num:
        if(i == '3' or i =='6' or i =='9'):
            total_sum +=1

total_sum = 0

if __name__ == "__main__":
    strName = input()
    lstNumbers = [int (num) for num in strName.split()]
    for i in range(lstNumbers[0],lstNumbers[1]+1):
        three_count(i)
    print(total_sum)