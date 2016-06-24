#!/usr/bin/python
import numpy as np
from pytipsy import wtipsy
from sys import argv

if __name__ == "__main__":
    infile = open('glass.dat').readlines()
    bsize = float(argv[3])
    h = {'time':0, 'n':len(infile)+1, 'ndim':3, 'ngas':len(infile), 'ndark':0, 'nstar':1}
    gx = [bsize*(float(i.split()[0])-0.5) for i in infile]
    gy = [bsize*(float(i.split()[1])-0.5) for i in infile]
    gz = [bsize*(float(i.split()[2])-0.5) for i in infile]
    gtemp = float(argv[4])*np.ones(len(infile))
    gmass = float(argv[1])*np.ones(len(infile))
    zeros = gmass*0
    metals = 0.0132*np.ones(len(infile))
    gas = {'mass':gmass, 'x':gx, 'y':gy, 'z':gz, 'vx':zeros, 'vy':zeros, 'vz':zeros, 
        'dens':zeros, 'tempg':gtemp, 'h':zeros, 'zmetal':metals, 'phi':zeros}
    stars = {'mass':[float(argv[2])], 'x':[0], 'y':[0], 'z':[0], 'vx':[0], 'vy':[0], 'vz':[0], 
        'tform':[0], 'eps':[0], 'metals':[0.0132], 'phi':[0]}
    wtipsy('onestar.std', h, gas, None, stars)
