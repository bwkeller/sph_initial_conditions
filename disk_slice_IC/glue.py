#!/usr/bin/env python
import numpy as np
from pytipsy import wtipsy, rtipsy
from sys import argv

if __name__ == "__main__":
    h,g,d,s = rtipsy(argv[1])
    width = g['x'].max()
    h['n'] *= 4
    h['ngas'] *= 4
    for field in ['mass', 'z', 'vx', 'vy', 'vz', 'dens', 'tempg', 'h', 'zmetal', 'phi']:
        g[field] = np.concatenate([g[field]]*4)
    g['x'] = np.concatenate((g['x']-width, g['x']-width, g['x']+width, g['x']+width))
    g['y'] = np.concatenate((g['y']-width, g['y']+width, g['y']-width, g['y']+width))
    wtipsy("glued_"+argv[1],h,g,d,s)
