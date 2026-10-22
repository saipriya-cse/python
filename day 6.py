n=4
for i in range(n):
    print(" "*(n-i)+"* "*i)

n=4
for i in range(n,0,-1):
    print(" "*(n-i)+"* "*i)

n=4
for i in range(n):
    for j in range(n):
        print( "* ",end='')
    print()
