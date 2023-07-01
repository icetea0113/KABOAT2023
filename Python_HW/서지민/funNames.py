words = str(input())
words = words.split()

if 'a' in words:
    words.remove('a')
if 'the' in words:
    words.remove('the')

ah = ['a','e','i','o','u']
word = list(words[0].lower())

bin = []
for j in range (0,len(word)):
    if word[j] not in ah:
        bin.append(word[j])
    j += 1
words[0] = "".join(bin)

i = 1
while i <= len(words)-1:
    word = list(words[i].lower())
    word[0] = word[0].upper()
    words[i] = "".join(word)
    i += 1

print("".join(words))
