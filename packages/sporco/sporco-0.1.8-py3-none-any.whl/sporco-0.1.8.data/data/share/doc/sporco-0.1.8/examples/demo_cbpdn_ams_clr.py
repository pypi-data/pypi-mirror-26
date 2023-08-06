#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2017 by Brendt Wohlberg <brendt@ieee.org>
# All rights reserved. BSD 3-clause License.
# This file is part of the SPORCO package. Details of the copyright
# and user license can be found in the 'LICENSE.txt' file distributed
# with the package.

"""Usage example: cbpdn.AddMaskSim (colour images)"""

from __future__ import print_function
from builtins import input
from builtins import range

import numpy as np

from sporco import plot
from sporco.admm import cbpdn
import sporco.metric as sm


# Construct image, mask, and dictionary. The example is such that the
# most effective representation, consisting of only 4 non-zero
# coefficients, is only possible if the mask on the reconstructed
# image is applied to the data fidelity term.
N = 16
L = 6
S = np.zeros((2*(N+L)+1,)*2 + (3,))
D = np.zeros((2*L+1,)*2+(3,2,))
for k in range(0,3):
    S[L+N,L:2*L+1,k] = (k+1)/3.0
    S[L+N,-2*L-1:-L,k] = (k+1)/3.0
    S[L:2*L+1,L+N,k] = (k+1)/3.0
    S[-2*L-1:-L,L+N,k] = (k+1)/3.0
    D[L,:,k,0] = (k+1)/3.0
    D[:,L,k,1] = (k+1)/3.0
W = np.zeros(S.shape[0:2])
W[L:-L,L:-L] = 1.0


# Set up ConvBPDN options
lmbda = 1e-3
opt = cbpdn.ConvBPDN.Options({'Verbose': True, 'MaxMainIter': 500,
                        'HighMemSolve': True, 'RelStopTol': 1e-3,
                        'AuxVarObj': False, 'RelaxParam': 1.8,
                        'rho': 1e2*lmbda, 'AutoRho': {'Enabled': False,
                        'StdResiduals': True}})


# Construct cbpdn.AddMaskSim wrapper for cbpdn.ConvBPDN
ams = cbpdn.AddMaskSim(cbpdn.ConvBPDN, D, S, W, lmbda, opt=opt)

# Call solve via wrapper
X = ams.solve()
print("AddMaskSim wrapped ConvBPDN solve time: %.2fs" %
      ams.timer.elapsed('solve'))


# Reconstruct representation
Sr = ams.reconstruct().squeeze()
print("                   reconstruction PSNR: %.2fdB\n" % sm.psnr(S, Sr))


# Display representation and reconstructed image
fig1 = plot.figure(1, figsize=(14,14))
plot.subplot(2,2,1)
plot.imview(np.squeeze(np.sum(abs(X), axis=ams.cri.axisM)), fgrf=fig1,
            cmap=plot.cm.Blues, title='Representation')
plot.subplot(2,2,2)
plot.imview(S, fgrf=fig1, title='Reference image')
plot.subplot(2,2,3)
plot.imview(Sr, fgrf=fig1, title='Reconstructed image')
plot.subplot(2,2,4)
plot.imview(W[...,np.newaxis] * Sr, fgrf=fig1,
            title='Masked reconstructed image')
fig1.show()


# Display mask and additive mask component
fig2 = plot.figure(2, figsize=(14,7))
plot.subplot(1,2,1)
plot.imview(W, fgrf=fig2, cmap=plot.cm.Blues, title='Mask')
plot.subplot(1,2,2)
plot.imview(ams.cbpdn.Y[ams.index_addmsk()].squeeze(), fgrf=fig2,
            title='AMS component')
fig2.show()


# Plot functional value, residuals, and rho
its = ams.getitstat()
fig3 = plot.figure(3, figsize=(21,7))
plot.subplot(1,3,1)
plot.plot(its.ObjFun, fgrf=fig3, xlbl='Iterations', ylbl='Functional')
plot.subplot(1,3,2)
plot.plot(np.vstack((its.PrimalRsdl, its.DualRsdl)).T, fgrf=fig3,
          ptyp='semilogy', xlbl='Iterations', ylbl='Residual',
          lgnd=['Primal', 'Dual'])
plot.subplot(1,3,3)
plot.plot(its.Rho, fgrf=fig3, xlbl='Iterations', ylbl='Penalty Parameter')
fig3.show()


# Wait for enter on keyboard
input()
