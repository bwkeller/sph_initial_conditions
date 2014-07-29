#include <stdio.h>
#include <math.h>

double verticalDiskLnTemperature(double zheight, double z0, double temperatureLow, double temperatureHigh)
{
  double variableFactor(1);
  const double lnFactor(log(temperatureHigh/temperatureLow));
  if (zheight < z0/2)
    variableFactor = 2*zheight*zheight/z0/z0;
  else if (zheight < z0)
    variableFactor = 1 - 2 * (pow(1-zheight/z0, 2));
  return variableFactor*lnFactor + log(temperatureLow);
}

double dlnTbydz(double zheight, double z0, double temperatureLow, double temperatureHigh)
{
  double variableFactor(0);
  const double lnFactor(log(temperatureHigh/temperatureLow)); // log(10^6) - log(10^4)
  if (zheight < z0/2)
    variableFactor = 4*zheight/z0/z0;
  else if (zheight < z0)
    variableFactor = 4 * (1-zheight/z0)/z0;
  return variableFactor*lnFactor;
}

double u2primed(double u1, double u2, double zheight, double z0, double temperatureLow, double temperatureHigh, double vc, double R)
{
  static const double fourPiG(4*3.1415*6.67e-8);
  static const double mbarbykb(0.6*1.67e-24/1.38e-16);
  static const double vc2(vc*vc);
  static const double R2(R*R);
  const double temperature(exp(verticalDiskLnTemperature(zheight, z0, temperatureLow, temperatureHigh)));
  return(-(u2*(dlnTbydz(zheight, z0, temperatureLow, temperatureHigh)+mbarbykb/temperature*(vc2*zheight/(R2+zheight*zheight)+fourPiG*u1))));
}

void densityAtZ(double& u1, double& u2, double zheight, double z0, double deltazheight, double temperatureLow, double temperatureHigh, double vc, double R)
{
  const int numberOfSteps(1000);
  const double stepSize(deltazheight/numberOfSteps);
  for (int count = 0; count < numberOfSteps; ++count)
  {
    // fourth-order Runge-Kutta and coupled equations - u1primed can be optimized as u2, but the logic is clear here
    const double k1(stepSize*u2);
    const double l1(stepSize*u2primed(u1, u2, zheight, z0, temperatureLow, temperatureHigh, vc, R));
    const double k2(stepSize*u2);
    const double l2(stepSize*u2primed(u1+k1/2, u2+l1/2, zheight+stepSize/2, z0, temperatureLow, temperatureHigh, vc, R));
    const double k3(stepSize*u2);
    const double l3(stepSize*u2primed(u1+k2/2, u2+l2/2, zheight+stepSize/2, z0, temperatureLow, temperatureHigh, vc, R));
    const double k4(stepSize*u2);
    const double l4(stepSize*u2primed(u1+k3, u2+l3, zheight+stepSize, z0, temperatureLow, temperatureHigh, vc, R));
    u1 += (k1+2*k2+2*k3+k4)/6;
    u2 += (l1+2*l2+2*l3+l4)/6;
  }
}
int main()
{
//Output is in cgs
	double vc = 220*1e5;
	double R = 6*3.09e21;
	double z0 = 1.1*3.09e21;
	double temperatureLow = 1e4;
	double temperatureHigh = 1e6;
	double u1 = 0;
	double u2 = 2*1.67e-24;
	double T;
	printf("zheight density column_density temperature\n");
	for (int i=0; i<400000; i++)
	{
		T = exp(verticalDiskLnTemperature(double(i)*0.00002*3.09e21, z0, temperatureLow, temperatureHigh));
		densityAtZ(u1, u2, double(i)*0.00002*3.09e21, z0, 0.00002*3.09e21, temperatureLow, temperatureHigh, vc, R);
		printf("%e %e %e %e\n", double(i)*0.00002*3.09e21,  u2, u1, T);
	}
	return 0;
}
