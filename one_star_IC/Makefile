#This makefile will generate the one star IC, along with parameter files needed to work with it.
#Files needed to start the generation are kept in dep.  Output will be dumped in the current directory.
RES = 128#The resolution of the IC, will be this many particles cubed. Must be 3 digits (ie, 16 is 016)
PMASS = 750#The mass per particle, in Msol
SMASS = 3e4#The star mass, in Msol
BSIZE = 5#The size of the box, in kpc
TEMP = 1e3#Gas temperature
default: onestar.std onestar.param


#Make a glass at the desired resolution
glass.dat:
	@cp dep/glass_016.dat .
	python reshape_glass.py $(RES)
	@rm glass_016.dat

#Make parameter files
onestar.param:
	@cp dep/onestar.param .
	sed -i -e 's/PERIOD/$(BSIZE)/g' onestar.param
	sed -i -e "s/MGMASS/`echo 'scale=10; 0.1*$(PMASS)' | bc`/" onestar.param


#Make a nonturbulent version of the hot disk
onestar.std: glass.dat
	python mktipsy.py $(RES) $(PMASS) $(SMASS) $(BSIZE) $(TEMP)

clean:
	rm -f *.std glass.dat *densities.dat *.param
