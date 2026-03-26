from datetime import datetime
a = input("enter the YYYY-MM-DD:")
b = input("enter the YYYY-MM-DD:")
a1 = datetime.strptime(a,"%Y-%m-%d")
b1 = datetime.strptime(b,"%Y-%m-%d")
print(b1-a1)