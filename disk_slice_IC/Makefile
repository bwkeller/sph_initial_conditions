#This makefile will generate the stratified disk, along with parameter files needed to work with it.
#Files needed to start the generation are kept in dep.  Output will be dumped in the current directory.
RES = 128#The resolution of the IC, will be this many particles cubed. Must be 3 digits (ie, 16 is 016)
TURBRMS = 10#The RMS Turbulent velocity in km/s
TOTALMASS = 9.84*10^6#The total mass of the box in solar masses.  Probably shouldn't change this unless you know what's what.

#By default, generate the turbulent and nonturbulent versions of the stratified disk 
default: turbulent_stratified_disk.std stratified_disk.param turbulent_stratified_disk.param 

#Generate the density/temperature/z-height profiles
densities.dat: 
	g++ dep/generaterho.c
	./a.out | tail --lines=+2 > densities.dat
	rm a.out

#Make a glass at the desired resolution
glass.dat:
	@cp dep/glass_016.dat .
	python reshape_glass.py $(RES)
	@rm glass_016.dat

#Make parameter files
stratified_disk.param:
	@cp dep/diskslice.param stratified_disk.param
	sed -i -e 's/FILE/stratified_disk/g' stratified_disk.param
	sed -i -e "s/MASS/`echo 'scale=10; 2*$(TOTALMASS)*$(RES)^-3' | bc`/" stratified_disk.param
	sed -i -e "s/MIN/`echo 'scale=10; 0.2*$(TOTALMASS)*$(RES)^-3' | bc`/" stratified_disk.param

turbulent_stratified_disk.param:
	@cp dep/diskslice.param turbulent_stratified_disk.param
	sed -i -e 's/FILE/turbulent_stratified_disk/g' turbulent_stratified_disk.param
	sed -i -e "s/MASS/`echo 'scale=10; 2*$(TOTALMASS)*$(RES)^-3' | bc`/" turbulent_stratified_disk.param
	sed -i -e "s/MIN/`echo 'scale=10; 0.2*$(TOTALMASS)*$(RES)^-3' | bc`/" turbulent_stratified_disk.param

#Make a nonturbulent version of the  disk
stratified_disk.std: densities.dat glass.dat
	python mktipsy.py $(RES)

#Make a turbulent version of the  disk
turbulent_stratified_disk.std: stratified_disk.std
	@cp dep/vout.bin .
	python mkturbulent.py $(TURBRMS)
	@rm stratified_disk.std
	@rm vout.bin

clean:
	rm -f *.std glass.dat *densities.dat *.param
