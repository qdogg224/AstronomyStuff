#!/usr/bin/env python

# File 1 inputs and controls
infile1="776_profilefinder.img_miriad"
ismiriad1=1 #<- this is a boolian. If the input file you've provided is in miriad format, this should be 1. If this is a fits image, it should
regshape1="box(3964,4150,111,111)" #<- This is the region (in physical coordinates) which is sent to cgslice for picturing purposes.
ra1=81 #<- The Right Ascension coordinate of the center of the remnant. When an integer or half integer, this is the image X-coordinate. If this is in another coordinate system, the impos function will have to be used (functionality not yet coded)
dec1=83.5 #<-The Declination coordinate of the center of the remnant. When an integer or half integer, this is the image Y-coordinate.

# File 2 inputs and controls
infile2="8554_profilefinder_UP_rp.img_miriad"
ismiriad2=1 #<- this is a boolian. If the input file you've provided is in miriad format, this should be 1. If this is a fits image, it should  be zero.
regshape2="box(3964,4150,111,111)" #<- This is the region (in physical coordinates) which is sent to cgslice for picturing purposes.
ra2=81
dec2=83.5

#Telescope parameters
detres=0.492 #Detector natural resolution in arcseconds

outfile="SNR0509_profiledifference_RP_CHRISTENE.txt"
outfile2="SNR0509_radius_distro_better_RP_UP_NEW.txt"

#infile="SNR0509_subtracted.img"
#outfile="test.txt"

import os
import math
import csv
import time
import numpy as np
import matplotlib.pyplot as plt

##############################################################################

#This is a time-saver that will automatically convert a fits file to a miriad file. This is controlled by the ismiriad boolean and the if statement below.

def fitsinp(file):
	miriadtempfile="%s_miriad" %(file)
	print("ismiriad boolean set to 0; using fits to convert to miriad image file named "+str(miriadtempfile)) 
	cmd="fits in=%s op=xyin out=%s" %(file,miriadtempfile)
	pcmd=os.popen(cmd)
	pcmd.read()
	return str(miriadtempfile)

##############################################################################

def impos(ra,dec,file):
	cmd="impos in=%s coord=%s,%s type=hms,dms" %(file,ra,dec)
	pcmd=os.popen(cmd)
	output=pcmd.read()
#	print output
	output=output.split('\n')
	rap=output[16].split()[-1]
	decp=output[17].split()[-1]
	return (float(rap),float(decp))
	
##############################################################################	

def cgslice(refra,refdec,regshape,angle,d,file):
	slicex=[]
	slicey=[]
#	cmd="cgslice in=%s type=pix labtyp=hms,dms region='box(0,0,77,77)' valout=output posin=input device=/xs xrange=0,30 yrange=-1e-3,5e-3 > /dev/null" %(file)
	cmd="cgslice in=%s type=pix labtyp=relpix region='box(40,39.5,124,124.5)' valout=output posin=input device=/xs xrange=0,20 yrange=0,5e-6 > /dev/null" %(file)
#	cmd="cgslice in=%s type=pix labtyp=relpix region='box(40,39.5,124,124.5)' valout=output posin=input device=xrayexample.ps/ps xrange=0,20 yrange=0,5e-6 > /dev/null" %(file)
	cmd_in=open("input","w")
	endx=refra  + d*math.cos(math.radians(angle))
	endy=refdec + d*math.sin(math.radians(angle))
#	print endx,endy
	cmd_in.write("abspix abspix  %f %f %f %f\n"%(refra,refdec,endx,endy))
	cmd_in.close()
	try:
		os.unlink("output")
	except:
		pass
	os.system(cmd)
	cmd_out=open("output","r")
	res=cmd_out.read()
	cmd_out.close()
#	print res
	lines=res.split('\n')
	i=0
	for line in lines:
#		print line
		if line:
			l=line.split()
#			print l[-1]
			if l[0]=='1':
#				slicex[i]=float(l[-2])
#				slicey[i]=float(l[-1])
				slicex.append(float(l[-2]))
				slicey.append(float(l[-1]))
				i=i+1
	try:
		os.unlink("input")
		os.unlink("output")
	except:
		pass
	time.sleep(0.1)
	return slicex,slicey,i
	
##############################################################################	

def findnoise(fluxarray,numnoise):
	fluxnoise=0.0
	for i in range(numnoise):
		fluxnoise=fluxnoise+fluxarray[len(fluxarray)-1-i]/numnoise
	return fluxnoise

##############################################################################	

def SNRrad(fluxarray,fluxnoise):
	arraylength=len(fluxarray)
	for i in range(len(fluxarray)):
		if fluxarray[len(fluxarray)-1-i]<10.0*fluxnoise:
			arraylength=arraylength-1
		else:
			break
	return arraylength

##############################################################################	

def expansion1dfinder(radarray2000,fluxarray2000,radarray2007,fluxarray2007,leftlim0,rightlim0):
	radarray2000_expanded=[]
	leftlim=leftlim0
	rightlim=rightlim0
#	fluxarray2007_interp=fluxarray2007
	scalearray=np.linspace(0.5,1.5,100)
	radarray=np.linspace(-0.5,1.0,500)
#	print radarray
	tempfluxarray2000=fluxarray2000
	numscale=len(scalearray)
	radscale=len(radarray)
	resid=0.0
	minresid=1000000.0
	scale_best=0.0
	expbest=0.0
	residualarray=[]
	expansionarray=[]
#	for i in range(numscale):
	for j in range(radscale):
		radarray2000_expanded=[]
#		radarray2000_expanded=radarray2000[1:-1]
#		fluxarray2007_interp=fluxarray2007
#		radarray2000_expanded=radarray2000
		for k in range(len(radarray2000)):
			radarray2000_expanded.append(radarray2000[k]+radarray[j])
		fluxarray2007_interp=np.interp(radarray2000_expanded,radarray2007,fluxarray2007,left=leftlim,right=rightlim)
#		print fluxarray2007_interp
		resid=0.0
		for k in range(len(fluxarray2000)):
			if (radarray2000_expanded[k]>leftlim and radarray2000_expanded[k]<rightlim):
				resid=resid+(fluxarray2007_interp[k]-fluxarray2000[k])*(fluxarray2007_interp[k]-fluxarray2000[k])
#		print resid
		residualarray.append(resid)
		if (resid<minresid):
#			print resid
			minresid=resid
#			scale_best=scalearray[i]
			expbest=radarray[j]
			bestfitrad=radarray2000_expanded
#	plotbestfit(radarray2000,fluxarray2000,radarray2007,fluxarray2007,bestfitrad,expbest,leftlim,rightlim)
#	plotresid(radarray,residualarray)
	return expbest

##############################################################################

def plotbestfit(radarray2000,fluxarray2000,radarray2007,fluxarray2007,bestfitrad,expbest,leftlim0,rightlim0):
	plt.plot(bestfitrad,fluxarray2000,marker="s",label="Expansion along ray",color="r")
	fluxarray2007_interp=np.interp(bestfitrad,radarray2007,fluxarray2007)
	plt.plot(bestfitrad,fluxarray2007_interp,marker="s",label="Expansion along ray",color="b")
#	plt.plot(radarray2007,fluxarray2007,marker="s",label="Expansion along ray",color="b")
	plt.show()

##############################################################################

def plotresid(array1,array2):
	plt.plot(array1,array2,marker="s",label="Expansion along ray",color="r")
	plt.show()

##############################################################################

if ismiriad1:
	midfile1=infile1
else:
	midfile1=fitsinp(infile1)

if ismiriad2:
	midfile2=infile2
else:
	midfile2=fitsinp(infile2)

#ra,dec=impos("05:09:31.15","-67:31:17.8",midfile)
#print "ra=%s,dec=%s"%(ra,dec)
#subtracted image: ra=81 dec=83.5

n=100 #
intx={}
inty={}
snr_phi=[]
snr_rad1=[]
snr_rad2=[]
expansion=[]
betterexpansion=[]
intx[0]=-1234
failcnt=0
mylen=0
noise2=1.34819e-08
noise1=1.57609e-08


for i in range(n):
	snr_phi.append(i*360.0/float(n))


for i in range(0,n):	
#	print i
	xv1,yv1,num1=cgslice(ra1,dec1,regshape1,(i*360.0)/float(n),40,midfile1)
#	xv1,yv1,num1=cgslice(ra1,dec1,regshape1,349.2,40,midfile1)
#	xv1=np.array(xv1)
#	yv1=np.array(yv1)
#	noise1=findnoise(yv1,20)
	radindex1=SNRrad(yv1,noise1)
#	print radindex1
	snr_radius1=xv1[radindex1-1]
	snr_rad1.append(snr_radius1)
	xv2,yv2,num2=cgslice(ra2,dec2,regshape2,(i*360.0)/float(n),40,midfile2)
#	xv2,yv2,num2=cgslice(ra2,dec2,regshape2,349.2,40,midfile2)
#	xv2=np.array(xv2)
#	yv2=np.array(yv2)
	exparameter=expansion1dfinder(xv1,yv1,xv2,yv2,14.0,17.0)
	print exparameter
	if exparameter<-0.05:
		exparameter=expansion1dfinder(xv1,yv1,xv2,yv2,10.0,17.0)

	betterexpansion.append(exparameter)
	print exparameter
#	print "best exp is %s" %(exparameter)
#	noise1=findnoise(yv1,20)
	radindex2=SNRrad(yv2,noise2)
#	print radindex2
	snr_radius2=xv2[radindex2-1]
	snr_rad2.append(snr_radius2)
	snr_expansion=snr_radius2-snr_radius1
#	print snr_expansion
	if snr_expansion<0:
		print "Weirdness at index %s expansion %s" %(i,snr_expansion)
	expansion.append(snr_expansion)
#	print "The noise level along this ray is %s and the SNR radius is %s" %(noise1,snr_radius)
#	print xv,yv
	if  intx[0]==-1234:
		print "initialising"
		for j in range(0,num1):
			intx[j]=xv1[j]
			inty[j]=0.0
		mylen=num1
#		print "mylen", mylen
	for j in range(0,mylen):
#		print intx[j]
		if j in xv1:
			if intx[j] == xv1[j]:
				inty[j]=inty[j]+yv1[j]
			else:
				print "fail", i, j
				failcnt+=1
#for k in range(0,len(intx)):
#	print "%e,%e" %(intx[k],inty[k]/float(n))
#print "failed", failcnt, " times"

#f = open(outfile , "w")

#for k in range(0,len(intx)):
#	f.write("%e,%e" %(intx[k],inty[k]/float(n))+"\n")

#f.close

sortexpansion=np.sort(expansion)

print np.average(expansion),np.std(expansion)

stdev=np.std(expansion)

uncert=np.sqrt((stdev*stdev+3*(0.492)*(0.492))/(3*np.float(n)))

uncert=str(uncert)

expo=str(np.average(expansion))

print("Naive expansion is "+expo+" plus or minus "+uncert+" arcsec.")

print np.average(betterexpansion),np.std(betterexpansion)

betterstdev=np.std(betterexpansion)

uncert=np.sqrt((betterstdev*betterstdev+3*detres*detres)/(3*np.float(n)))

uncert=str(uncert)

expo=str(np.average(betterexpansion))

print("Better expansion is "+expo+" plus or minus "+uncert+" arcsec.")

f= open(outfile2, "w")

for i in range(len(expansion)):
	f.write("%.4f,%.4f,%.4f,%.4f,%.4f" %(snr_phi[i],snr_rad1[i],snr_rad2[i],expansion[i],betterexpansion[i])+"\n")

f.close

##############################################################################


#cgslice in=2008-6cm.mir/ valout=/dev/fd/1 posin=/dev/fd/0 device=/xs type=pix  <<EOF
# arcsec arcsec  -0.000001 0.000011 72.146599 -34.566853
# EOF
