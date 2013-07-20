'''
Dummy file to make python think the materials directory is a module.
This allows importing like this:
>>> from materials import cf_rod

Modules:
--------
cf_rod.py : Carbon fiber rod
copper : oxygen-free high thermal conductivity copper
'''
import numpy as np
from scipy import interpolate

import materials.basefunctions as bf
