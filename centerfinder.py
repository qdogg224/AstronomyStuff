from sherpa.utils import nearest_interp

load_image(1,"8554_centerfinder.fits")
#load_table_model( "epoch2001" , "776_0509_image.fits" , nearest_interp )
#notice2d("776_0509_phys.reg")
image_data()
set_coord("image")
set_stat("cstat")
set_method("moncar")
show_all()
set_model(gauss2d.snr1+const2d.c1)
c1.c0.max=1.0
c1.c0.min=-1.0
#snr1.xpos.min=40
#snr1.xpos.max=50
#snr1.ypos.min=40
#snr1.ypos.max=50
#epoch2001.ampl=0.00369967/0.00502998
#freeze(epoch2001.ampl)
fit()
image_fit(tile=False)
