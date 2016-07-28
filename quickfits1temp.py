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

load_pha(1, "776_0509.pi")
notice(0.5,2.0)
set_xsxset("APECROOT","/home/quentin/Downloads/AtomDB/CIE/apec_v3.0.1")
set_xsxset("NEIAPECROOT","/home/quentin/Downloads/AtomDB/NEI/atomdb_v3.0.1/apec_v3.0.1_nei")
set_xsxset("NEIVERS","3.0")
set_xsabund("wilm")
set_xsxsect("vern")

reg_name="776_0509"

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
#my_bkg_model= (unitrsp(bpl1))set_xsxset("NEIAPECROOT","/home/quentin/Downloads/AtomDB/NEI/atomdb_v3.0.1/apec_v3.0.1_nei")
set_xsxset("NEIVERS","3.0")
#my_bkg_model=(brsp(abs1*bc1))
#my_bkg_model= (unitrsp(bg1+bpl1))

set_full_model(1,rsp(((xstbabs.abs1*xstbvarabs.abs2)*(xsvapec.sc1)))+scale*my_bkg_model)

abs1.nH=0.192
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

set_model_abundances(abs2,"LMC")

freeze(bpl1)
freeze(bc1)
freeze(bg1)

# abs1.nH=0.06
# abs1.nH.max=1.0
# abs2.nH.max=3.0
# abs2.nH.min=5e-3
sc1.kT.min=1.0
#sc1.kT.min=0.3
#sc1.kT.max=1.5
#sc1.norm=5e-5
#sc1.norm.max=1e-3
sc1.norm.min=1e-6

thaw(sc1.S)
#thaw(sc1.O)
#thaw(sc1.Fe)
thaw(sc1.Si)
#thaw(sc1.Ne)
#thaw(sc1.Mg)

fit(1)

Si0=sc1.Si.val
S0=sc1.S.val
kT0=sc1.kT.val
norm0=sc1.norm.val

add_window()

plot_fit_resid()

apecfittime=time.time()

sourceuptime = apecfittime - end_time

human_uptime = str(datetime.timedelta(seconds=int(sourceuptime)))

print "Apec source fit took "+human_uptime

set_full_model(1,rsp(((xstbabs.abs1*xstbvarabs.abs2)*(xsvapec.sc1+xspowerlaw.sc2)))+scale*my_bkg_model)

sc1.Si=Si0
sc1.S=S0
sc1.norm=norm0
sc1.kT=kT0

fit(1)

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

#filename=reg_name+absmodelname+"vapec1temp_results.csv"
#outfile=open(filename,"wb")
#wrt=csv.writer(outfile)
#outfile.write("cash/dof= {0} / {1} \n" .format(stat0,dof0))
#wrt.writerow(vapec1tempfit.parnames)
# wrt.writerow(['\n'])
#wrt.writerow(vapec1tempfit.parvals)
# wrt.writerow(['\n'])
#wrt.writerow(vapec1tempfit.parmins)
# wrt.writerow(['\n'])
#wrt.writerow(vapec1tempfit.parmaxes)
#outfile.close()

# plot_fit_resid(1)

# print_window("presbipolr1spec.ps")

set_full_model(1,rsp(((xstbabs.abs1*xstbvarabs.abs2)*(xsvvrnei.sc1)))+scale*my_bkg_model)

# thaw(abs1.nH)

# Setting the source abundances to SMC abundances

set_model_abundances(sc1,"LMC")

set_model_abundances(abs2,"LMC")

# abs1.nH=0.06
# abs1.nH.max=1.0
# sc1.kT.min=1.0

#thaw(sc1.Fe)
link(sc1.kT_init,sc1.kT)
thaw(sc1.Si)
thaw(sc1.S)

nei_init_time=time.time()

fit(1)

Si0=sc1.Si.val
S0=sc1.S.val
norm0=sc1.norm.val
kT0=sc1.kT.val
Tau0=sc1.Tau.val

nei_final_time=time.time()

confuptime=nei_final_time-nei_init_time

human_uptime= str(datetime.timedelta(seconds=int(confuptime)))

print "NEI fit took "+human_uptime

#set_method("levmar")

#conf()apecfittime=time.time()

sourceuptime = apecfittime - end_time

human_uptime = str(datetime.timedelta(seconds=int(sourceuptime)))

#set_method("moncar")

set_full_model(1,rsp(((xstbabs.abs1*xstbvarabs.abs2)*(xsvvrnei.sc1+xspowerlaw.sc2)))+scale*my_bkg_model)

sc1.Si=Si0
sc1.S=S0
sc1.norm=norm0
sc1.kT=kT0
sc1.Tau=Tau0

set_model_abundances(sc1,"LMC")

set_model_abundances(abs2,"LMC")

# abs1.nH=0.06
# abs1.nH.max=1.0
# sc1.kT.min=1.0

#thaw(sc1.Fe)
link(sc1.kT_init,sc1.kT)
thaw(sc1.Si)
thaw(sc1.S)

fit(1)

nH0= abs1.nH.val

Fe0= sc1.Fe.val
sourcenorm0=sc1.norm.val
sourcekT0= sc1.kT.val

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

fit_results=get_fit_results()
stat0=fit_results.statval
dof0=fit_results.dof

#vnei1tempfit=get_conf_results()

#filename=reg_name+absmodelname+"vnei1temp_results.csv"
#outfile=open(filename,"wb")
#wrt=csv.writer(outfile)
#outfile.write("cash/dof= {0} / {1} \n" .format(stat0,dof0))
#wrt.writerow(vnei1tempfit.parnames)
# wrt.writerow(['\n'])
#wrt.writerow(vnei1tempfit.parvals)
# wrt.writerow(['\n'])
#wrt.writerow(vnei1tempfit.parmins)
# wrt.writerow(['\n'])
#wrt.writerow(vnei1tempfit.parmaxes)
#outfile.close()

add_window()

plot_fit_resid(1)
