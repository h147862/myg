import numpy as np
import matplotlib.pyplot as plt
import csv


num_of_child = np.zeros(50)
temp = []
resnum  = 7

with open('result/v4nsga2_out_' + str(resnum) +'.csv' , 'rb') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        temp.append(row[3])


for index,number in enumerate(temp):
    num_of_child[int(index)%50] += int(number)



# num_of_child = num_of_child / (len(temp)/50)
plt.bar(range(50),num_of_child)
# plt.hist(range(50),num_of_child, bins='auto')
# plt.title("Histogram with 'auto' bins")
plt.show()