#This makefile will generate the stratified disk, along with parameter files needed to work with it.
#Files needed to start the generation are kept in dep.  Output will be dumped in the current directory.
RES = 032#The resolution of the IC, will be this many particles cubed. Must be 3 digits (ie, 16 is 016), a multiple of 16
TOTALMASS = 5.6e7#The total mass of the box in Msol.  For a surface density of 14 Msol/pc^2 (~MW value), use 5.6e7
BCMASS = 5.6*10^7#BC doesn't like the previous syntax.

default: stratified_cube.std stratified_cube.param

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
stratified_cube.param:
	@cp dep/diskslice.param stratified_cube.param
	sed -i -e 's/FILE/stratified_cube/g' stratified_cube.param
	sed -i -e "s/MASS/`echo 'scale=10; 2*$(BCMASS)*$(RES)^-3' | bc`/" stratified_cube.param
	sed -i -e "s/MIN/`echo 'scale=10; 0.2*$(BCMASS)*$(RES)^-3' | bc`/" stratified_cube.param

#Make a nonturbulent version of the  cube
stratified_cube.std: densities.dat glass.dat
	python mktipsy.py $(RES) $(TOTALMASS)

clean:
	rm -f *.std glass.dat *densities.dat *.param
