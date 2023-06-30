
weight = 0
sti = str(input())
word = sti.split() #띄어쓰기 기준으로 나눠둠

sp = list(sti) #공백까지 그냥 리스트에 삭다 집어 넣음 ㅎ

bin = [] 
ah = {'a': 0,'e': 0,'i': 0,'o': 0,'u': 0}

rest = [' ', '.' ,',', '?', '!']

for i in range(0, len(sp)):
    if sp[i] not in rest:
        bin.append(sp[i])

for i in range(0, len(bin)):
    if bin[i] in ah.keys() :
        ah[bin[i]] = ah[bin[i]] + 1 
        weight += 2
    elif bin[i] == 'w' or bin[i] =='y':
        weight += 1.5
    else :
        weight += 1

c = max(ah.values())*2

print(round((c/weight),3))