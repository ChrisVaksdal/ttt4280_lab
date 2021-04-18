import csv
import matplotlib as plt
from pylab import *;plot();show()

header=[]
data=[]
data_2=[]
filename="bandpass1.csv"

with open(filename) as csvfile:
    csvreader=csv.reader(csvfile)

    header =next(csvreader)

    for datapoint in csvreader:

        values=[float(value) for value in datapoint]

        data.append(values)

print(header)
print(data[21])

time=[p[0] for p in data]
ch1=[p[1] for p in data]
ch2=[p[2] for p in data]
#math1=[p[3] for p in data]



plt.semilogx(time,ch2)

filename="bandpass2.csv"

with open(filename) as csvfile:
    csvreader=csv.reader(csvfile)

    header =next(csvreader)

    for datapoint in csvreader:

        values=[float(value) for value in datapoint]

        data_2.append(values)

print(header)
print(data[21])

time=[p[0] for p in data]
ch1=[p[2] for p in data_2]
ch2=[p[2] for p in data]
#plt.semilogx(time,ch1)
plt.subplot(2, 1, 1)
plt.semilogx(time,ch2)
plt.title("Bandpass 1")
plt.xlabel(header[0])
plt.ylabel(" [dB]")
plt.legend(header[1:],loc="lower right")

plt.subplot(2, 1, 2)
plt.semilogx(time,ch1)
plt.xlabel(header[0])
plt.ylabel(" [dB]")
plt.title("Bandpass 2")
plt.legend(header[1:],loc="lower right")
plt.tight_layout(pad=2.0)
plt.savefig('filename.png', dpi=600)
plt.show()