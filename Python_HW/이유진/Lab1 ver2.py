side = list(map(int, input().split(','))) 
#input 된 값을 , 기준으로 쪼개서 원소로 인식
#만약 공백으로 할거면 그냥 ''없이 ()로 쓰면 됨

max_v = max(side)

side.remove(max_v)
nomax = side
# side = nomax 사용 이유.

if (sum(nomax)-max_v) > 0:
    print("True")
else:
    print("No")