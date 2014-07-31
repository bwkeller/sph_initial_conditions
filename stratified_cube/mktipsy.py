#!/usr/bin/python
from sys import argv
from progressbar import ProgressBar
import numpy as np
from pytipsy import wtipsy
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def stretch(res, totalmass):
	print "Making %d^3 Disk Slice" % res
	h = {'time':0, 'n':res**3, 'ndim':3, 'ngas':res**3, 'ndark':0, 'nstar':0}
	ones = np.ones(res**3)
	zeros = np.zeros(res**3)
	gx = np.zeros(res**3)
	gy = np.zeros(res**3)
	gz = np.zeros(res**3)
	gtemp = np.zeros(res**3)
	print "Loading Glass File"
	infile = np.loadtxt('glass.dat', dtype={'names':('x','y','z'), 'formats':('f8', 'f8', 'f8')})
	print "Done!"
	print "Loading Density File"
	dfile = np.loadtxt('densities.dat')
	print "Done!"
	column_densities = dfile[:,2]
	#Normalize
	column_densities = column_densities/column_densities[-1]
	heights = dfile[:,0]
	temps = dfile[:,3]
	inv_column_func = interpolate.interp1d(column_densities, heights, kind='linear', bounds_error=False, fill_value=0)
	temp_func = interpolate.interp1d(heights, temps, kind='linear', bounds_error=False, fill_value=1e4)
	infile['z'] *= -1.0
	scoords = np.sort(infile, order=['z'])
	x = scoords['x']
	y = scoords['y']
	z_i = -1.0*scoords['z']
	wheres = np.where(z_i < 0.5)
	x = x[wheres]
	y = y[wheres]
	z_i = z_i[wheres]
	z_i_sorted = z_i
	progress = ProgressBar()
	print "Generating Bottom Half"
	ifrac = np.arange(len(z_i_sorted))/float(len(z_i))
	gx = x.copy()
	gy = y.copy()
	z_f = inv_column_func(ifrac)
	gtemp = temp_func(z_f)
	gz = z_f/-3.085e21
	infile['z'] *= -1.0
	scoords = np.sort(infile, order=['z'])
	x = scoords['x']
	y = scoords['y']
	z_i = scoords['z']
	wheres = np.where(z_i > 0.5)
	x = x[wheres]
	y = y[wheres]
	z_i = z_i[wheres]
	z_i_sorted = np.sort(z_i)
	progress = ProgressBar()
	print "Generating Top Half"
	ifrac = np.arange(len(z_i_sorted))/float(len(z_i))
	gx = np.append(gx,x.copy())-0.5
	gy = np.append(gy,y.copy())-0.5
	z_f = inv_column_func(ifrac)
	gtemp = np.append(gtemp,temp_func(z_f))
	gz = np.append(gz,z_f/3.085e21)
	gas = {'mass':ones*totalmass/res**3, 'x':2*gx, 'y':2*gy, 'z':gz, 'vx':zeros, 'vy':zeros, 'vz':zeros, 'dens':zeros, 'tempg':gtemp, 
			'h':zeros, 'zmetal':0.0132*ones, 'phi':zeros}
	wtipsy('stratified_cube.std', h,gas,None,None)

if __name__ == "__main__":
	stretch(int(argv[1]), float(argv[2]))
