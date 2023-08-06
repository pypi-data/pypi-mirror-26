#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2017 by Brendt Wohlberg <brendt@ieee.org>
# All rights reserved. BSD 3-clause License.
# This file is part of the SPORCO package. Details of the copyright
# and user license can be found in the 'LICENSE.txt' file distributed
# with the package.

"""Example demonstrating the use of dictlrn.DictLearn to construct a
dictionary learning algorithm with the flexibility of choosing the
sparse coding and dictionary update classes. In this case they are
ConvBPDN and ConvCnstrMOD respectively, so the resulting dictionary
learning algorithm is equivalent to cbpdndl.ConvBPDNDictLearn (see
usage example 'demo_cbpdndl_clr_ssd.py'). This example uses colour
input images and a colour dictionary.
"""

from __future__ import division
from __future__ import print_function
from builtins import input
from builtins import range

import numpy as np

from sporco.admm import cbpdn
from sporco.admm import ccmod
from sporco.admm import dictlrn
from sporco import cnvrep
from sporco import util
from sporco import plot


# Training images
exim = util.ExampleImages(scaled=True, zoom=0.5)
img1 = exim.image('barbara.png', idxexp=np.s_[10:522, 100:612])
img2 = exim.image('kodim23.png', idxexp=np.s_[:, 60:572])
img3 = exim.image('monarch.png', idxexp=np.s_[:, 160:672])
S = np.stack((img1, img2, img3), axis=3)


# Highpass filter test images
npd = 16
fltlmbd = 5
sl, sh = util.tikhonov_filter(S, fltlmbd, npd)


# Initial dictionary
np.random.seed(12345)
D0 = np.random.randn(8, 8, 3, 64)


# Construct object representing problem dimensions
cri = cnvrep.CDU_ConvRepIndexing(D0.shape, sh)

# X and D update options
lmbda = 0.2
optx = cbpdn.ConvBPDN.Options({'Verbose': False, 'MaxMainIter': 1,
                    'rho': 50.0*lmbda + 0.5,
                    'AutoRho': {'Period': 10, 'AutoScaling': False,
                    'RsdlRatio': 10.0, 'Scaling': 2.0, 'RsdlTarget': 1.0}})
optd = ccmod.ConvCnstrMODOptions({'Verbose': False, 'MaxMainIter': 1,
                    'rho': cri.K,
                    'AutoRho': {'Period': 10, 'AutoScaling': False,
                    'RsdlRatio': 10.0, 'Scaling': 2.0, 'RsdlTarget': 1.0}},
                    method='ism')

# Normalise dictionary according to Y update options
D0n = cnvrep.Pcn(D0, D0.shape, cri.Nv, dimN=2, dimC=1, crp=True,
                 zm=optd['ZeroMean'])

# Update D update options to include initial values for Y and U
optd.update({'Y0': cnvrep.zpad(cnvrep.stdformD(D0n, cri.C, cri.M), cri.Nv),
             'U0': np.zeros(cri.shpD)})

# Create X update object
xstep = cbpdn.ConvBPDN(D0n, sh, lmbda, optx)

# Create D update object
dstep = ccmod.ConvCnstrMOD(None, sh, D0.shape, optd, method='ism')

# Create DictLearn object
opt = dictlrn.DictLearn.Options({'Verbose': True, 'MaxMainIter': 100})
d = dictlrn.DictLearn(xstep, dstep, opt)
D1 = d.solve()
print("DictLearn solve time: %.2fs" % d.timer.elapsed('solve'), "\n")


# Display dictionaries
D1 = D1.squeeze()
fig1 = plot.figure(1, figsize=(14,7))
plot.subplot(1,2,1)
plot.imview(util.tiledict(D0), fgrf=fig1, title='D0')
plot.subplot(1,2,2)
plot.imview(util.tiledict(D1), fgrf=fig1, title='D1')
fig1.show()


# Plot functional value and residuals
itsx = xstep.getitstat()
itsd = dstep.getitstat()
fig2 = plot.figure(2, figsize=(21,7))
plot.subplot(1,3,1)
plot.plot(itsx.ObjFun, fgrf=fig2, xlbl='Iterations', ylbl='Functional')
plot.subplot(1,3,2)
plot.plot(np.vstack((itsx.PrimalRsdl, itsx.DualRsdl, itsd.PrimalRsdl,
                     itsd.DualRsdl)).T,
          fgrf=fig2, ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
          lgnd=['X Primal', 'X Dual', 'D Primal', 'D Dual'])
plot.subplot(1,3,3)
plot.plot(np.vstack((itsx.Rho, itsd.Rho)).T, fgrf=fig2, xlbl='Iterations',
          ylbl='Penalty Parameter', ptyp='semilogy', lgnd=['Rho', 'Sigma'])
fig2.show()


# Wait for enter on keyboard
input()
