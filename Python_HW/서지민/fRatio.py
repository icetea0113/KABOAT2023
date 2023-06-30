count={}
lists = list(str(input()).lower().split(' '))
word =[]
real = ['1','2','3','4','5','6','7','8','9','0']
for i in range (0, len(lists)):
    words = list(lists[i])
    for j in range(0, len(words)):
        if words[j] not in real:
            word.append(words[j])

for i in word:
    try: count[i] += 1
    except: count[i]=1

num = max(count.values())

result = num/len(word)
print("{:.2f}".format(result))