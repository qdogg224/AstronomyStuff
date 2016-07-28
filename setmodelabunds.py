def set_model_abundances(modelname,galcontrol):
	if galcontrol=="SMC":
		print "SMC abundances based on Russell and Dopita (1992)"
		set_par(modelname.He,0.83)
		set_par(modelname.C,0.13)
		set_par(modelname.N,0.05)
		set_par(modelname.O,0.15)
		set_par(modelname.Ne,0.19)
		set_par(modelname.Mg,0.24)
		set_par(modelname.Si,0.28)
		set_par(modelname.S,0.21)
		set_par(modelname.Ar,0.16)
		set_par(modelname.Ca,0.21)
		set_par(modelname.Fe,0.20)
		set_par(modelname.Ni,0.40)
		try:
			set_par(modelname.Al,0.80)
		except:
			print "No Al parameter"
#		show_model()
	elif galcontrol=="LMC":
		print "LMC abundances based on Russell and Dopita (1992)"
		set_par(modelname.He,0.89)
		set_par(modelname.C,0.26)
		set_par(modelname.N,0.16)
		set_par(modelname.O,0.32)
		set_par(modelname.Ne,0.42)
		set_par(modelname.Mg,0.74)
		set_par(modelname.Si,1.0)
		set_par(modelname.S,0.27)
		set_par(modelname.Ar,0.49)
		set_par(modelname.Ca,0.33)
		set_par(modelname.Fe,0.50)
		set_par(modelname.Ni,0.62)
		try:
			set_par(modelname.Al,0.50)
		except:
			print "No Al parameter"
#		show_model()
	else:
		print "No abundance table with that name..."


