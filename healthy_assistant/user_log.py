user_name=input("enter your name:")
user_password=input("enter your password:")
inbuilt_user_name="admin"
inbuilt_user_password="admin123"

if user_name == inbuilt_user_name and user_password == inbuilt_user_password:
    print("login successful!")
else:
    print("invalid username or password.")