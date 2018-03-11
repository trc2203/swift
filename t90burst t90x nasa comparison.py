import matplotlib.pyplot as plt
import numpy as np
import os
import glob
filelist=glob.glob("Data\\Files backup\\00*.dat")
both=[]
xrtonly=[]
batonly=[]
neither=[]
uniquegrbs=[]
for file in filelist:
    filenumber=file[18:26]
    if not filenumber in uniquegrbs:
        uniquegrbs.append(filenumber)
    xrtfile="Data\\Files backup\\%s_xrt.dat" %filenumber
    batfile="Data\\Files backup\\%s_bat.dat" %filenumber
    if os.path.isfile(xrtfile):
        if os.path.isfile(batfile):
            if not filenumber in both:
                both.append(filenumber)
# t_burst data
TrNosburst=[]
t90sburst=[]
GRBNumbers=[]
TriggerNumbers=[]
Nasat90s=[]
t90s=[]
SwiftNotBurst=[]
BurstNotSwift=[]
SwiftAndBurst=[]
with open("t_burst\\results.txt") as infile1, open("t90scomparison.txt") as infile2:
    for line in infile1:
        TrNon=line.split("\t")[3]
        TrNo=TrNon[:-1]
        t90burst=line.split("\t")[0]
        TrNosburst.append(TrNo)
        t90sburst.append(t90burst)
    for line in infile2:
        GRBNo=line.split("\t")[0]
        TriggerNo=line.split("\t")[1]
        Nasat90=line.split("\t")[2]
        t90n=line.split("\t")[3]
        t90=t90n[:-1]
        GRBNumbers.append(GRBNo)
        TriggerNumbers.append(TriggerNo)
        Nasat90s.append(Nasat90)
        t90s.append(t90)
comparison=[[],[],[],[],[]] # GRB Number, Trigger Number, t90g, t90burst, t90x
for element in TriggerNumbers:
    comparison[0].append(element)
    i=TriggerNumbers.index(element)
    comparison[1].append(TriggerNumbers[i])
    comparison[2].append(Nasat90s[i])
    comparison[4].append(t90s[i])
    if element in TrNosburst:
        SwiftAndBurst.append(element)
    else:
        SwiftNotBurst.append(element)
for element in TrNosburst:
    if element in TriggerNumbers:
        j=TrNosburst.index(element)
        comparison[3].append(t90sburst[j])
    else:
        comparison[3].append("n/a")
        BurstNotSwift.append(element)
with open("t90 t_burst comparison.txt",'w') as outfile:
    for x in zip(*comparison):
        outfile.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(*x))
print("The total number of unique GRBs in the two data sets was %d" %len(SwiftAndBurst+SwiftNotBurst+BurstNotSwift))
print("The number of GRBs found in Swift data but not burst data was %d" %len(SwiftNotBurst))
print("The number of GRBs found in burst data but not Swift data was %d" %len(BurstNotSwift))
discarded=SwiftNotBurst+BurstNotSwift
print("The number of GRBs compared was %d which should be (almost) the same as %d" %(len(t90s),len(both)))
print("The number of GRBs that were discarded was %d" %len(discarded))
x=[]
y=[]
with open("t90 t_burst comparison.txt") as infile:
    for line in infile:
        try:
            check1=line.split("\t")[0] # Assigning each element of data in a line to a variable, if possible
            check2=line.split("\t")[1]
            check3=line.split("\t")[2]
            check4=line.split("\t")[3]
            check5=line.split("\t")[4]
        except IndexError: # If there aren't enough columns to split line into 6, it is an unwanted line e.g. line 1 "READ TERR 1 2"
            pass
        try:
            if float(check2) and float(check3) and float(check4) and float(check5): # If every element in the row can be converted to float then it is valid data
                x.append(check4)
                y.append(check5)
        except ValueError:
            pass
a=np.logspace(0,7,num=8)
b=a
plt.plot(a,b)
plt.scatter(x,y)
plt.xscale('log',basex=10)
plt.yscale('log',basey=10)
plt.xlabel("t$_{90 burst}$ (s)")
plt.ylabel("t$_{90X}$ (s)")
plt.title("t$_{90}$/t$_{90 burst}$ comparison")
plt.show()