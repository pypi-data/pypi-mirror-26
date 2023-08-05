from lmfit import Model
import numpy  as np
pi = np.pi

def coupling_parameters_doc(sep="\n"):
    def _decorator(func):
        params_docstring = \
        r"""
    Parameters
    -----------
    w : numeric [rad/sec]
        Probe frequency
    b : numeric [T]
        External magnetic bias field
    wc : scalar [rad/s]
        Cavity resonance frequency
    ws : function [rad/s]
        Function returning the spin resonance frequency for every value of b
    kappaci : scalar [rad/s]
        Internal cavity relaxation rate :math:`\kappa_{c,i}`, corresponding to 
        the half width half maximum (HWHM) linewidth.
    kappace : scalar [rad/s]
        External relaxation rate (coupling to feed line) :math:`\kappa_{c,e}`,
        corresponding to the HWHM linewidth
    kappas : scalar [rad/s]
        Spin relaxation rate :math:`\kappa_{s}`, corresponding to the HWHM 
        linewidth
    g : scalar [rad/s]
        Coupling rate :math:`g`
        """        
        if func.__doc__ == None:
            func.__doc__ = params_docstring
        else:
            func.__doc__ = func.__doc__ % {'parameters':params_docstring}
        return func
    return _decorator
    
@coupling_parameters_doc()
def s11(w, b, wc, ws, kappaci, kappace, kappas, g):
    r"""
    Model the reflection parameter of a hybrid system of ferromagnet and 
    cavity resonator according to Abe et al. [1].

    .. math:: 
        1 + \frac
            {
                \kappa_{c,e}
            }
            {
                i(\omega-\omega_{c}) 
                - (\kappa_{c,i} 
                + \kappa_{c,e}) 
                + \frac{g^2}{i(\omega-\omega_{s}(B) - \kappa_{s}}
            }
    %(parameters)s
    Returns
    --------
        Reflection parameter S11 at the given frequency\frequencies w and 
        magnetic field(s) b.

    Notes
    -----
    Note that the parameters (including ws) are typically given in rad/s.
    However, consistently using [Hz] of course also works as this unit cancles
    out.
    
    References
    -----------
        [1] Abe, E. et al. Appl. Phys. Lett. 98, 251108 (2011)
        
    Examples
    --------
    Generate calculate the response for a typical 3D cavity resonator / 
    paramagnet system. Adjust num=2 to your needs (try 1000).
    Plot in matplotlib with e.g. plt.imshow(reflection.T, origin='left').
    
    >>> import numpy as np
    >>> reflection = s11(
            w=np.linspace(9.4e9, 9.6e9, num=2)*2*np.pi,
            b=np.linspace(0.3, 0.4, num=2),
            wc=9.5e9*2*np.pi,
            ws=lambda b: 28e9*2*np.pi * b,
            kappaci=10e6*2*np.pi,
            kappace=10e6*2*np.pi,
            kappas=20e6*2*np.pi,
            g=80e6*2*np.pi)
    >>> print(reflection)
    [[ 0.98283411+0.09073983j  0.97855042-0.10108048j]
     [ 0.97934753+0.09939495j  0.98212674-0.09270865j]]
    """
    if not (len(np.shape(w)) and np.shape(w) == np.shape(b)):
        W, B = np.meshgrid(w, b)
    s11 =  1 + kappace / (1j*(W-wc) - (kappaci + kappace) + g**2/(1j*(W-ws(B)) - kappas))
    return s11

@coupling_parameters_doc()
def s21(w, b, wc, ws, kappaci, kappace, kappas, g):
    r"""
    Model the transmission parameter of a hybrid system of ferromagnet and 
    resonator according to Huebl et al. [1]. We unify the notation of cavity 
    and spin relaxation rate to :math:`\kappa_{c}` and :math:`\kappa_{s}` to
    avoid confusion witht the gyromagnetic ratio :math:\gamma and the symbol
    :math:`\gamma_{s}` which Huebl et al. [1] use for the spin relaxation rate.
    Furthermore, we correct a factor 2 in the equation of [1] so all relaxation
    rates correspond to the half width half maximum linewidth.

    .. math:: 
        \frac
            {
                \kappa_{c,e}
            }
            {
                i(\omega-\omega_{c}) 
                - (\kappa_{c,i} 
                + \kappa_{c,e}) 
                + \frac{g^2}{i(\omega-\omega_{s}(B) - \kappa_{s}}
            }
    %(parameters)s
    Returns
    --------
        Reflection parameter S11 at the given frequency\frequencies w and 
        magnetic field(s) b.

    Notes
    -----
    Note that the parameters (including ws) are typically given in rad/s.
    However, consistently using [Hz] of course also works as this unit cancles
    out.
    
    References
    -----------
        [1] Huebl, H. et al. Phys. Rev. Lett. 111, 127003 (2013)
        
    Examples
    --------
    Generate calculate the response for a typical transmission line resonator / 
    paramagnet system. Adjust num=2 to your needs (try 1000).
    Plot in matplotlib with e.g. plt.imshow(reflection.T, origin='left').
    
    >>> import numpy as np
    >>> reflection = s11(
            w=np.linspace(9.4e9, 9.6e9, num=2)*2*np.pi,
            b=np.linspace(0.3, 0.4, num=2),
            wc=9.5e9*2*np.pi,
            ws=lambda b: 28e9*2*np.pi * b,
            kappaci=10e6*2*np.pi,
            kappace=10e6*2*np.pi,
            kappas=20e6*2*np.pi,
            g=80e6*2*np.pi)
    >>> print(reflection)
    [[ 0.98283411+0.09073983j  0.97855042-0.10108048j]
     [ 0.97934753+0.09939495j  0.98212674-0.09270865j]]
    """
    if not (len(np.shape(w)) and np.shape(w) == np.shape(b)):
        W, B = np.meshgrid(w, b)
    s21 =  1 + kappace / ( 1j*(W-wc) - (kappaci + kappace) + g**2/(1j*(W-ws(B)) - kappas) )
    return s21

def herskind(x, kappac, kappas, g, wc):
    """ 
    Herskind model according to [1] which returns the resonance shift and line 
    broadening due to a weak cavity-spin coupling. The model is in accordance 
    with the independent formulation of Schuster et al. [2].  
    All parameters need to be given consistently in Hz or in rad/s. The return 
    value is then in the same unit.
    
    Note that this model **returns inaccurate parameters** and should therefore
    not be used.
    
    Parameters
    ----------
        x : = Delta = ws-wc = γ*(H-H_res) 
            Frequency detuning \Delta
        kappac :
            Cavity relaxation rate, corresponding to half width half maximum 
            (HWHM) linewidth
        kappas : 
            Spin relaxation rate (corresponding to HWHM linewidth)
        g :
            Cavity-spin coupling rate
        wc :
            Cavity resonance frequency  
    
    Returns
    -------
        Complex number consisting of omega_0 + 1j*(kappa).
        
    References
    ----------    
        [1] Herskind, P. F. et al. Nat. Phys. 5, 494–498 (2009).
        [2] Schuster, D. I. et al. Phys. Rev. Lett. 105, 140501 (2010).
    """
    return (
        herskind_omega(x, kappas, g, wc)
        + 1j*herskind_kappa(x, kappac, kappas, g) )

def herskind_omega(x, kappas, g, wc):
    """
    Returns resonance frequency omega_0 of the hybridized system.
    
    For detailed documentation see herskind().
    """
    return wc - g**2 * x / ( kappas**2 + x**2 )

def herskind_kappa(x, kappac, kappas, g):
    """
    Returns linewidth kappa of the hybridized system.
    
    For detailed documentation see herskind().
    """
    return kappac + g**2 * kappas / ( kappas**2 + x**2 )


# TODO: Add lmfit models implementing parameter guesses for the models in this
#    submodule.
#params = model.make_params(**guess)
#params["kappaci"] = Parameter(expr="kappac")
#params["kappac"].min=0
#params["kappas"].min=0
#params["g"].min=0
#params["omegac"].min=0