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
    '''Return the coefficients of the piecewise natural cubic interpolation of `points`.
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
  
  
def hermite_coefs(points: "((x₀,y₀,y₀'),(x₁,y₁,y₁'),…)") -> '((a₀¹,a₁¹,a₂¹,a₃¹),(a₀²,a₁²,a₂²,a₃³),…)':
    '''Return the coefficients of the piecewise cubic hermit interpolation of `points`.
   
    See [the corresponding — and well-written — Wikipedia entry][WIKHE]. From it we can
    infer that the interpoling polynomial on $[xᵢ,xᵢ₊₁]$ is 
    
    $$P∘\frac{X-xᵢ}{xᵢ₊₁-xᵢ}$$
    where $P$ is
    $$P = (2yᵢ−2yᵢ₊₁+(xᵢ₊₁−xᵢ)yᵢ'+(xᵢ₊₁−xᵢ)yᵢ₊₁')X³+(−3yᵢ+3yᵢ₊₁-2(xᵢ₊₁−xᵢ)yᵢ'-(xᵢ₊₁−xᵢ)yᵢ₊₁')X²+(xᵢ₊₁−xᵢ)yᵢ'X+yᵢ$$
    
    So the coefficients of $P$ (in decreasing powers) are the components of
    $$
      [[ 2 -2  1  1]    [[yᵢ]
       [-3  3 -2 -1]  ×  [yᵢ₊₁] 
       [ 0  0  1  0]     [yᵢ']
       [ 1  0  0  0]]    [yᵢ₊₁']]
    $$
    That we vectorise into $H×P$ where $H$ is the above Hermite matrix and $P$ is simply
    $$
      [[y₀  y₁  …]
       [y₁  y₂  …]
       [y₀' y₁' …]
       [y₁' y₂' …]]
    $$
    After wich we just renormalise the coefficients by multiplying the first line of $HP$ by $(\frac{X-xᵢ}{xᵢ₊₁-xᵢ})³$,
    the second line by$(\frac{X-xᵢ}{xᵢ₊₁-xᵢ})²$… To use them, don't forget to apply the shift, too. E.g if you are
    interpoling on $[5,7]$, the coefficients returned by this function are those of the polynomial in $X-5$.
    
    [WIKHE]: https://en.wikipedia.org/wiki/Cubic_Hermite_spline#Interpolation_on_an_arbitrary_interval'''
     
    x, y, t = map(np.array,zip(*sorted(points)))
    H = np.array(((2,-2,1,1),(-3,3,-2,-1),(0,0,1,0),(1,0,0,0)))
    Δ = x[1:]-x[:-1]
    P = np.array((y[:-1],y[1:],Δ*t[:-1],Δ*t[1:]))
    coefs = H.dot(P)
    normaliser = np.array((1/Δ**3,1/Δ**2,1/Δ,1/Δ**0))

    normal_coefs = coefs * normaliser
    return (l[::-1] for l in normal_coefs.transpose().tolist())
  
  
def plot_interpol(points: '((x₀,y₀),(x₁,y₁),…)', interpol=cubic_interpol, samples=100):
    '''Display a crude graphical output of the cubic interpolation using matplotlib.'''
    x, y = zip(*points)
    f = interpol(points)
    xnew = np.linspace(min(x), max(x), samples)
    plt.plot(x,y,'o',xnew,f(xnew),'-')
    plt.legend(['data', 'cubic'], loc='best')
    plt.show()
  

if __name__=='__main__':
    print(list(hermite_coefs(((0,0,1),(5,0,0),(7,1,1)))))

