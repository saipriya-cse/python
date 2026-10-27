# n=int(input("enter a number:"))
# sum=0
# for i in range(1,n):
#     if n%i==0:
#         sum=sum+i
#     if sum==n:
#         print("perfect number")
#     else:
#         print("not a perfect number") #pgm1



# n=int(input("enter a number"))
# rev=0
# while n>0:
#     dig=n%10
#     rev=rev*10+dig
#     n=n//10
# print("the reverse number is",rev)#pgm reverse number

# n=int(input("enter a number"))
# while n!=1 and n!=4:
#     total=0
#     while n>0:
#         digit=n%10
#         total+=digit**2
#         n//10
#     n=total
# if n==1:
#     print("happy number")
# else:
#     print("not happy number")#happy number

# n=int(input("enter a number"))
# while n!=1 and n!=4:
#     total=0
#     while n>0:
#         digit=n%10
#         total+=digit**2
#         n//=10
#     n=total
# if n==1:
#     print("happy number")
# else:
#     print("not happy number")#happy number



# n=int(input("enter a number:"))
# rev=0
# while n>0:
#     digit=n%10
#     rev=rev*10+digit
#     n=n//10
# print("the reversed number is",rev)



# n=int(input("enter a number:"))
# rev=0
# while n>0:
#     digit=n%10
#     rev=rev*10+digit
#     n=n//10
# print("the reverse number is",rev)

#happy number
# n=int(input("enter a number:"))
# while n!=1 and n!=4:
#     total=0
#     digit=n%10
#     total+=digit**2
#     n=n//10
#     n=total
# if n==1:
#     print("happy number")
# else:
#     print("not happy number")

#armstrong


# n=int(input("enter a number:"))
# temp=n
# digit=len(str(n))
# total=0
# while temp>0:
#     digit=temp%10
#     total+=digit**digit
#     temp//=10
# if total==n:
#     print("armstrong number")
# else:
#     print("not armstrong number")

#perfrct number

# n=int(input("enter a number:"))
# total=0
# for i in range(1,n):
#     if n%i==0:
#         total+=i
#     if total==n:
#         print("perfect square")
#     else:
#         print("not perfect square")

#neon number
# n=int(input("enter a number:"))
# square=n*n
# total=0
# digit=square%10
# total+=digit
# square//=10
# if sum==n:
#     print("neon number")
# else:
#     print("not neon number")

#perfect number

n=int(input("enter a number:"))
total=0
for i in range(1,n):
    if n%i==0:
        total+=i
if total==n:
    print("perfect number:")
else:
    print("not perfect number")



