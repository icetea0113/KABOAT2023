a1 = int(input())
a2 = int(input())
a3 = int(input())
a_list = [a1,a2,a3]
sorted_number = sorted(a_list)

if sorted_number[2] < sorted_number[0]+sorted_number[1]:
    print("yes")
else:
    print("No")
