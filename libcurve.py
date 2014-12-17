import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def cubic_interpol(points: '((x₀,y₀),(x₁,y₁),…)'):
  x, y = zip(*points)
  return interp1d(x, y, kind='cubic')

 
def plot_interpol(points: '((x₀,y₀),(x₁,y₁),…)', interpol=cubic_interpol, samples=100):
  x, y = zip(*points)
  f = interpol(points)
  xnew = np.linspace(min(x), max(x), samples)
  plt.plot(x,y,'o',xnew,f(xnew),'-')
  plt.legend(['data', 'cubic'], loc='best')
  plt.show()
  

plot_interpol(((0,-2),(3,1),(2,7),(1,3),(5,-6)))

