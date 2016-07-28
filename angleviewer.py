import matplotlib.pyplot as plt
#import pylab as pl
import numpy as np
import scipy as sp
import csv

rayangle=[]
snrrad1=[]
snrrad2=[]
oldexpo=[]
expansion=[]

tempx=0
tempy1=0
tempy2=0
tempz=0

reader= csv.reader(open("SNR0509_radius_distro_better_RP_UP_NEW.txt"),delimiter=',')

for row in reader:
	tempx,tempy1,tempy2,temp3,tempz=row
	rayangle.append(tempx)
	snrrad1.append(tempy1)
	snrrad2.append(tempy2)
	oldexpo.append(temp3)
	expansion.append(tempz)

n=len(expansion)

#rayangle=np.array(rayangle)
#expansion=np.array(expansion)
rayangle2=[]
expansion2=[]
expan2=0
vel=0

for i in range(len(expansion)):
	just=float(expansion[i])
#	if just>-0.6 and just<1.0:
	rayangle2.append(rayangle[i])
	expan2=float(expansion[i])
	vel=expan2*33.8840
	expansion2.append(vel)

meanvel=np.average(expansion2)
meanangle=meanvel/33.8840
meananglestr=str(meanangle)

print meanvel,meanangle

plt.plot(rayangle2,expansion2,marker="s",label="Expansion along ray",color="r")
plt.plot((0,360),(meanvel,meanvel),color="r",label="Av exp v 7500 km/s",linestyle="dashed")
plt.plot((0,60),(10.8,10.8),color="b",label="Av exp v (30 deg) 10800 km/s",linestyle="dashed")
plt.plot((66,120),(12.4,12.4),color="k",label="Av exp v (90 deg) 12400 km/s",linestyle="dashed")
plt.plot((120,180),(6.6,6.6),color="g",label="Av exp v (150 deg) 6600 km/s",linestyle="dashed")
plt.plot((180,240),(5.3,5.3),color="c",label="Av exp v (210 deg) 5300 km/s",linestyle="dashed")
plt.plot((240,300),(3.3,3.3),color="m",label="Av exp v (270 deg) 3300 km/s",linestyle="dashed")
plt.plot((300,360),(6.2,6.2),color="y",label="Av exp v (330 deg) 6200 km/s",linestyle="dashed")
plt.title("MCSNR 0509-67.5 Chandra Expansion Velocity (2000-2007)")
plt.xlabel("Paralactic ray angle relative to West (Degrees)")
plt.ylabel("Expansion Velocity (1000 km/second)")
plt.xlim(0,360)
plt.ylim(-5,27.0)
plt.legend(bbox_to_anchor=(0.6,0.975),loc=2,fontsize=8)

plt.show()

#flnm="angleviewer_enhanced.eps"
#plt.savefig(flnm,format='eps',bbox_inches="tight")
