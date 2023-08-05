# -*- coding: utf-8 -*-
def lorentzian(x, center, sigma, height):
    """
    Amplitude normalized Lorentzian distribution
    
    Parameters:
    ==========    
    x :
        Free variable
    center:
        Center of distribution in units of x
    sigma: 
        HWHM linewidth
    height: 
        Amplitude at x=center
        
    """
    return height/(1+((x-center)/sigma)**2)
