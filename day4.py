a = input("enter the Passcode:")
up = 0
sm = 0
sp = 0
dg = 0

if(len(a)>7):
    for i in a:
        if (i.isupper):
            up = up +1
        elif(i.islower):
            sm = sm+1
        elif(i.isalnum):
            sp = sp+1
        elif(i.isdigit):
             dg= dg+1
        else:
            print("weak")
else:
    print("need more strong")                       