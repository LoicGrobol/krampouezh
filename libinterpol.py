'''
@author: Loïc Grobol <loic.grobol@gmail.com>
Copyright © 2014, Loïc Grobol <loic.grobol@gmail.com>
Permission is granted to Do What The Fuck You Want To
with this document.

See the WTF Public License, Version 2 as published by Sam Hocevar
at http://www.wtfpl.net if you need more details.

This provides the maths for the interpolation, and a few
goodies as well, such as a crude graphical output using matplotlib
shamelessly stolen in [scipy's doc][1].

There is also a naive implementation of the cubic interpolation
using the method described in [Piecewise polynomial interpolation][IWA13].

 [1]: http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d
 [IWA13]: http://www.opengamma.com/blog/piecewise-polynomial-interpolation
'''

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.sparse.linalg import spsolve


def cubic_interpol(points: '((x₀,y₀),(x₁,y₁),…)'):
  '''Return the piecewise cubic interpolation of `points`.'''
  x, y = zip(*points)
  return interp1d(x, y, kind='cubic')
  

def cubic_coefs(points: '((x₀,y₀),(x₁,y₁),…)') -> '((a₀¹,a₁¹,a₂¹,a₃¹),(a₀²,a₁²,a₂²,a₃³),…)':
  '''Return the coefficients of the piecewise cubic interpolation of `points`.
     Based on [Piecewise polynomial interpolation][IWA13].
     
     [IWA13]: http://www.opengamma.com/blog/piecewise-polynomial-interpolation'''
     
  x, y = map(np.array,zip(*sorted(points)))
  h = x[1:]-x[:-1]
  s = (y[1:]-y[:-1])/h
  sub = np.concatenate((h[:-1],[0]))
  super = np.concatenate(([0],h[1:]))
  main = np.concatenate(([1],2*(h[:-1]+h[1:]),[1]))
  A = sp.sparse.diags((sub,main,super),(-1,0,1),format='csr')
  b = 6*np.concatenate(([0],s[1:]-s[:-1],[0]))
  m = spsolve(A,b)
  a0 = y
  a1 = s - m[:-1]*h/2 - h*(m[1:]-m[:-1])/6
  a2 = m/2
  a3 = (m[1:]-m[:-1])/(6*h)
  return zip(a0,a1,a2,a3)
  
 
def plot_interpol(points: '((x₀,y₀),(x₁,y₁),…)', interpol=cubic_interpol, samples=100):
  '''Display a crude graphical output of the cubic interpolation using matplotlib.'''
  x, y = zip(*points)
  f = interpol(points)
  xnew = np.linspace(min(x), max(x), samples)
  plt.plot(x,y,'o',xnew,f(xnew),'-')
  plt.legend(['data', 'cubic'], loc='best')
  plt.show()
  

if __name__=='__main__':
  print(list(cubic_coefs(((0,-2),(3,1),(2,7),(1,3),(5,-6)))))
  plot_interpol(((0,-2),(3,1),(2,7),(1,3),(5,-6)))

