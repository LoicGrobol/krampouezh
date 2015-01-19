#!/usr/bin/env python3

'''
@author: Loïc Grobol <loic.grobol@gmail.com>
Copyright © 2014, Loïc Grobol <loic.grobol@gmail.com>
Permission is granted to Do What The Fuck You Want To
with this document.

See the WTF Public License, Version 2 as published by Sam Hocevar
at http://www.wtfpl.net if you need more details.

A smooth interpolation utility.
'''

from libkrampouezh import libinterpol
from libkrampouezh import naive_tree
import sys
import argparse


def main(args=sys.argv[1:]):
    out_formats=('pgf', 'geogebra', 'latex', 'gui')
    # The usual argparse recipe
    parser = argparse.ArgumentParser(description="A 1D interpoler with convenient output formats.")
    parser.add_argument('-t', '--format', choices=out_formats, default=out_formats[0],
			help='Output format (default: %(default)s)')
    sub = parser.add_subparsers()
    
    cubic = sub.add_parser('cubic', help='Interpolation using natural cubic splines.')
    cubic.add_argument('points', nargs='+', help='The points to interpol in the format `(x,y)`. At least 3.')
    cubic.set_defaults(interpol=libinterpol.cubic_coefs)
    
    hermite = sub.add_parser('hermite', help='Interpolation using cubic Hermite splines.')
    hermite.add_argument('points', nargs='+', help="The points to interpol in the format `(x,y,y')`. At least 2.")
    hermite.set_defaults(interpol=libinterpol.hermite_coefs)
    
    args = parser.parse_args(args)
    points = tuple(tuple(float(f) for f in s[1:-1].split(',')) for s in args.points)
    if args.format == 'gui':
        libinterpol.plot_interpol(tuple(p[:2] for p in points))
    else:
        out = getattr(naive_tree.piecewise_polynomial(naive_tree.Variable(), args.interpol(points), (p[0] for p in points)), args.format)()
        print(out)
    
if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))
