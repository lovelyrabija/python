import matplotlib.pyplot as plt
import numpy as np

overs = np.arange(1,21)
scores =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
plt.bar(overs,scores,color="blue")
plt.xlabel("number of overs")
plt.ylabel("scored")
plt.xticks(overs)
plt.grid(axis="y", linestyle ="--", alpha=0.9)
plt.show()