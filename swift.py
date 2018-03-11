import os
import glob
import numpy as np
import matplotlib.pyplot as plt
filelist=glob.glob("Data\\raw_*")
binned=[]
t90s=[]
area90s=[]
durations=[]
filenames=[]
if os.path.isfile("results.txt"):
    integneeded=False
else:
    integneeded=True
for file in filelist:
    integrable=False
    filename=file[9:-4] # Removes raw_ and .txt from filename to use as title of graph and to ensure simple file does not include phrase raw_
    filenametxt=file[9:]
    simplefile="Data\\simple_%s" %filenametxt
    if not os.path.isfile(simplefile): # Checks if simple file already exists; if it does there is no need to apply the stripping function before plotting
        print("%s has not yet been simplified. Stripping now..." %filename)
        with open(file,'r') as infile, open("Data\\temp.txt",'w') as outfile:
            for line in infile:
                try:
                    check1=line.split("\t")[0] # Assigning each element of data in a line to a variable, if possible
                    check2=line.split("\t")[1]
                    check3=line.split("\t")[2]
                    check4=line.split("\t")[3]
                    check5=line.split("\t")[4]
                    check6=line.split("\t")[5]
                except IndexError: # If there aren't enough columns to split line into 6, it is an unwanted line e.g. line 1 "READ TERR 1 2"
                    pass
                try:
                    if float(check1) and float(check2) and float(check3) and float(check4) and float(check5) and float(check6): # If every element in the row can be converted to float then it is valid data
                        outfile.write(line)
                except ValueError:
                    pass
                if "! gamma panel" in line:
                    break # Stops writing new lines once this line is reached in the original, to filter out the photon indices data
        with open("Data\\temp.txt",'r') as infile, open("Data\\temp2.txt",'w') as outfile:
            for line in infile:
                column1,column2,column3,column4,column5,column6=line.split("\t")
                outfile.write("%s\t%s\n" %(column1,column4))
        os.remove("Data\\temp.txt")
        with open("Data\\temp2.txt",'r') as infile, open (simplefile,'w'):
            data=[]
            for line in infile:
                line=line.split("\t")
                data.append(line)
            sortcol=sorted(data,key=lambda data_entry: float(data_entry[0]))
            np.savetxt(simplefile,sortcol,fmt="%s",delimiter="\t",newline="\r") # Might need to change newline parameter depending on OS
        os.remove("Data\\temp2.txt")
    with open(simplefile) as filecheck:
        nolines=sum(1 for line in filecheck)
    if nolines>4:  # If there are only 2 lines of data (and one blank line) in the results file we can't use it
        integrable=True
        if not os.path.isfile("Graphs\\%s.png" %filename):
            x,y=np.loadtxt(simplefile,delimiter="\t",unpack=True)
            plt.plot(x,y,label="Light Curve")
            plt.yscale('log',basey=10)
            plt.xscale('log',basex=10)
            plt.xlabel("Time since BAT trigger (s)")
            plt.ylabel("Flux Density (Jy @ 10keV)")
            plt.legend()
            plt.title("Swift Light Curve\n%s" %filename)
            plt.savefig("Graphs\\%s.png" %filename)
            plt.close()
            print("A graph has been plotted for %s" %filename)
    else:
        binned.append(filename)
    if integrable and integneeded:
        ix,iy=np.loadtxt(simplefile,delimiter="\t",unpack=True) # Renamed x and y to ensure the imported x and y in integrate.py are the correct ones
        if float(ix[0])<=0:
            bit=ix[0]
            ix=ix+1
            ix=ix-bit
        lx=np.log10(ix)
        ly=np.log10(iy)
        interpolate=True
        a=0
        while interpolate:
            n=len(lx)
            if a==n-1:
                interpolate=False
            elif lx[a]<(lx[a+1]-0.01):
                b=(lx[a]+lx[a+1])/2
                c=(ly[a]+ly[a+1])/2
                lx=np.insert(lx,a+1,b)
                ly=np.insert(ly,a+1,c)
            else:
                a=a+1
        x=10**lx
        y=10**ly
        print("Calculating area90 and t90 for GRB %s" %filename)
        totalflux=np.trapz(y,x)
        integrate=True
        n=1
        while integrate:
            q=(np.trapz(y[:n],x[:n]))
            w=(totalflux/100)*5
            if q>w:
                k=x[n-1]
                integrate=False
            else:
                n=n+1
        integrate=True
        a=len(x)
        while integrate:
            d=(np.trapz(y[:a],x[:a]))
            f=(totalflux/100)*95
            if d<f:
                l=x[a]
                integrate=False
            else:
                a=a-1
        t90=l-k
        listx=x.tolist()
        indexk=listx.index(k)
        indexl=listx.index(l)
        area90=np.trapz(y[indexk:indexl],x[indexk:indexl])
        t_first=x[0]
        t_last=x[-1]
        duration=t_last-t_first
        t90s.append(t90)
        area90s.append(area90)
        durations.append(duration)
        filenames.append(filename)
if integneeded:
    with open("results.txt",'w') as outfile:
        for index in range(len(t90s)):
            outfile.write(str(t90s[index])+"\t"+str(area90s[index])+"\t"+str(durations[index])+"\t"+str(filenames[index])+"\n")
else:
    print("The results have already been calculated")
t90,area90,duration,filename=np.loadtxt("results.txt",delimiter="\t",unpack=True) # Plots a graph of t90 against 90% integrated area under the curve for all of the unique GRB results in results.txt
x=t90
y=area90
plt.scatter(x,y)
plt.xscale('log',basex=10)
plt.yscale('log',basey=10)
plt.xlabel("t$_{90}$ (s)")
plt.ylabel("90% Integrated Flux (Jy)")
plt.title("GRB Populations")
plt.show()
if not os.path.isfile("Flux vs t90.pdf"):
    print("A results graph has been plotted")
else:
    print("The results have already been plotted")
print("The number of input files was %d" %len(filelist))
print("The number of files which did not contain enough data was %d" %len(binned))
if not len(binned)==0:
    print("The files which did not contain enough data were: ")
    print(binned)