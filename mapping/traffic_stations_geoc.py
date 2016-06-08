#!/usr/bin/env python
# -*- coding: utf-8 -*-

# reads stations etrs N,E coordinates -> geographic stuff

import numpy as np


infile = "../metadata/csv/meta_traffic_stations.csv"
outfile = "./meta_traffic_stations_latlon.csv"


# constants

A1 = 6367449.145771
k0 = 0.9996
lamb0 = 27.0 * np.pi / 180.0
E0 = 500000.0

h1 = 0.000837732168164
h2 = 0.000000059058696
h3 = 0.000000000167349
h4 = 0.000000000000217

def sech(x):
    return 1.0/np.cosh(x)

def transfrom(N, E):
    N = np.float(N)
    xi = N/(A1*k0)
    eta = (E-E0)/(A1*k0)
    print xi, eta
    xip1 = h1*np.sin(2*xi)*np.cosh(2*eta)
    xip2 = h2*np.sin(4*xi)*np.cosh(4*eta)
    xip3 = h3*np.sin(6*xi)*np.cosh(6*eta)
    xip4 = h4*np.sin(8*xi)*np.cosh(8*eta)
    print xip1, xip2, xip3, xip4
    etap1 = h1*np.cos(2*xi)*np.sinh(2*eta)
    etap2 = h2*np.cos(4*xi)*np.sinh(4*eta)
    etap3 = h3*np.cos(6*xi)*np.sinh(6*eta)
    etap4 = h4*np.cos(8*xi)*np.sinh(8*eta)
    print etap1, etap2, etap4, etap4
    xip  = xi-xip1-xip2-xip3-xip4
    etap = eta-etap1-etap2-etap3-etap4
    print xip, etap
    beta = np.arcsin(sech(etap)*np.sin(xip))
    l = np.arcsin(np.tanh(etap)/np.cos(beta))
    print beta, l
    Q = np.arcsinh(np.tan(beta))
    print Q
    #e = np.e # ??
    e = np.sqrt(0.006694380023)
    Qp = Q + e*np.arctanh(e*np.tanh(Q))

    for i in xrange(3):
        Qp = Q + e*np.arctanh(e*np.tanh(Qp))

    print Qp

    rhoo = np.arctan(np.sinh(Qp))
    lamb = lamb0 + l
    return rhoo*180.0/np.pi, lamb*180.0/np.pi

with open(infile, 'r') as inf:
    ilines = [l.split(';') for l in inf]

headers = ilines[0]
meta = [l[0:4] for l in ilines[1:]]
etrs_coords = [(int(l[-4]), (l[-3])) for l in ilines[1:]]
outlines = []
for m, etrs in zip(meta,etrs_coords):
    x = float(etrs[0])
    y = float(etrs[1])
    l = m[:]
    lat, lon = transfrom(x,y)
    l.extend((str(lat),str(lon)))
    outlines.append(l)

str = ';'.join(headers[0:4]) + ';'
str += 'lat;lon;\n'
for o in outlines:
    str += ';'.join(o) + ';\n'
with open(outfile, 'w') as ouf:
    ouf.write(str)
