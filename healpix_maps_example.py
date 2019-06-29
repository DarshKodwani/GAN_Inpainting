import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
import sys, platform, os
import camb
from camb import model, initialpower
import h5py

### Running CAMB ###

As_array = np.linspace(1e-9, 3e-9, 20) # Range of A_s values used for making maps

nside = 1024
lmax =  nside*2 #1024
pars = camb.CAMBparams()
pars.set_cosmology(H0=67.5, ombh2=0.022, omch2=0.122, mnu=0.06, omk=0, tau=0.06)
pars.InitPower.set_params(As=2e-9, ns = 0.1)
results = camb.get_results(pars)
powers =results.get_cmb_power_spectra(pars, CMB_unit='muK')
totcl = powers['unlensed_scalar']
TT = totcl[:lmax,0]
ls = np.arange(len(TT))
ls[0] = 1

"""
plt.loglog(ls, TT, color = 'k')
plt.xlim([2,totcl.shape[0]])
plt.show()
"""

### Making boxes ###

box_xsize = 800 # Size of box

xmap = hp.synfast(TT/(ls*(ls+1)/(2*np.pi)), nside)
box = hp.cartview(xmap, lonra = [-10, 0], latra = [-10, 0], return_projected_map = True, xsize = box_xsize)

hp.mollview(xmap, min = -300, max = 300)
hp.mollview(xmap)
plt.savefig("full_sky_As9_ns01.pdf")
plt.show()

"""
cls_recon = hp.anafast(xmap, lmax = lmax)
plt.loglog(ls, TT, label = 'input')
plt.loglog(ls, cls_recon[1:], label = 'recon')
plt.xlim([2,lmax])
plt.legend()
plt.show()
"""
