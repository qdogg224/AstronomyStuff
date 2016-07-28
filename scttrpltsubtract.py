import matplotlib.pyplot as plt
#import pylab as pl
import numpy as np
import scipy as sp
import csv

scatterx=[]
scatterx2=[]
scattery1=[]
scattery2=[]
scattersubtract=[]

tempx=0
tempy=0
tempz=0

reader= csv.reader(open("SNR0509_776.txt"),delimiter=',')
#reader= csv.reader(open("RegionCvapecvapecFe1Dconf.txt"),delimiter=' ')

for row in reader:
#	tempx,tempy,tempz=row
	tempx,tempy=row
	scatterx2.append(float(tempx))
	scattery1.append(float(tempy))
#	scattery2.append(float(tempz))

for i in range(len(scattery1)):
	scattery1[i]=scattery1[i]*1000000.0

reader2= csv.reader(open("SNR0509_8554.txt"),delimiter=',')

for row in reader2:
#	tempx,tempy,tempz=row
	tempx,tempy=row
#	scatterx.append(float(tempx))
	scattery2.append(float(tempy))

for i in range(len(scattery2)):
	scattery2[i]=scattery2[i]*1000000.0

#reader3 = csv.reader(open("SNR0102_120_provileage_global3.txt"),delimiter=',')

#for row in reader3:
#	tempx,tempy,tempz=row
#	tempx,tempy=row
#	scatterx.append(float(tempx))
#	scattersubtract.append(float(tempy))


#for i in range(len(scattery2)):
#	diff=5*(scattery2[i]-scattery1[i])
#	scattersubtract.append(diff)

noise2000=0
noise2007=0

for i in range(20):
	noise2000=noise2000+scattery1[len(scattery1)-1-i]/20.0

for i in range(20):
	noise2007=noise2007+scattery2[len(scattery1)-1-i]/20.0


noiseplot2000=15.0*noise2000
noiseplot2007=15.0*noise2007

print noiseplot2000
print noiseplot2007

#print statvalu

#reader2=csv.reader(open("RegionAvapecnH123siglimits.txt"),delimiter=' ')

#siglims=[]
#param0=0.58

#for row in reader2:
#	siglims.append(row)

#print siglims

plt.plot(scatterx2,scattery1,marker="s",label="2000 Profile",color="r")
plt.plot((0,15.44),(noiseplot2000,noiseplot2000),color="r",label="2000 6XRMS noise",linestyle="dashed")
plt.plot((15.44,15.44),(0,noiseplot2000),color="r",linestyle="dashed")
plt.plot(scatterx2,scattery2,marker="+",label="2007 Profile",color="b")
plt.plot((0,15.6),(noiseplot2007,noiseplot2007),color="b",label="2007 6XRMS noise",linestyle="dashed")
plt.plot((15.6,15.6),(0,noiseplot2007),color="b",linestyle="dashed")
#plt.plot(scatterx2,scattersubtract,marker="o",label="2015 - 1999 profile",color="k")
#plt.plot((1.0,15.1),(0.35,0.35),color="r",linestyle="dashed")

#6xSigma for 776 is 1.75
#6xSigma for 8554 is 1.51

#plt.scatter(scatterx,scattery1,marker="o",label="Subtracted normalized counts",color="k")
plt.legend(bbox_to_anchor=(0.7,0.95),loc=2,fontsize=8)
plt.xlabel("Distance from center (arcseconds)")
plt.ylabel("Average surface brightness (x10^{-6})")
#plt.xlim(0,30)
plt.xlim(1,16)
plt.ylim(0,2.5)
plt.suptitle("SNR0509-67.5 X-ray Profile curve (global)")
#plt.vlines(siglims[0],0,1.1,colors='r', linestyles='solid')
#plt.vlines(siglims[1],0,1.1,colors='g', linestyles='solid')
#plt.vlines(siglims[2],0,1.1,colors='b', linestyles='solid')
#plt.vlines(0.59,0,1.1,colors='k', linestyles='solid')
#plt.vlines(siglims[3],0,1.1,colors='b', linestyles='solid')
#plt.vlines(siglims[4],0,1.1,colors='g', linestyles='solid')
#plt.vlines(siglims[5],0,1.1,colors='r', linestyles='solid')

#fig=plt.gcf()
#fig.set_size_inches(6.0,8.0)

#plt.colorbar()
#plt.show()
flnm="SNR0509_xray_profileavg_global.eps"
plt.savefig(flnm,format='eps',bbox_inches="tight")

