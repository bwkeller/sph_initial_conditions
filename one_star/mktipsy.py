#!/usr/bin/python
import numpy as np
import pynbody as pyn
import matplotlib.pyplot as plt
from sys import argv
if __name__ == "__main__":
    infile = open('glass.dat').readlines()
    tipsy = pyn.new(gas=len(infile))
    bsize = 6
    tipsy.gas['x'] = [bsize*(float(i.split()[0])-0.5) for i in infile]
    tipsy.gas['y'] = [bsize*(float(i.split()[1])-0.5) for i in infile]
    tipsy.gas['z'] = [bsize*(float(i.split()[2])-0.5) for i in infile]
    tipsy.gas['temp'] = 1e-6
    tipsy.gas['mass'] = 0.005461863242089748*64
    tipsy.gas['metals'] = 0.0132*np.ones(len(infile))
    tipsy.properties['a'] = 0
    tipsy.write(filename="onestar.std", fmt=pyn.tipsy.TipsySnap)
