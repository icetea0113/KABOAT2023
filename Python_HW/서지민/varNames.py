ah = ['a','e','i','o','u']

word = str(input().lower())
word = word.split()

real_type = ['bool', 'int', 'float', 'complex','str', 'list']
st_type = ['b', 'i', 'fp', 'cplx', 'str', 'ls']
delete = ['in', 'at', 'on', 'to' ,'of', 'by', 'the', 'a']
bin = []

if word[0] in real_type:
    num = real_type.index(word[0])
    bin.append(st_type[num])

for i in range(1, len(word)):
    if word[i] not in delete:
        bin.append(word[i])

middle_step = list(bin[1])
if len(middle_step) > 3 :
    middle_step = middle_step[0:3]
bin[1] = "".join(middle_step)

str = "_".join(bin)
print(str)