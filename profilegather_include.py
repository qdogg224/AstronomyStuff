#!/usr/bin/env python

# File 1 inputs and controls
infile1="776_profilefinder.img_miriad"
ismiriad1=1 #<- this is a boolian. If the input file you've provided is in miriad format, this should be 1. If this is a fits image, it should
regshape1="box(3964,4150,111,111)" #<- This is the region (in physical coordinates) which is sent to cgslice for picturing purposes.
ra1=81 #<- The Right Ascension coordinate of the center of the remnant. When an integer or half integer, this is the image X-coordinate. If this is in another coordinate system, the impos function will have to be used (functionality not yet coded)
dec1=83.5 #<-The Declination coordinate of the center of the remnant. When an integer or half integer, this is the image Y-coordinate.

# File 2 inputs and controls
infile2="8554_profilefinder.img_miriad"
ismiriad2=1 #<- this is a boolian. If the input file you've provided is in miriad format, this should be 1. If this is a fits image, it should  be zero.
regshape2="box(3964,4150,111,111)" #<- This is the region (in physical coordinates) which is sent to cgslice for picturing purposes.
ra2=81
dec2=83.5

outfile="SNR0509_profiledifference.txt"

#infile="SNR0509_subtracted.img"
#outfile="test.txt"

import os
import math
import csv
import time

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
	slicex={}
	slicey={}
#	cmd="cgslice in=%s type=pix labtyp=hms,dms region='box(0,0,77,77)' valout=output posin=input device=/xs xrange=0,30 yrange=-1e-3,5e-3 > /dev/null" %(file)
	cmd="cgslice in=%s type=pix labtyp=relpix region='box(40,39.5,124,124.5)' valout=output posin=input device=/xs xrange=0,20 yrange=0,5e-6 > /dev/null" %(file)
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
#			print l[0]
			if l[0]=='1':
				slicex[i]=float(l[-2])
				slicey[i]=float(l[-1])
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
	fluxnoise=0
	for i in range(numnoise):
		fluxnoise=fluxnoise+fluxarray[len(fluxarray)-1-i]/numnoise
	return fluxnoise

##############################################################################	

def SNRrad(fluxarray,fluxnoise):
	arraylength=len(fluxarray)
	for i in range(len(fluxarray)):
		if fluxarray[len(fluxarray)-1-i]<5.0*fluxnoise:
			arraylength=arraylength-1
		else:
			break
	return arraylength

##############################################################################	

if ismiriad1:
	midfile1=infile1
else:
	midfile1=fitsinp(infile1)

if ismiriad2:
	midfile2=infile2
else:
	midfile2=fitsinp(infile2)

n=90 #
intx={}
inty={}
intx[0]=-1234
failcnt=0
mylen=0
noise1=1.34819e-08
noise2=1.57609e-08
