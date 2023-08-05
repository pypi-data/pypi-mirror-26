# -*- coding: utf-8 -*-
"""
Processing functions for pulsed EPR time-domain measurements.
"""

import numpy as np
from scipy import signal

# support versioning of processing operations; expose version of package
from bbfmr._version import get_versions
__version__ = get_versions()['version']
del(get_versions)

def filter_savitzky_golay(
        X=None, Y=None, Z=None,
        axis:
            {
            "type": "int",
            "min":0, "max": 1,
            "hint": "Axis along which the filter is applied."
            }=0,
        window_length:
            {
            "type": "int", 
            "min": 1
            }=5,
        polyorder:{
            "type": "int",
            "min":1
            }=1,
        deriv:
            {
            "type": "int",
            "min":0, 
            "hint": "The order of the derivative to compute. 0 means without differentiating."
            }=0,
        mode:{
            "type": "int",
            "min":0, 
            "max":4,
            "hint": "0:mirror, 1:constant, 2:nearest, 3:wrap, 4:interp"
            }=2
        ):
    """
    Smooths the data with a Savitzky-Golay-Filter. 
    See scipy.signal.savgol_filter for details.

    Params:
    =======
        window_length : 
            lenth of the filter window (i.e. number of coefficients), must be odd.
        polyorder : 
            order of the polynomial used to fit the samples, must be less than window_length.
        deriv : 
            order of the derivative to compute. If 0 then data is filtered without differentiating.
        mode :
            can be "mirror", "constant", "nearest", "wrap" or "interp".
    """
    
    if axis==1:
        Z=Z.T
    
    # FIXME: support lists as function annotation in gui
    if mode==0:
        filter_mode='mirror'
    elif mode==1:
        filter_mode='constant'
    elif mode==2:
        filter_mode='nearest'
    elif mode==3:
        filter_mode='wrap'
    elif mode==4:
        filter_mode='interp'
    
    # Window_length has to be odd. Therefore increase lengt by 1 if even:
    if window_length%2==0:
        window_length+=1
        
    # Polyorder always has to be smaller than window_length
    if polyorder>=window_length:
        polyorder=window_length-1
        
    filtered =  np.zeros_like(Z)
    for i in range(len(Z[:,0])-1):
        filtered[i, :] = signal.savgol_filter(Z[i,:], window_length, polyorder, deriv, mode=filter_mode)
        
    if axis == 1:
        filtered = filtered.T
        
    return X, Y, filtered

    
def filter_median(
        X=None, Y=None, Z=None,
        axis:
            {
            "type": "int",
            "min":0,
            "max": 1,
            "hint": "Axis along which the filter it applied."
            }=0,
        kernel_size:{
            "type": "int",
            "min": 1,
            "hint": "Size of filter window."
            }=3
        ):
    """
    Smooths the data with a Median-Filter. 
    See scipy.signal.medfilt for details.

    Params:
    =======
        axis : 
            axis along which the smoothing should be performed.
        kernel_size : 
            size of the smoothing window (has to be odd)
    """
    
    if axis==1:
        Z=Z.T
        
    if kernel_size%2==0:
        kernel_size+=1
        
    filtered=signal.medfilt(Z,kernel_size)

    if axis ==1:
        filtered=filtered.T
        
    return X, Y, filtered
