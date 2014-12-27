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

def polynomial(coefs, template='{coef:+f}x^{power:d}', constant_template='{coef}'):
  '''Return the representation of the polynomial with coefs `coefs`.
  
    >>> polynomial((1,2,3))
    '1+2x^2+3x^3'
    >>> polynomial((1,2,3), {0:+f}×y^({3:f})'
    '1+2×y^(1.0)+3×y^(2.0)'
  '''
  return ''.join(template.format(coef=c,power=p) if p != 0 else constant_template.format(coef=c) for c,p in zip(coefs,it.count()) if c != 0)

def interpol_geogebra(points: '((x₀,y₀),(x₁,y₁),…)'):
  '''Return a Geogebra definition of the interpolant of `points`.'''
  x,y = zip(*sorted(points))
  coefs = list(libinterpol.cubic_coefs(points))
  functions = (polynomial(c,'{{coef:+f}}*(x{0:+d})^{{power:d}}'.format(-x0)) for c,x0 in zip(coefs,x))
  return piecewise_geogebra(x,functions)

def piecewise_tikz(bounds, functions):
  '''Return TikZ code to display a function defined piecewise on intervals
     delimited by `bounds` by `functions`.'''
  b = sorted(bounds)
  return '\n'.join(r'\draw[smooth,samples=100,domain={1}:{2}] plot(\x,{{{0}}});'.format(f,a,b) for f,a,b in zip(functions,b[:-1],b[1:]))
  
def interpol_tikz(points: '((x₀,y₀),(x₁,y₁),…)'):
  '''Return a TikZ definition of the interpolant of `points`.'''
  x,y = zip(*sorted(points))
  coefs = list(libinterpol.cubic_coefs(points))
  functions = (polynomial(c,'{{coef:+f}}*(\\x{0:+d})^({{power:d}})'.format(-x0)) for c,x0 in zip(coefs,x))
  return piecewise_tikz(x,functions)
  
print(interpol_tikz(((0,1),(2,6),(3,-5),(7,0))))