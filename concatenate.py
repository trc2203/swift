import os
import glob
filelist=glob.glob("Data\\Files backup\\00*.dat")
for file in filelist:
    filenumber=file[18:26]
    xrtfile="Data\\Files backup\\%s_xrt.dat" %filenumber
    batfile="Data\\Files backup\\%s_bat.dat" %filenumber
    if os.path.isfile(xrtfile):
        if os.path.isfile(batfile):
            with open(xrtfile) as infile1, open(batfile) as infile2, open("Data\\raw_%s.txt" %filenumber, 'w') as outfile:
                for line in infile1:
                    outfile.write(line)
                for line in infile2:
                    outfile.write(line)
            print("%s bat and xrt files have been concatenated" %filenumber)