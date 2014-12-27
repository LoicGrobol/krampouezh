Krampouezh
=======

A smooth 1d interpolator

## Running

    python3 krampouezh.py --help

Should tell you all you need to know. E.g.

    $ python3 krampouezh.py -ttikz "(0,0)" "(5,2)" "(7,1)" "(10,0)"
      \draw[smooth,samples=100,domain=0.0:5.0] plot(\x,{+0.7431372549019608*(\x-0.0)^(1)-0.013725490196078433*(\x-0.0)^(3)});
      \draw[smooth,samples=100,domain=5.0:7.0] plot(\x,{2.0-0.28627450980392155*(\x-5.0)^(1)-0.2058823529411765*(\x-5.0)^(2)+0.04950980392156864*(\x-5.0)^(3)});
      \draw[smooth,samples=100,domain=7.0:10.0] plot(\x,{1.0-0.515686274509804*(\x-7.0)^(1)+0.0911764705882353*(\x-7.0)^(2)-0.010130718954248366*(\x-7.0)^(3)});


## Dependencies

  - Python 3
  - Matplotlib (and Python 3 bindings)
  - Scipy/Numpy for Python 3
  
So for the lazy ubuntu users, that will be

    sudo apt-get install python3-scipy python3-numpy python3-matplotlib


## Licence

Useless details in LICENCE. All you should need to know
is that it is released under the WTFPL Version 2 as published by Sam Hocevar
at http://www.wtfpl.net.