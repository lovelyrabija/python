import calendar 
from datetime import datetime
a = input("Enter your date of birth:")
b = input("Enter your current date:")

a1=datetime.strptime(a,"%Y-%m-%d")
b1=datetime.strptime(b,"%Y-%m-%d")

print(f"Harish has lived {b1-a1} so far")
