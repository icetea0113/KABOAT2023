def find_indexes(l1, l2):
    indexes = []
    l1_size = len(l1)
    l2_size = len(l2)
    
    if(l1_size>l2_size):
        list_tem = l1
        l1 = l2
        l2 = list_tem
        l1_size = len(l1)
        l2_size = len(l2)
    
    l1.reverse()
    l2.reverse()
    for i in range(0,l1_size):        
        indexes.append(l1[i]+l2[i])#i번째에 값이 있는지 확인하는거 추가
    for i in range(l1_size,l2_size):
        indexes.append(l2[i])
    indexes.reverse()
    for i in indexes:
        print(i," ", end="")

if __name__ == "__main__":
    strName1 = input()
    lstNumbers = [int (num) for num in strName1.split()]
    
    strName2 = input()
    lstNumbers2 = [int (num) for num in strName2.split()]
    
    find_indexes(lstNumbers,lstNumbers2)
    
    