import numpy as np
h = [] # h is the array for t90 values for different durations
i=1.5 # the decay constant
b = np.arange(0.5, 8.5, 0.5)  # the log of the durations for the bursts
decay=True 
z=0 # z is the element number for the duration being used for this iteration
while decay:
    if z < len(b):
        n = np.arange(b[z]/1000,b[z],(b[z])/1000) # creates an array of data points for each duration 
        k = 10**n 
        g = 10*k**(-i) # the model power law
        integrate=True # calculates t90 for each duration
        u=1
        while integrate:
            t=(np.trapz(g,k))
            q=(np.trapz(g[:u],k[:u]))
            w=(t/100)*5
            if q>w:
                p=k[u-1]
                integrate=False
            else:
                u+=1
        integrate=True
        a=1
        while integrate:
            s=(np.trapz(g,k))
            d=(np.trapz(g[:a],k[:a]))
            f=(s/100)*95
            if d>f:
                o=k[a-1]
                integrate=False
            else:
                a+=1
        t90 = o - p
        h = h + [t90] # adds this t90 to the array
        z  = z+1 # moves onto the next burst duration
    else:
        decay = False
with open("inumber%sh.txt" %i,'w') as outfile:
    for element in h:
        outfile.write(str(element))
        outfile.write("\n")
with open("inumber%s10b.txt" %i,'w') as outfile:
    for element in 10**b:
        outfile.write(str(element))
        outfile.write("\n")