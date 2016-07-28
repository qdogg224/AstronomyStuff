# This is a simple Sherpa algorithm designed to fit a background spectrum and evaluate its goodness of fit.
# This script is written and tested by Quentin Roper, based on a talk by Tom Aldcroft given at the CIAO Workshop
# on August 6th, 2011, as well as the Sherpa help thread "Fitting a PHA Data Set with Multiple Responses" which can, at time
# of scripting, be found at http://cxc.harvard.edu/sherpa/threads/manual_source/ .
# Version 0.2 (August 10, 2011)

import numpy as np

import csv

import time

import datetime

execfile("setmodelabunds.py")

# Load the spectrum-- should automatically point to responses.

start_time=time.time()

load_pha(1, "776_knot.pi")
notice(0.5,2.0)
set_xsxset("APECROOT","/home/quentin/Downloads/AtomDB/CIE/apec_v3.0.1")
set_xsxset("NEIAPECROOT","/home/quentin/Downloads/AtomDB/NEI/atomdb_v3.0.1/apec_v3.0.1_nei")
set_xsxset("NEIVERS","3.0")
set_xsabund("wilm")
set_xsxsect("vern")

reg_name="776_knot"

src_mod=xsvvrnei.sc1+xspowerlaw.sc2
thaw_params=[sc1.Si,sc1.S,sc1.Fe,sc1.C,sc1.Mg]

freeze_bkg=1

# Setting statistics and method appropriately

set_stat("cstat")
set_method("moncar")

# Acrobatics for setting the model for the background
# Note-- The background is modelled by a thermal, diffuse absorbed X-ray background, and a particle background consisting of a
# powerlaw and a gaussian that are not convolved with the responses.

brsp=get_response(bkg_id=1)
rsp=get_response(1)
copy_data(1,2)
unit_arf = get_arf(2)
unit_arf.specresp = 0.*unit_arf.specresp +1.0
unitrsp = get_response(2)
absmodelname="tbabs"

set_bkg_full_model(1,brsp(xstbabs.abs1*xsvapec.bc1)+unitrsp(gauss1d.bg1+xspowerlaw.bpl1))
#set_bkg_full_model(1,unitrsp(xspowerlaw.bpl1))
#set_bkg_full_model(1,brsp(xstbabs.abs1*xsvapec.bc1))
#set_bkg_full_model(1,unitrsp(gauss1d.bg1+xspowerlaw.bpl1))

scale = get_bkg_scale(1)

my_bkg_model= (brsp(abs1*bc1)+unitrsp(bg1+bpl1))
#my_bkg_model= (unitrsp(bpl1))
#my_bkg_model=(brsp(abs1*bc1))
#my_bkg_model= (unitrsp(bg1+bpl1))

set_full_model(1,rsp(((xstbabs.abs1*xstbvarabs.abs2)*src_mod))+scale*my_bkg_model)

#abs1.nH=0.186
abs1.nH=0.8
freeze(abs1.nH)

try:
	bg1.pos=1.75
	bg1.pos.min=1.6
	bg1.pos.max=2.0
	bg1.ampl=0.3
	bg1.fwhm=0.01
except:
	print "No Gaussian bg component"

try:
	bc1.kT=1.0
	bc1.kT.max=1.4
	bc1.norm.min=5.0e-7
	thaw(bc1.Fe)
except:
	print "No BG thermal component"

try:
	bpl1.PhoIndex=1
	bpl1.norm=0.01
except:
	print "No BG PL component"

fit_bkg(1)

plot_bkg_fit_resid()

end_time=time.time()

bkgfittime = end_time - start_time

human_uptime = str(datetime.timedelta(seconds=int(bkgfittime)))

print "bkg fit time is "+human_uptime

#raw_input("Press enter to continue")

# thaw(abs1.nH)

# Setting the source abundances to SMC abundances

set_model_abundances(sc1,"LMC")

#try:
#	set_model_abundances(sc2,"LMC")
#else:
#	print "Second source model either does not exist or is nonthermal"

set_model_abundances(abs2,"LMC")

if freeze_bkg==1:
#	try:
	freeze(bpl1)
#	else:
	print " "
#	try:
	freeze(bc1)
#	else:
	print " "
#	try:
	freeze(bg1)
#	else:
	print " "

# abs1.nH=0.06
# abs1.nH.max=1.0
# abs2.nH.max=3.0
# abs2.nH.min=5e-3
#sc1.kT=0.7
#sc1.kT.min=0.3
#sc1.kT.max=1.5
#sc1.norm=5e-5
#sc1.norm.max=1e-3
sc1.norm.min=1e-6

for i in range(len(thaw_params)):
	thaw(thaw_params[i])

#link(sc2.S,sc1.S)
#link(sc2.Si,sc1.Si)

fit(1)

plot_fit_resid()

#add_window()

#plot_fit_resid()

apecfittime=time.time()

sourceuptime = apecfittime - end_time

human_uptime = str(datetime.timedelta(seconds=int(sourceuptime)))

print "Apec source fit took "+human_uptime

#set_method("levmar")

#conf()

#set_method("moncar")

conftime=time.time()

confuptime=conftime-apecfittime

human_uptime= str(datetime.timedelta(seconds=int(confuptime)))

print "Apec conf took "+human_uptime

#vapec1tempfit=get_conf_results()

try:
	bgkT0= bc1.kT.val
	bgthermnorm0= bc1.norm.val
except:
	print "No Thermal BG component"

try:
	pos0= bg1.pos.val
	ampl0= bg1.ampl.val
	fwhm0= bg1.fwhm.val
except:
	print "No Gaussian bg component"

try:
	gamma0 = bpl1.PhoIndex.val
	bgnorm0 = bpl1.norm.val
except:
	print "No PL background component"

nH0= abs2.nH.val
#Fe0= sc1.Fe.val
sourcenorm0=sc1.norm.val
sourcekT0= sc1.kT.val

fit_results=get_fit_results()
stat0=fit_results.statval
dof0=fit_results.dof

