'''
@author: Loïc Grobol <loic.grobol@gmail.com>
Copyright © 2014, Loïc Grobol <loic.grobol@gmail.com>
Permission is granted to Do What The Fuck You Want To
with this document.

See the WTF Public License, Version 2 as published by Sam Hocevar
at http://www.wtfpl.net if you need more details.

A smooth interpolation utility.
'''

import itertools as it
import libinterpol

def piecewise_latex(bounds, functions):
  '''Return LaTeX code to display a function defined piecewise on intervals
     delimited by `bounds` by `functions`.'''
  return ' + '.join('\\left({0}\\right)⋅𝟙_{{\\left[{1:f},{2:f}\\right[}}'.format(f,a,b)
                      for f,a,b in zip(functions,bounds[:-1],bounds[1:]))

def piecewise_geogebra(bounds, functions):
  '''Return Geogebra code to display a function defined piecewise on intervals
     delimited by `bounds` by `functions`.'''
  b = sorted(bounds)
  return 'Function[{0},{1},{2}]'.format(
					'+'.join('If[x>={1:f} && x<{2:f},{0},0]'.format(f,a,b)
					    for f,a,b in zip(functions,b[:-1],b[1:])),
					b[0],
					b[-1])

def polynomial(coefs, indeterminate='x', times=''):
  '''Return the representation of the polynomial with coefs `coefs`.
  
    >>> polynomial((1,2,3), 'y', '×')
    '1+2×y^2+3×y^3'
  '''
  return str(coefs[0]) + ''.join('{0:+f}{1}{2}^{3:d}'.format(c,t,i,p)
			      for c,t,i,p in zip(coefs[1:],it.repeat(times), it.repeat(indeterminate), it.count(1)))

def interpol_geogebra(points: '((x₀,y₀),(x₁,y₁),…)'):
  x,y = zip(*sorted(points))
  coefs = list(libinterpol.cubic_coefs(points))
  functions = (polynomial(c,'(x{0:+d})'.format(-x0)) for c,x0 in zip(coefs,x))
  return piecewise_geogebra(x,functions)
  
print(interpol_geogebra(((0,-2),(1,1),(2,4),(6,-1),(-2,1))))