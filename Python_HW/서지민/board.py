ho = int(input())
ver = int(input())


print("+--+"+"--+"*(ver-1))
print("|  |"+"  |"*(ver-1))

if ho == 1:
    print("+--+"+"--+"*(ver-1))

else:
    i = 1
    while i < ho:
        print("+--+"+"--+"*(ver-1))
        print("|  |"+"  |"*(ver-1))
        i += 1
    print("+--+"+"--+"*(ver-1))
