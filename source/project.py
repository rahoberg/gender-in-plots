import re
import matplotlib.pyplot as plt
import numpy as np
import pylab

# Count male pronouns and female pronouns in file
def countPronouns(filename):
    malepattern='[hH]i[sm]|[hH]e|[hH]imself'
    femalepattern='[hH]ers?|[sS]he|[hH]erself'  
    femalecounts=[]
    malecounts=[]
    #assuming the file starts with a title and alternates with plots
    isPlot=False
    with open(filename,'r') as f:
        for line in f:
            if isPlot:
                femalecounts.append(len(re.findall(r'\b(%s)\b'%femalepattern,line)))
                malecounts.append(len(re.findall(r'\b(%s)\b'%malepattern,line)))
            isPlot= not isPlot
    return np.array(femalecounts),np.array(malecounts)

#Compute empirical cumulative distribution function
def ecdf(x):
    n=len(x)
    y=np.sort(x)
    z=1/n*np.array(range(n))
    return y,z

def plotecdf(title,malecounts,femalecounts,outfilename,countlimit):
    fx,fy=ecdf(femalecounts[femalecounts<countlimit])
    mx,my=ecdf(malecounts[malecounts<countlimit])
    plt.plot(fx,fy, label='Female')
    plt.plot(mx,my,label='Male')
    plt.xlabel('Pronoun count')
    plt.ylabel('ECDF')
    plt.title(title)
    plt.legend(loc='lower right')
    pylab.savefig(outfilename)
    plt.close()

#Scatterplot                                                 
def plotscatter(title,malecounts,femalecounts,outfilename,numscatter):
#countsArray gives number of occurrences of all possible pairs of male/female pronouns up to numscatter
    countsArray=[[0]*numscatter for i in range(numscatter)]
    for i in range(len(femalecounts)):
        if femalecounts[i]<numscatter and malecounts[i]<numscatter:
            countsArray[femalecounts[i]][malecounts[i]]+=1
    scaling=max(max(countsArray))
    x=[0]*(numscatter**2)
    y=[0]*(numscatter**2)
    c=[0]*(numscatter**2)
    s=[0]*(numscatter**2)
    for i in range(numscatter):
        for j in range(numscatter):
            x[i*numscatter+j]=i
            y[i*numscatter+j]=j
            c[i*numscatter+j]=np.log(float(countsArray[i][j])+1)
            s[i*numscatter+j]=float(countsArray[i][j])/scaling*1000
    plt.scatter(x,y,s=s,c=c,cmap='cool')
    plt.xlabel('Female pronouns')
    plt.ylabel('Male pronouns')
    plt.title(title)
    pylab.savefig(outfilename)
    plt.close()

#Permutation test
#Null hypothesis: he counts and she counts come from same distribution
def permtest(malecounts,femalecounts):
    combinedlist=np.concatenate((malecounts,femalecounts))
    size=10000
    permutedsamples=np.empty(size)
    obsdiff=np.mean(combinedlist[:len(combinedlist)//2])-np.mean(combinedlist[len(combinedlist)//2:])
    for i in range(size):
        permutedlist=np.random.permutation(combinedlist)
        #compute sample of the difference in mean, put into permuted samples
        permutedsamples[i]=np.mean(permutedlist[:len(permutedlist)//2])-np.mean(permutedlist[len(permutedlist)//2:])
    print("99 Percentile over permutations:", np.percentile(permutedsamples,[.5,99.5]))
    #print("Observed difference of means:", np.mean(combinedlist[:len(combinedlist)//2])-np.mean(combinedlist[len(combinedlist)//2:]))
    print("p value = ",np.sum(permutedsamples>=obsdiff)/len(permutedsamples))
    return np.mean(combinedlist[:len(combinedlist)//2])-np.mean(combinedlist[len(combinedlist)//2:])

def makePlots(filename,outecdf,outscatter,numscatter=10,countlimit=50):
    ecdftitle='Plots from '+filename
    scattertitle='Small pronoun counts from '+filename
    femalecounts,malecounts=countPronouns(filename)
    plotecdf(ecdftitle,malecounts,femalecounts,outecdf,countlimit)
    plotscatter(scattertitle,malecounts,femalecounts,outscatter,numscatter)
    print(filename)
    return permtest(malecounts,femalecounts)
    

def plotByYear():
    y=[]
    for year in range(1990,2019):
        syear=str(year)
        meandiff=makePlots('plotdata/'+syear+'movieplots','plots/'+syear+'movieecdf','plots/'+syear+'moviescatter')
        y.append(meandiff)
    x=range(1990,2019)
    m,b=np.polyfit(x,y,1)
    xp=[1990,2018]
    yp=[1990*m+b,2018*m+b]
    plt.plot(x,y,marker='.',linestyle='none')
    plt.plot(xp,yp)
    plt.xlabel('Year')
    plt.ylabel('Average Difference') 
    plt.title('Average #Male Pronouns - #Female Pronouns in movie plots')
    pylab.savefig('pronoundiffbyyear')

#plotByYear()

#makePlots('2017movieplots','plots/2017movieecdf','plots/2017moviescatter')
#makePlots('movieplots','plots/movieecdf','plots/moviescatter',10,50)
#makePlots('tvplots','plots/tvecdf','plots/tvscatter',10,50)
#makePlots('westernbookplots','plots/westernbookecdf','plots/westernbookscatter',10,50)
#makePlots('feministnovels','plots/feministnovelsecdf','plots/feministnovelsscatter',10,50)
#makePlots('lonerangerplots','plots/lonerangerecdf','plots/lonerangerscatter',10,50)
#makePlots('movieplots2','plots/movieecdf','plots/moviescatter')
