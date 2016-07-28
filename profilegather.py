#!/usr/bin/env python

infile="8554_profilefinder.img_miriad"
outfile="SNR0509_8554.txt"
regshape="box(3964,4150,111,111)"
#infile="SNR0509_subtracted.img"
#outfile="test.txt"
ismiriad=1 #<- this is a boolian. If the input file you've provided is in miriad format, this should be 1. If this is a fits image, it should be zero.
import os
import math
import csv
import time

##############################################################################

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
	

if ismiriad:
	midfile=infile
else:
	midfile=fitsinp(infile)

#ra,dec=impos("05:09:31.15","-67:31:17.8",midfile)
#print "ra=%s,dec=%s"%(ra,dec)
#subtracted image: ra=81 dec=83.5
ra=81
dec=83.5
n=90 #
intx={}
inty={}
intx[0]=-1234
failcnt=0
mylen=0
for i in range(0,n):	
	xv,yv,num=cgslice(ra,dec,regshape,(i*360.0)/float(n),40,midfile)
#	print xv,yv
	if  intx[0]==-1234:
		print "initialising"
		for j in range(0,num):
			intx[j]=xv[j]
			inty[j]=0.0
		mylen=num
		print "mylen", mylen
	for j in range(0,mylen):
#		print intx[j]
		if j in xv:
			if intx[j] == xv[j]:
				inty[j]=inty[j]+yv[j]
			else:
				print "fail", i, j
				failcnt+=1
for k in range(0,len(intx)):
	print "%e,%e" %(intx[k],inty[k]/float(n))
print "failed", failcnt, " times"

f = open(outfile , "w")

for k in range(0,len(intx)):
	f.write("%e,%e" %(intx[k],inty[k]/float(n))+"\n")

f.close


##############################################################################


#cgslice in=2008-6cm.mir/ valout=/dev/fd/1 posin=/dev/fd/0 device=/xs type=pix  <<EOF
# arcsec arcsec  -0.000001 0.000011 72.146599 -34.566853
# EOF
