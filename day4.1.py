import matplotlib.pyplot as plt
import numpy as np
overs = np.arange(1,21)
scores =[5,10,23,15,8,7,6,4,2,3,8,7,2,0,1,5,4,3,2,1]
plt.bar(overs,scores,color="blue")
plt.title("india's score over 20 overs(Bar Chart)")
plt.xlabel("over number")
plt.ylabel("runs scored")
plt.xticks(overs)
plt.grid(axis='y',linestyle='-')
plt.show()