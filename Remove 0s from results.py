import os
os.rename("results.txt","results0s.txt")
with open("results0s.txt") as infile, open("results.txt",'w') as outfile:
    for line in infile:
        col1=line.split("\t")[0]
        col2=line.split("\t")[1]
        col3=line.split("\t")[2]
        col4=line.split("\t")[3]
        while int(col4[0])==0:
            col4=col4[1:]
        outfile.write("%s\t%s\t%s\t%s" %(col1,col2,col3,col4))
os.remove("results0s.txt")