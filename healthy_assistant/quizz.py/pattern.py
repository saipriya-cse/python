n=int(input())
for i in range(1,n+1):
    for j in range(1,n+1):
        ch=" "
        if i==j or i+j==n+1:
            ch="*"
        elif i==1 or i==n:
            ch="-"
        elif j==1 or j==n:
            ch="|"
        print(ch,end=" ")
    print()
