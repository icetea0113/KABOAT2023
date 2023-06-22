class squar:
    def __init__(self, p):
        self.x1 = p[0]
        self.x2 = p[2]
        self.y1 = p[1]
        self.y2 = p[3]
    
    def count_point(self,p2):
        if(p2[0] >= self.x1 and p2[0] <= self.x2 and p2[1] >= self.y1 and p2[1] <= self.y2):
            return 1
        else:
            return 0


if __name__ == "__main__":
    strName1 = input()
    lstNumbers = [int (num) for num in strName1.split()]

    lstNumbers2 = []
    while(1):
        strName2 = input()
        if strName2 == ' ':
            break
        lstNumbers2.append([int (num) for num in strName2.split()])
    squar_count = squar(lstNumbers)
    sum =0
    for i in range(0,len(lstNumbers2)):
        sum += squar_count.count_point(lstNumbers2[i])    
    print(sum)
