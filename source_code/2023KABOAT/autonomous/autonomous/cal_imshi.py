gps = [(35.0695989, 128.5786773),(35.0692921,128.578877),(35.0693113, 128.5789217),(35.0696177, 128.5787222)]
a = 0
b = 0

for i in gps:
    a += i[0]
    b += i[1]

print(a/4)
print(b/4)