'''
@author: Loïc Grobol <loic.grobol@gmail.com>
Copyright © 2014, Loïc Grobol <loic.grobol@gmail.com>
Permission is granted to Do What The Fuck You Want To
with this document.

See the WTF Public License, Version 2 as published by Sam Hocevar
at http://www.wtfpl.net if you need more details.

A naïve syntax tree to help format function definitions for several engines.

Plans are for support of
  - Python
  - LaTeX maths
  - Geogebra
  - Pgf/TikZ
'''

import itertools as it
import numbers
import copy

class Term:
    def __add__(self, y):
        z = Scalar(y) if isinstance(y, numbers.Number) else y
        return Sum((self, z))
   
    def __neg__(self):
        return Minus(self)
        
    def __sub__(self, y):
        z = Scalar(y) if isinstance(y, numbers.Number) else y
        return self + (-z)
        
    def __pow__(self, n):
        m = Scalar(n) if isinstance(n, numbers.Number) else n
        return Power(self, m)
    
    def __mul__(self, y):
        z = Scalar(y) if isinstance(y, numbers.Number) else y
        return Scale(self, z)

    def __radd__(self, y):
        z = Scalar(y) if isinstance(y, numbers.Number) else y
        return Sum((z, self))
        
    def __rsub__(self, y):
        z = Scalar(y) if isinstance(y, numbers.Number) else y
        return z + (-self)
    
    def __rmul__(self, y):
        z = Scalar(y) if isinstance(y, numbers.Number) else y
        return Scale(z, self)
        
    def simplify(self):
        return copy.deepcopy(self)
        
class Sum(Term):
    def __init__(self, summands):
        self.summands = tuple(summands)

    def __str__(self):
        return '({})'.format('+'.join(('{}'.format(s) for s in self.summands)))

    def latex(self):
        return '({})'.format('+'.join(('{}'.format(s.latex()) for s in self.summands)))

    def geogebra(self):
        return '({})'.format('+'.join(('{}'.format(s.geogebra()) for s in self.summands)))
        
    def pgf(self):
        return '({})'.format('+'.join(('{}'.format(s.pgf()) for s in self.summands)))
        
    def value(self, *args, **kwargs):
        return sum(s.value(*args, **kwargs) for s in self.summands)
    
    def simplify(self):
        su = tuple(s.simplify() for s in self.summands)
        return Sum((s for s in su if not ((isinstance(s,  Scalar) and s.scalar == 0) or s == 0)))
    
    
class Scale(Term):
    def __init__(self, scale, vector):
        self.scale = scale
        self.vector = vector

    def __str__(self):
        return '({scale}*{vector})'.format(**self.__dict__)
        
    def geogebra(self):
        return '({scale}*{vector})'.format(**{a: self.__dict__[a].geogebra() for a in self.__dict__})

    def latex(self):
        return '({scale}*{vector})'.format(**{a: self.__dict__[a].latex() for a in self.__dict__})
        
    def pgf(self):
        return '({scale}*{vector})'.format(**{a: self.__dict__[a].pgf() for a in self.__dict__})
        
    def value(self, *args, **kwargs):
        return self.scale.value(*args, **kwargs)*self.vector.value(*args, **kwargs)
    
    def simplify(self):
         s, v = self.scale.simplify(),  self.vector.simplify()
         if isinstance(s, Scalar) and s.scalar == 0 or s == 0:
            return Integer(0)
         if isinstance(s, Scalar) and s.scalar == 1 or s == 1:
            return v
         if isinstance(v, Scalar) and v.scalar == 0 or v == 0:
            return Integer(0)
         if isinstance(v, Scalar) and v.scalar == 1 or v == 1:
            return s
         return Scale(self.scale.simplify(),  self.vector.simplify())
        
        
class Scalar(Term):
    def __init__(self, scalar):
        self.scalar = scalar

    def __str__(self):
        return str(self.scalar)
        
    def value(self, *args, **kwargs):
        return self.scalar

    geogebra = __str__
    pgf = __str__
    latex = __str__
    

class Integer(Scalar):
    pass


class Minus(Term):
    def __init__(self, val):
        self.val = val
        
    def __str__(self):
        return '(-({}))'.format(self.val)
        
    def geogebra(self):
        return '(-({}))'.format(self.val.geogebra())

    def latex(self):
        return '(-({}))'.format(self.val.latex())
        
    def pgf(self):
        return '(-({}))'.format(self.val.pgf())
        
    def value(self, *args, **kwargs):
        return -self.val.value(*args, **kwargs)
    
    def simplify(self):
        v = self.val.simplify()
        if isinstance(v,  Minus): # -(-a)
            return v.val.simplify()
        if (isinstance(v,  Scalar) and v.scalar == 0) or v == 0: # -0
            return Integer(0)
        if isinstance(v,  Scalar) and hasattr(v.scalar, '__neg__'): # -Scalar(a) pour a négatif
            try:
                if v.scalar<0:
                    return Scalar(-v.scalar)
            except TypeError:
                pass
        return Minus(v)
        
        
class Variable(Term):
    def __init__(self, varname='x'):
        self.varname = varname

    def __str__(self):
        return self.varname        

    geogebra = __str__
    
    def pgf(self):
        return r'\{}'.format(self.varname)
        
    latex = __str__
    
    def value(self, *args, **kwargs):
        return kwargs[self.varname]
        

class Power(Term):
    def __init__(self, var, power):
        self.var = var
        self.power = power

    def __str__(self):
        return '({var}**{power})'.format(**self.__dict__)
        
    def geogebra(self):
        return '({var}^{power})'.format(**{a: self.__dict__[a].geogebra() for a in self.__dict__})

    def latex(self):
        return '({var}^{{{power}}})'.format(**{a: self.__dict__[a].latex() for a in self.__dict__})
        
    def pgf(self):
        return '({var}^{power})'.format(**{a: self.__dict__[a].pgf() for a in self.__dict__})
        
    def value(self, *args, **kwargs):
        return self.var.value(*args, **kwargs)**self.power.value(*args, **kwargs)
        
    def simplify(self):
        v, p = self.var.simplify(),  self.power.simplify()
        if (isinstance(p, Scalar) and p.scalar == 0) or p == 0: # a^0
            return Integer(1)
        if (isinstance(p, Scalar) and p.scalar  == 1) or p == 1: # a^1
            return v.simplify()
        if (isinstance(v, Scalar) and v.scalar  == 0) or v == 0: # 0^a (since 0^0 has already been dealt with)
            return Integer(0)
        return Power(v.simplify(), p.simplify())
        

class RealFun(Term):
    def __init__(self, a, b, image, variable):
        self.a = Scalar(a) if isinstance(a, numbers.Number) else a
        self.b = Scalar(b) if isinstance(b, numbers.Number) else b
        self.image = image
        self.variable = variable
    
    def __str__(self):
        return r'''def f({variable}):
    if {a}<={variable}<={b}:
        return {image}
    else:
        raise DomainError()'''.format(**self.__dict__)
        
    def geogebra(self):
        return 'Function[{a}, {b}, {image}]'.format(**{a: self.__dict__[a].geogebra() for a in self.__dict__})
    
    def pgf(self):
        return r'\draw[smooth,samples=100,domain={a}:{b}] plot({variable},{{{image}}});'.format(**{a: self.__dict__[a].pgf() for a in self.__dict__})
    
    def latex(self):
        return '{variable}⟼{image}'.format(**{a: self.__dict__[a].latex() for a in self.__dict__})
        
    def value(self, *args, **kwargs):
        if not (self.a.value(*args, **kwargs) <= self.variable.value(*args, **kwargs) <=  self.b.value(*args, **kwargs)):
            raise DomainError()
        return self.image.value(*args, **kwargs)
        
    def simplify(self):
        return RealFun(self.a.simplify(), self.b.simplify(),  self.image.simplify(),  self.variable.simplify())
        

class Indicator(Term):
    '''Indicator of [a,b[ (𝟙_{[a,b[}).'''
    def __init__(self, a, b, variable):
        self.a = Scalar(a) if isinstance(a, numbers.Number) else a
        self.b = Scalar(b) if isinstance(b, numbers.Number) else b
        self.variable = variable
        
    def __str__(self):
        return '(1 if {a} <= {variable} < {b} else 0)'.format(**self.__dict__)
        
    def geogebra(self):
        return '(If[x>={a} && x<{b},{variable},0])'.format(**{a: self.__dict__[a].geogebra() for a in self.__dict__})
        
    def latex(self):
        return r'𝟙_{{\left[{a}, {b}\right[}}({variable})'.format(**{a: self.__dict__[a].latex() for a in self.__dict__})
        
    def pgf(self):
        return 'and({variable}>={a},{variable}<{b})'.format(**{a: self.__dict__[a].pgf() for a in self.__dict__})
        
    def value(self, *args, **kwargs):
        return 1 if self.a.value(*args, **kwargs) <= self.variable.value(*args, **kwargs) < self.b.value(*args, **kwargs) else 0
        
    def simplify(self):
        return Indicator(self.a.simplify(), self.b.simplify(), self.variable.simplify())


class DomainError(Exception):
    pass
    
    
def piecewise_polynomial(variable, coefs, bounds):
    bounds = sorted(list(bounds))
    img = Sum(Sum(c*(variable-a)**i for c,i in zip(piece_coefs,it.count()))*Indicator(a,b,variable) for a,b,piece_coefs in zip(bounds[:-1],bounds[1:],coefs))
    return RealFun(Scalar(bounds[0]), Scalar(bounds[-1]), img, variable)
        
def tree_fun(tree, *vars):
    '''Return a callable that returns the evaluation of `tree` after the substitution of
       `vars`. That is `tree_fun(tree, ('x', 'y'))(2,5)` is `tree.value({'x': 2, 'y':5})`.'''
    def f(*vals):
        return tree.value({x: y for x,y in zip(vars, vals)})
    return f

if __name__=='__main__':
    x = Variable()
    import libinterpol
    c = list(libinterpol.cubic_coefs(((0,0),(5,2),(7,1),(10,0))))
    f = piecewise_polynomial(x, c, (0,2,3,1,5))
    print(f.simplify().pgf())

