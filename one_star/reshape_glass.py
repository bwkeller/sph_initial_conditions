#!/usr/bin/python
from sys import argv
from random import random
from progressbar import ProgressBar
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":
	res = int(argv[1])/16
	infile = open('glass_016.dat').readlines()
	outfile = open('glass.dat', 'w')
	subglass = [map(lambda x: float(x), i.split()) for i in infile]
	progress = ProgressBar()
	for x,y,z in progress(subglass):
		for i in range(res):
			for j in range(res):
				for k in range(res):
					outfile.write("%f\t%f\t%f\n" % ((x+i)/float(res), (y+j)/float(res),
					(z+k+0.00001*random())/float(res)))
