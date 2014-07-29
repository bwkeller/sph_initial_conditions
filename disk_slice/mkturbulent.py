#!/usr/bin/python

from pytipsy import rtipsy,wtipsy
import numpy as np
from scipy.interpolate import griddata
from sys import argv
import matplotlib.pyplot as plt

kmPerSecUnit = 0.00207403

if __name__ == "__main__":
	inbin = open('vout.bin', 'rb')
	velocities = np.reshape(np.fromstring(inbin.read(12*128**3), dtype=np.float32, count=3*128**3), (128,128,128,3))
	positions = np.reshape(np.swapaxes(np.indices((32,32,32))/32.0-0.5,0,3), (32**3,3))
	h,g,d,s = rtipsy("stratified_disk.std")
#These values need to be re-scaled!
	vel_x = velocities[::4,::4,::4,0]
	vel_y = velocities[::4,::4,::4,1]
	vel_z = velocities[::4,::4,::4,2]
	stdscale = float(argv[1])*kmPerSecUnit*np.std(np.sqrt(vel_x**2+vel_y**2+vel_y**2))
	print "Fitting x velocities"
	g['vx'] = griddata(positions, vel_x.flatten(), (g['x'], g['y'], g['z']), fill_value=0, method='linear')
	print "Fitting y velocities"
	g['vy'] = griddata(positions, vel_y.flatten(), (g['x'], g['y'], g['z']), fill_value=0, method='linear')
	print "Fitting z velocities"
	g['vz'] = griddata(positions, vel_z.flatten(), (g['x'], g['y'], g['z']), fill_value=0, method='linear')
	print "The std velocity is:"
	g['vx'] /= stdscale
	g['vy'] /= stdscale
	g['vz'] /= stdscale
	print np.std(np.sqrt(g['vx']**2+g['vy']**2+g['vz']**2))
	wtipsy("turbulent_stratified_disk.std", h,g,d,s)
