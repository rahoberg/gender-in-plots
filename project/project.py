import math
import pylab
import matplotlib.pyplot as plt
import numpy as np
import csv
import re

plottitles = open("plots/titles")
plotplots = open("plots/plots")
titleline=plottitles.readline()
plotline=plotplots.readline()
femcount=0
masccount=0
zeroshecount=0
zerohecount=0
smallshecount=0
smallhecount=0
medshecount=0
medhecount=0
largeshecount=0
largehecount=0
tvzeroshecount=0
tvzerohecount=0
tvsmallshecount=0
tvsmallhecount=0
tvmedshecount=0
tvmedhecount=0
tvlargeshecount=0
tvlargehecount=0
#xlargehecount=0
#xlargeshecount=0
hecountlist=[]
shecountlist=[]
numscatter=10
countsarray=[[0]*numscatter for i in range(numscatter)]
while plotline and titleline:
    hecount=0
    shecount=0
    while "<EOS>" not in plotline:
        hecount+=len(re.findall(r'\b[hH]i[sm]\b',plotline))#.count(" he ")
        hecount+=len(re.findall(r'\b[hH]e\b',plotline))
        hecount+=len(re.findall(r'\b[hH]imself\b',plotline))
        shecount+=len(re.findall(r'\b[hH]ers?\b',plotline))
        shecount+=len(re.findall(r'\b[sS]he\b',plotline))
        shecount+=len(re.findall(r'\b[hH]erself\b',plotline))
#        hecount+=plotline.count(" He ")
#        shecount+=plotline.count(" she ")
#        shecount+=plotline.count(" She ")
#        hecount+=plotline.count(" his ")
#        hecount+=plotline.count(" him ")
#        shecount+=plotline.count(" her ")
        plotline=plotplots.readline()
    if hecount<numscatter and shecount<numscatter:
        countsarray[hecount][shecount]+=1
        hecountlist.append(hecount)
        shecountlist.append(shecount)
    if shecount!=0 and hecount==0:
        femcount+=1
    if shecount==0 and hecount!=0:
        masccount+=1
    if shecount==0:
        zeroshecount+=1
    if hecount==0:
        zerohecount+=1
    if hecount>0 and hecount<5:
        smallhecount+=1
    if shecount>0 and shecount<5:
        smallshecount+=1
    if hecount>=5 and hecount<15:
        medhecount+=1
    if shecount>=5 and shecount<15:
        medshecount+=1
    if shecount>=15: #and shecount<50:
        largeshecount+=1
    if hecount>=15: # and hecount<50:
        largehecount+=1
    if  "TV series" in titleline or "television series" in titleline:
        if shecount==0:
            tvzeroshecount+=1
        if hecount==0:
            tvzerohecount+=1
        if hecount>0 and hecount<5:
            tvsmallhecount+=1
        if shecount>0 and shecount<5:
            tvsmallshecount+=1
        if hecount>=5 and hecount<15:
            tvmedhecount+=1
        if shecount>=5 and shecount<15:
            tvmedshecount+=1
        if shecount>=15: #and shecount<50:
            tvlargeshecount+=1
        if hecount>=15: # and hecount<50:
            tvlargehecount+=1
    plotline=plotplots.readline()
    titleline=plottitles.readline()

plotplots.close()
plottitles.close()



#Scatterplot                                                                                                
x=[0]*(numscatter**2)
y=[0]*(numscatter**2)
c=[0]*(numscatter**2)
s=[0]*(numscatter**2)
for i in range(numscatter):
    for j in range(numscatter):
        x[i*numscatter+j]=i
        y[i*numscatter+j]=j
        c[i*numscatter+j]=math.log(float(countsarray[i][j])+1)
        s[i*numscatter+j]=float(countsarray[i][j])/10
plt.scatter(x,y,s=s,c=c,cmap='cool')
plt.xlabel('Male pronouns')
plt.ylabel('Female pronouns')
plt.title('Small pronoun counts')
pylab.savefig('coolscatter.png')

#plt.scatter(x,y,s=s,c=c,cmap='hot')
#pylab.savefig('hotscatter.png')

#Plotting all titles
n_groups = 4
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, [zerohecount,smallhecount,medhecount,largehecount], bar_width,
                 alpha=opacity,
                 color='b',
                 label='Male pronouns')
 
rects2 = plt.bar(index + bar_width, [zeroshecount,smallshecount,medshecount,largeshecount], bar_width,
                 alpha=opacity,
                 color='g',
                 label='Female pronouns')
 
plt.xlabel('Range of counts')
plt.ylabel('Number of titles')
plt.title('Pronoun counts by gender (all titles)')
plt.xticks(index + bar_width, ('count=0', '0<count<5', '5<=count<15', '15<=count'))
plt.legend()
 
#plt.tight_layout()
pylab.savefig('alltitles.png')

#Plotting (some) TV titles 
n_groups = 4
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, [tvzerohecount,tvsmallhecount,tvmedhecount,tvlargehecount], bar_width,
                 alpha=opacity,
                 color='b',
                 label='Male pronouns')

rects2 = plt.bar(index + bar_width, [tvzeroshecount,tvsmallshecount,tvmedshecount,tvlargeshecount], bar_width,
                 alpha=opacity,
                 color='g',
                 label='Female pronouns')

plt.xlabel('Range of counts')
plt.ylabel('Number of titles')
plt.title('Pronoun counts by gender (TV titles)')
plt.xticks(index + bar_width, ('count=0', '0<count<5', '5<=count<15', '15<=count'))
plt.legend()
#plt.tight_layout()
pylab.savefig('tvtitles.png')
#plt.show()
