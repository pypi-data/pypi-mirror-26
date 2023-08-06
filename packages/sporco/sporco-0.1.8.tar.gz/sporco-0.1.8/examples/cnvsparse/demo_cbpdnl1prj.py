#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2017 by Brendt Wohlberg <brendt@ieee.org>
# All rights reserved. BSD 3-clause License.
# This file is part of the SPORCO package. Details of the copyright
# and user license can be found in the 'LICENSE.txt' file distributed
# with the package.

"""Usage example: cbpdn.ConvBPDNProjL1 (greyscale images)"""

from __future__ import print_function
from builtins import input
from builtins import range

import numpy as np

from sporco import util
from sporco import plot
from sporco.admm import cbpdn
import sporco.metric as sm


# Load demo image
img = util.ExampleImages().image('barbara.png', scaled=True, gray=True)


# Highpass filter test image
npd = 16
fltlmbd = 5
sl, sh = util.tikhonov_filter(img, fltlmbd, npd)


# Load dictionary
D = util.convdicts()['G:12x12x36']


# Set up ConvBPDN options
gamma = 2e-2
opt = cbpdn.ConvBPDNProjL1.Options({'Verbose': True, 'MaxMainIter': 250,
                    'HighMemSolve': True, 'LinSolveCheck': True,
                    'RelStopTol': 5e-3, 'AuxVarObj': False})


# Initialise and run ConvBPDN object
b = cbpdn.ConvBPDNProjL1(D, sh, gamma, opt)
X = b.solve()
print("ConvBPDNProjL1 solve time: %.2fs" % b.timer.elapsed('solve'))


# Reconstruct representation
shr = b.reconstruct().squeeze()
imgr = sl + shr
print("reconstruction PSNR: %.2fdB\n" % sm.psnr(img, imgr))


# Display representation and reconstructed image
fig1 = plot.figure(1, figsize=(21,7))
plot.subplot(1,3,1)
plot.imview(np.sum(abs(X), axis=b.cri.axisM).squeeze(), fgrf=fig1,
            cmap=plot.cm.Blues, title='Representation')
plot.subplot(1,3,2)
plot.imview(imgr, fgrf=fig1, title='Reconstructed image')
plot.subplot(1,3,3)
plot.imview(imgr - img, fgrf=fig1, title='Reconstruction difference')
fig1.show()


# Plot functional value, residuals, and rho
its = b.getitstat()
fig2 = plot.figure(2, figsize=(14,14))
plot.subplot(2,2,1)
plot.plot(its.ObjFun, fgrf=fig2, ptyp='semilogy', xlbl='Iterations',
          ylbl='Functional')
plot.subplot(2,2,2)
plot.plot(its.Cnstr, fgrf=fig2, ptyp='semilogy', xlbl='Iterations',
          ylbl='Constraint')
plot.subplot(2,2,3)
plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T, fgrf=fig2,
          ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
          lgnd=['Primal', 'Dual'])
plot.subplot(2,2,4)
plot.plot(its.Rho, fgrf=fig2, xlbl='Iterations', ylbl='Penalty Parameter')
fig2.show()


# Wait for enter on keyboard
input()
