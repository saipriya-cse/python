# ctr=0
# while ctr<5:
#     print(ctr)
#     ctr+=1 #pgm1

# for x in range(3):
#     print(x)#pgm2

# for x in range(2,10,2):
#     print(x)#pgm3
# for x in 'rama':
#     if x=='m':
#         break
#     else:
#         print(x)#pgm4

# for x in 'rama':
#     if x=='m':
#        pass
#     else:
#         print(x)#pgm5

correct_password="admin123"
for attempt in range(1,4):
    password=input("enter your password:")
    if password==correct_password:
    print("login successful")
    break
else:
     print("wwrong password")
     if attempt==3:
     print("account locked")
