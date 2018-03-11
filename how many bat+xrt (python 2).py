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
        else:
            if not filenumber in xrtonly:            
                xrtonly.append(filenumber)
    else:
        if os.path.isfile(batfile):
            if not filenumber in batonly:
                batonly.append(filenumber)
        else:
            if not filenumber in neither:
                neither.append(filenumber)
            print("Something's gone horribly wrong")
with open("how many bat+xrt.txt",'w') as outfile:
    print>>outfile,("The number of GRBs was %d" %len(uniquegrbs))
    print>>outfile,("The number of files containing data from both xrt and bat was %d" %len(both))
    print>>outfile,("The number of files containing data from just xrt was %d" %len(xrtonly))
    print>>outfile,("The files which only contained data from xrt were:")
    print>>outfile,(xrtonly)
    print>>outfile,("The number of files containing data from just bat was %d" %len(batonly))
    print>>outfile,("The files which only contained data from bat were:")
    print>>outfile,(batonly)
    if not len(neither)==0:
        print>>outfile,("The number of horrible mistakes was %d" %len(neither))
