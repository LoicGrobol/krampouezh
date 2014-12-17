'''
@author: Loïc Grobol <loic.grobol@gmail.com>
Copyright © 2014, Loïc Grobol <loic.grobol@gmail.com>
Permission is granted to Do What The Fuck You Want To
with this document.

See the WTF Public License, Version 2 as published by Sam Hocevar
at http://www.wtfpl.net if you need more details.

This one is just a dirty estimator of the time it takes to compute
the coefficients of the cubic interpolation.
'''
import timeit
import libinterpol
import random

def test(n):
  l = [[(x,random.uniform(-10,10)) for x in range(n)] for i in range(100)]
  return sum(timeit.timeit('libinterpol.cubic_coefs({})'.format(s),'import libinterpol',number=100) for s in l)/100
  
print('\n'.join(str(test(i)) for i in range(3,10)))