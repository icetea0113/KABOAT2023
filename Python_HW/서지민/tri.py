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
    print("No")
else:
    print("Yes")