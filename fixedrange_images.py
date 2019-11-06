#/usr/bin/python3
import numpy as np
import healpy as hp
import camb
import scipy.misc
import matplotlib

nside = 1024
pars = camb.CAMBparams()
pars.set_cosmology(H0=67.5)
pars.InitPower.set_params()
results = camb.get_results(pars)
powers =results.get_cmb_power_spectra(pars, CMB_unit='muK')
totcl = powers['unlensed_scalar']

TT = totcl[:, 0]
ls = np.arange(len(TT))
ls[0] = 1
cltt = TT/(ls*(ls+1)/(2*np.pi))

vmin = -300.
vmax = 300.
mapnorm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
cmap = matplotlib.cm.get_cmap('jet')

fdir = './data/fixed/'
for k in range(10000):
    xmap = hp.synfast(cltt, nside, verbose=False)
    cutmap = hp.gnomview(xmap, xsize=128, reso=hp.nside2resol(nside, arcmin=True)*2, return_projected_map=True, no_plot=True)
    rgbmap = np.asarray(np.round(cmap(mapnorm(cutmap))[:, :, :3]*255), dtype=int)
    rgb = scipy.misc.toimage(rgbmap)
    imgfname = fdir+'img'+str(k)+'.png'
    rgb.save(imgfname)


