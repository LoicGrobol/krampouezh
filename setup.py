from distutils.core import setup

setup(name='krampouezh',
      version='0.20150105',
      description='A smooth 1d interpolator',
      url='https://github.com/Evpok/krampouezh',
      author='Loïc Grobol', 
      author_email='loic.grobol@gmail.com',
      license='WTFPL',
      packages=['libkrampouezh'],
      install_requires=[ 'scipy','numpy','matplotlib'],
      scripts=['krampouezh.py'],)
