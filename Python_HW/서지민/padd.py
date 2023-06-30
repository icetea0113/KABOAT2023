f = list(map(int, input().split()))
g = list(map(int, input().split()))
result = []
good = max(len(f), len(g))

if len(f) < good :
    num = good - len(f)
    for i in range(0, num):
        f.insert(0, 0)

elif len(g) < good :
    num = good - len(g)
    for i in range(0, num):
        g.insert(0, 0)

for i in range(0, good):
    result.append(f[i] + g[i])

print(' '.join(str(_) for _ in result))