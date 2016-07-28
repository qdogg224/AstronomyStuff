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

angleinterparray=[30.0,92.0,150.0,210.0,270.0,330.0]

tempx=0
tempy1=0
tempy2=0
tempz=0

reader= csv.reader(open("SNR0509_radius_distro_better_RP_UP.txt"),delimiter=',')

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
tempray=0.0

for i in range(len(expansion)):
	just=float(expansion[i])
#	if just>-0.6 and just<1.0:
	tempray=float(rayangle[i])
#	if tempray<350.0:
	rayangle2.append(tempray)
#	else:
#		rayangle2.append(tempray-360.0)
	expan2=float(expansion[i])
	vel=expan2*33.8840
	expansion2.append(vel)

#print expansion2
meanvel=np.average(expansion2)
meanangle=meanvel/33.8840
meananglestr=str(meanangle)

print meanvel,meanangle

expansioninterp=np.interp(angleinterparray,rayangle2,expansion2)

print expansioninterp
