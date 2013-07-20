##############################################################################
# G10.py                                                                     #
# Author: Nicholas Huang                                                     #
# Material properties of G10                                                 #
##############################################################################
from materials import *

def cv(T):
    '''
    Thermal conductivity in W / m K
    '''

    if (not isinstance(T, np.ndarray)):
        T = np.array(T)

    if (np.any(T > 4.2)):
        print 'Warning: Temperature too high (valid range is .3 to 4.2 K)'
    if (np.any(T < .3)):
        print 'Warning: Temperature too low (valid range is .3 to 4.2 K)'
    
    alpha = 12.8e-3
    Beta = 2.41
    gamma = -9.21
    n = .222
    return bf.kt(T, alpha, Beta, gamma, n)
