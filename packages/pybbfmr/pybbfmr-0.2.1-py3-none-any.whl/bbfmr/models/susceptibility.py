# -*- coding: utf-8 -*-
"""
(Complex LMFIT) models for the FMR response, i.e. high frequency susceptibility
"""

import numpy as np
from lmfit.models import LinearModel, LorentzianModel
from bbfmr.complex_model import ComplexModel
from bbfmr.models.complex import ComplexLinearModel
import sympy as s

import scipy.constants as c
from numpy import pi
mu_0 = 4*pi*1e-7
mu_b = c.physical_constants["Bohr magneton"][0]


# %% Field space models
class VNAFMR_IPFieldModel(ComplexModel):
    def func(x, f=1e10, B_r=1, dB=0.005, g=2.024, Z=1, phi=0):
        I = 1j
        mu_0 = 4*np.pi*1e-7
        B = x
        H = np.abs(B/mu_0)
        H_r = B_r/mu_0
        dH = dB/mu_0
        H_equiv = (2*pi*c.hbar*f)/(mu_0*g*mu_b)
        M = (H_equiv**2 - H_r**2)/H_r # from IP dispersion
        
        numerator = M * (H + M - I*dH/2.)
        denominator = (H + M - I * dH/2.) *  (H - I * dH/2.) - H_equiv**2
        return -1j * Z * np.exp(1j*phi) * numerator/denominator

    def __init__(self, *args, **kwargs):
        super(VNAFMR_IPFieldModel, self).__init__(
            VNAFMR_IPFieldModel.func, *args,
            **kwargs)
        self.name = "VNAFMR_IPFieldModel"

    def calc_Z(self, y, params):
        B_r = params[self.prefix +'B_r'].value
        g = params[self.prefix +'g'].value
        dB = params[self.prefix +'dB'].value
        f = params[self.prefix +'f'].value

        omega = 2*np.pi*f
        gamma = g*mu_b/c.hbar
        mu_0 = 4*np.pi*1e-7
        mu0Hres = B_r
        dH = dB/mu_0
        I = 1j
        amp_r = np.abs(((omega**2/(gamma**2*mu_0**2) -  mu0Hres**2)*(-((1/2)*I*dH*mu_0**2) - (omega**2/(gamma**2*mu_0**2) - mu0Hres**2)/mu0Hres + mu0Hres))/ (mu0Hres*(-(omega**2/gamma**2) + (-((1/2)*I*dH*mu_0**2) - (omega**2/(gamma**2*mu_0**2) - mu0Hres**2)/mu0Hres + mu0Hres)**2)))
        return y/amp_r


    def make_params(self, **kwargs):
        p = super(VNAFMR_IPFieldModel, self).make_params(**kwargs)
        p[self.prefix + "f"].vary = False
        p[self.prefix + "g"].vary = False
        p[self.prefix + "B_r"].min = 0
        p[self.prefix + "dB"].min = 0
        p[self.prefix + "phi"].min = -np.pi*2
        p[self.prefix + "phi"].max = np.pi*2
        p[self.prefix + "phi"].value = -1.6
        p[self.prefix + "Z"].min = 0
        return p

    def guess(self, data, x=None, **kwargs):
        center, hwhm, height = guess_peak_lorentzian(np.abs(data), x=x)
        pars = self.make_params(B_r=center, dB=hwhm, **kwargs)
        pars[self.prefix + 'Z'].value = self.calc_Z(height, pars)
        return pars

    def recommended_roi(self, x, data, arg):
        p = self.guess(data, x=x)
        width = p[self.prefix + "dB"].value * float(arg)
        B_r = p[self.prefix + "B_r"].value
        min_idx = np.argmin(np.abs(x - (B_r - width)))
        max_idx = np.argmin(np.abs(x - (B_r + width)))
        
        return np.arange(min_idx, max_idx)
        
        
class VNAFMR_SimpleFieldModel(ComplexModel):
    @staticmethod
    def chi_ip_yy(B, f=1e10, M_eff=140e3, dB=1e-2, gamma=28.024e9, **kwargs):
        """
        Dynamic yy component of the susceptibility tensor acording to Louis
        (2.44) for a thin film magnetized in plane divided by M
        FIXME: Document limits of this approximation

        B ; [T]
            Magnetic field strength B
        f : [Hz]
            MW frequency
        dH : [T]
            HWHM linewidth
        M_eff : [A/m]
            Effective magnetization (due to anisotropy)
        gamma : [Hz/T]
            gyromagnetic ratio, gamma = g*mu_b/hbar

        """
        dH = dB/2 / mu_0  # FWHM
        H = B/mu_0
        w = 2*pi*f
        H_res_eval = w/(mu_0*gamma)
        chi= (
                (M_eff*(H - 1j*dH/2))
                 /
                ((H - 1j*dH/2)*(H + M_eff - 1j*dH/2) - H_res_eval**2)
            )
        return chi

    def func(x, f=1e10, B_res=0.1, dB=1e-2, gamma=28.024e9, Z=1, phi=0):
        w = 2*pi*f
        H_res0 = w/(mu_0*gamma)
        H_res = B_res/mu_0
        M_eff = (H_res0**2-H_res**2)/H_res
        chi = VNAFMR_SimpleFieldModel.chi_ip_yy(x, f=f, M_eff=M_eff,
                                                dB=dB, gamma=gamma)
        return Z*np.exp(1j*phi) * chi

    def __init__(self, *args, **kwargs):
        super().__init__(func=VNAFMR_SimpleFieldModel.func, *args, **kwargs)

    def make_params(self, *args, **kwargs):
        p = super().make_params(*args, **kwargs)
        p["Z"].min = 0
        p["phi"].min = 0
        p["phi"].max = +2*np.pi
        p["gamma"].min = 0
        p["gamma"].vary = False
        p["dB"].min = 0
        p["phi"].min = -np.pi
        p["phi"].max = +np.pi

        return p

    def guess(self, data, x=None, **kwargs):
        lm = LinearModel()
        y_slope = lm.eval(x=x,
                          params=lm.guess(np.abs(data), x=x))
        center, hwhm, height = guess_peak(np.abs(np.abs(data)-y_slope), x=x)

        pars = self.make_params(Ms=height, B_res=center, dB=hwhm)
        return pars


# %% Frequency space models
class VNAFMR_EllipsoidSphereModel(ComplexModel):
    def func(x, B=1, f_r=1e10, M_s=140e3, df=30e6,
             gamma=28.0249527e9, Z=1, phi=0):
        f = x
        return (1.0*1j*Z*f*(B*M_s*gamma**2*mu_0/(-1.0*1j*df*f - f**2 + f_r**2) - 1.0*1j*M_s*df*gamma*mu_0/(-1.0*1j*df*f - f**2 + f_r**2))*np.exp(1.0*1j*phi))

    def __init__(self, *args, **kwargs):
        super(VNAFMR_EllipsoidSphereModel, self).__init__(
            VNAFMR_EllipsoidSphereModel.func, *args,
            **kwargs)
        self.name = "VNAFMR_EllipsoidSphereModel"

    def fit(self, *args, **kwargs):
        fit_kws_orig = kwargs.pop("fit_kws", {})
        if "diag" not in fit_kws_orig:
            fit_kws = {"diag": [1e9, 1, 1e9, 1e3, 1e6,
                                1e9, 1, 1, 1, 1, 1]}
            fit_kws.update(fit_kws_orig)
        else:
            fit_kws = fit_kws_orig

        return super(VNAFMR_EllipsoidSphereModel, self).fit(*args,
                                                                 fit_kws=fit_kws,
                                                                 **kwargs)
    def calc_Z(self, y, params):
        M_s = params[self.prefix + 'M_s'].value
        B = params[self.prefix +'B'].value
        gamma = params[self.prefix +'gamma'].value
        df = params[self.prefix +'df'].value
        f_r = params[self.prefix +'f_r'].value

        amp_r = (1.0*np.sqrt(1.0*B**2*M_s**2*gamma**4*mu_0**2/(df**2*f_r**2) + 1.0*M_s**2*gamma**2*mu_0**2/f_r**2)*np.abs(f_r))
        return y/amp_r


    def make_params(self, **kwargs):
        p = super(VNAFMR_EllipsoidSphereModel, self).make_params(**kwargs)
        p[self.prefix + "B"].vary = False
        p[self.prefix + "M_s"].vary = False
        p[self.prefix + "gamma"].vary = False
        p[self.prefix + "f_r"].min = 0
        p[self.prefix + "df"].min = 0
        p[self.prefix + "phi"].min = -np.pi*2
        p[self.prefix + "phi"].max = np.pi*2
        p[self.prefix + "phi"].value = 0
        return p

    def guess(self, data, x=None, **kwargs):
        center, hwhm, height = guess_peak_lorentzian(np.abs(data), x=x)
        pars = self.make_params(M_s=1.4e5, f_r=center, df=hwhm, **kwargs)
        pars[self.prefix + 'df'].set(min=0.0)
        pars[self.prefix + 'B'].value = 1
        pars[self.prefix + 'Z'].value = self.calc_Z(height, pars)
        return pars

    def recommended_roi(self, x, data, arg):
        # Typically the data input still contains a background. Subtract this.
        lin_model = ComplexLinearModel()
        lin_params = lin_model.guess(data, x=x)
        p = self.guess(data-lin_model.eval(x=x, params=lin_params), x=x)
        width = p[self.prefix + "df"].value * float(arg)
        fr = p[self.prefix + "f_r"].value
        min_idx = np.argmin(np.abs(x - (fr - width)))
        max_idx = np.argmin(np.abs(x - (fr + width)))
        
        return np.arange(min_idx, max_idx)


class VNAFMR_EllipsoidDerivativeSphereModel(ComplexModel):
    def func(x, B=1, f_r=1e10, M_s=140e3, df=30e6,
             gamma=28.0249527e9, Z=1, phi=0):
        f = x
        return (-1.0*1j*Z*f*(B*M_s*gamma**2*mu_0*(1.0*1j*df + 2*f)/(-1.0*1j*df*f - f**2 + f_r**2)**2 - 1.0*1j*M_s*df*gamma*mu_0*(1.0*1j*df + 2*f)/(-1.0*1j*df*f - f**2 + f_r**2)**2)*np.exp(1.0*1j*phi))

    def __init__(self, *args, **kwargs):
        super(VNAFMR_EllipsoidDerivativeSphereModel, self).__init__(
            VNAFMR_EllipsoidDerivativeSphereModel.func, *args,
            **kwargs)
        self.name = "VNAFMR_EllipsoidDerivativeSphereModel"

    def fit(self, *args, **kwargs):
        fit_kws_orig = kwargs.pop("fit_kws", {})
        if "diag" not in fit_kws_orig:
            fit_kws = {"diag": [1e9, 1, 1e9, 1e3, 1e6,
                                1e9, 1, 1, 1, 1, 1]}
            fit_kws.update(fit_kws_orig)
        else:
            fit_kws = fit_kws_orig

        return super(VNAFMR_EllipsoidDerivativeSphereModel, self).fit(*args,
                                                                   fit_kws=fit_kws,
                                                                   **kwargs)

    def make_params(self, **kwargs):
        p = super(VNAFMR_EllipsoidDerivativeSphereModel, self).make_params(**kwargs)
        p[self.prefix + "B"].vary = False
        p[self.prefix + "M_s"].vary = False
        p[self.prefix + "gamma"].vary = False
        p[self.prefix + "phi"].vary = False
        p[self.prefix + "phi"].min = -np.pi*2
        p[self.prefix + "phi"].max= np.pi*2
        p[self.prefix + "f_r"].min = 0
        p[self.prefix + "df"].min = 0
        return p

    def calc_Z(self, y, params):
        M_s = params[self.prefix + 'M_s'].value
        B = params[self.prefix +'B'].value
        gamma = params[self.prefix +'gamma'].value
        df = params[self.prefix +'df'].value
        f_r = params[self.prefix +'f_r'].value
        amp_r_f = (1.0*np.sqrt(1.0*B**2*M_s**2*gamma**4*mu_0**2/(df**2*f_r**4) + 4.0*B**2*M_s**2*gamma**4*mu_0**2/(df**4*f_r**2) + 1.0*M_s**2*gamma**2*mu_0**2/f_r**4 + 4.0*M_s**2*gamma**2*mu_0**2/(df**2*f_r**2))*np.abs(f_r))
        return y/amp_r_f
        
    def guess(self, data, x=None, **kwargs):
        center, hwhm, height = guess_peak(np.abs(data), x=x)
        pars = self.make_params(Ms=height, f_r=center, df=hwhm, **kwargs)
        pars[self.prefix + 'df'].set(min=0.0)
        pars[self.prefix + 'B'].value = 1
        pars[self.prefix + 'Z'].value = self.calc_Z(height, pars)
        return pars

    def recommended_roi(self, x, data, arg):
        p = self.guess(data, x=x)
        width = p[self.prefix + "df"].value * float(arg)
        fr = p[self.prefix + "f_r"].value
        min_idx = np.argmin(np.abs(x - (fr - width)))
        max_idx = np.argmin(np.abs(x - (fr + width)))
        
        return np.arange(min_idx, max_idx)

        
class VNAFMR_EllipsoidDifferenceQuotientSphereModel(ComplexModel):
    def func(x, B=1, f_r=1e10, M_s=140e3, df=30e6, mod_f=1e6,
             gamma=28.0249527e9, Z=1, phi=0):
        f = x
        return (Z*(B*M_s*gamma**2*mu_0/(-1.0*1j*df*(f + mod_f) + f_r**2 - (f + mod_f)**2) - B*M_s*gamma**2*mu_0/(-1.0*1j*df*(f - mod_f) + f_r**2 - (f - mod_f)**2) - 1.0*1j*M_s*df*gamma*mu_0/(-1.0*1j*df*(f + mod_f) + f_r**2 - (f + mod_f)**2) + 1.0*1j*M_s*df*gamma*mu_0/(-1.0*1j*df*(f - mod_f) + f_r**2 - (f - mod_f)**2))*np.exp(1.0*1j*phi)/(2*mod_f))

    def __init__(self, *args, **kwargs):
        super(VNAFMR_EllipsoidDifferenceQuotientSphereModel, self).__init__(
            VNAFMR_EllipsoidDifferenceQuotientSphereModel.func, *args,
            **kwargs)
        self.name = "VNAFMR_EllipsoidDerivativeSphereModel"

    def fit(self, *args, **kwargs):
        fit_kws_orig = kwargs.pop("fit_kws", {})
        if "diag" not in fit_kws_orig:
            fit_kws = {"diag": [1e9, 1, 1e9, 1e3, 1e6,
                                1e9, 1, 1, 1, 1, 1]}
            fit_kws.update(fit_kws_orig)
        else:
            fit_kws = fit_kws_orig

        return super(VNAFMR_EllipsoidDifferenceQuotientSphereModel, self).fit(*args,
                                                                   fit_kws=fit_kws,
                                                                   **kwargs)

    def make_params(self, **kwargs):
        p = super(VNAFMR_EllipsoidDifferenceQuotientSphereModel, self).make_params(**kwargs)
        p[self.prefix + "B"].vary = False
        p[self.prefix + "M_s"].vary = False
        p[self.prefix + "gamma"].vary = False
        p[self.prefix + "phi"].vary = False
        p[self.prefix + "phi"].min = -np.pi*2
        p[self.prefix + "phi"].max= np.pi*2
        p[self.prefix + "f_r"].min = 0
        p[self.prefix + "df"].min = 0
        p[self.prefix + "mod_f"].min = 0
        p[self.prefix + "mod_f"].vary = False
        return p

    def calc_Z(self, y, params):
        M_s = params[self.prefix + 'M_s'].value
        B = params[self.prefix +'B'].value
        gamma = params[self.prefix +'gamma'].value
        df = params[self.prefix +'df'].value
        f_r = params[self.prefix +'f_r'].value
        mod_f = params[self.prefix +'f_r'].value
        amp_r_f = np.abs(np.sqrt((4.0*df**6*f_r**4 - 8.0*df**6*f_r**2*mod_f**2 + 4.0*df**6*mod_f**4 + 16.0*df**4*f_r**6 - 8.0*df**4*f_r**2*mod_f**4 + 8.0*df**4*mod_f**6 + 128.0*df**2*f_r**6*mod_f**2 - 32.0*df**2*f_r**4*mod_f**4 + 4.0*df**2*mod_f**8 + 256*f_r**6*mod_f**4 - 128*f_r**4*mod_f**6 + 16*f_r**2*mod_f**8)/(1.0*df**8*f_r**8 - 4.0*df**8*f_r**6*mod_f**2 + 6.0*df**8*f_r**4*mod_f**4 - 4.0*df**8*f_r**2*mod_f**6 + 1.0*df**8*mod_f**8 + 16.0*df**6*f_r**8*mod_f**2 - 44.0*df**6*f_r**6*mod_f**4 + 44.0*df**6*f_r**4*mod_f**6 - 20.0*df**6*f_r**2*mod_f**8 + 4.0*df**6*mod_f**10 + 96.0*df**4*f_r**8*mod_f**4 - 176.0*df**4*f_r**6*mod_f**6 + 134.0*df**4*f_r**4*mod_f**8 - 44.0*df**4*f_r**2*mod_f**10 + 6.0*df**4*mod_f**12 + 256.0*df**2*f_r**8*mod_f**6 - 320.0*df**2*f_r**6*mod_f**8 + 176.0*df**2*f_r**4*mod_f**10 - 44.0*df**2*f_r**2*mod_f**12 + 4.0*df**2*mod_f**14 + 256*f_r**8*mod_f**8 - 256*f_r**6*mod_f**10 + 96*f_r**4*mod_f**12 - 16*f_r**2*mod_f**14 + mod_f**16))*np.sqrt(B**2*gamma**2 + 1.0*df**2)*np.abs(M_s)*np.abs(gamma)*np.abs(mu_0)/2)
        return y/amp_r_f
        
    def guess(self, data, x=None, **kwargs):
        center, hwhm, height = guess_peak(np.abs(data), x=x)
        pars = self.make_params(Ms=height, f_r=center, df=hwhm, **kwargs)
        pars[self.prefix + 'df'].set(min=0.0)
        pars[self.prefix + 'Z'].value = self.calc_Z(height, pars)
        return pars

    def recommended_roi(self, x, data, arg):
        p = self.guess(data, x=x)
        width = p[self.prefix + "df"].value * float(arg)
        fr = p[self.prefix + "f_r"].value
        min_idx = np.argmin(np.abs(x - (fr - width)))
        max_idx = np.argmin(np.abs(x - (fr + width)))
        
        return np.arange(min_idx, max_idx)
# The following models have not been cross checked and may not be correct.
#class VNAFMR_EllipsoidDerivativeModel(ComplexModel):
#    def func(x, B=1, f_r=1e10, M_s=140e3, df=30e6, phi=0,
#             gamma=28.0249527e9, Z=1, N_1=0, N_2=0, N_3=1):
#        I = 1j
#        f = x
#        chi_ddf = (B*M_s*gamma**2*mu_0*(1.0*I*df + 2*f)/(-1.0*I*df*f - f**2 + f_r**2)**2 + M_s**2*N_2*gamma**2*mu_0**2*(1.0*I*df + 2*f)/(-1.0*I*df*f - f**2 + f_r**2)**2 - M_s**2*N_3*gamma**2*mu_0**2*(1.0*I*df + 2*f)/(-1.0*I*df*f - f**2 + f_r**2)**2 - 1.0*I*M_s*df*f*gamma*mu_0*(1.0*I*df + 2*f)/((gamma*mu_0*(B/mu_0 + M_s*(N_1 - N_3)) + gamma*mu_0*(B/mu_0 + M_s*(N_2 - N_3)))*(-1.0*I*df*f - f**2 + f_r**2)**2) - 1.0*I*M_s*df*gamma*mu_0/((gamma*mu_0*(B/mu_0 + M_s*(N_1 - N_3)) + gamma*mu_0*(B/mu_0 + M_s*(N_2 - N_3)))*(-1.0*I*df*f - f**2 + f_r**2)))
#        # chi_ddH = (B*M_s*gamma**2*mu_0*(-gamma**2*mu_0**2*(B/mu_0 + M_s*(N_1 - N_3)) - gamma**2*mu_0**2*(B/mu_0 + M_s*(N_2 - N_3)))/(-1.0*I*df*f - f**2 + f_r**2)**2 + M_s**2*N_2*gamma**2*mu_0**2*(-gamma**2*mu_0**2*(B/mu_0 + M_s*(N_1 - N_3)) - gamma**2*mu_0**2*(B/mu_0 + M_s*(N_2 - N_3)))/(-1.0*I*df*f - f**2 + f_r**2)**2 - M_s**2*N_3*gamma**2*mu_0**2*(-gamma**2*mu_0**2*(B/mu_0 + M_s*(N_1 - N_3)) - gamma**2*mu_0**2*(B/mu_0 + M_s*(N_2 - N_3)))/(-1.0*I*df*f - f**2 + f_r**2)**2 + 2.0*I*M_s*df*f*gamma**2*mu_0**2/((gamma*mu_0*(B/mu_0 + M_s*(N_1 - N_3)) + gamma*mu_0*(B/mu_0 + M_s*(N_2 - N_3)))**2*(-1.0*I*df*f - f**2 + f_r**2)) - 1.0*I*M_s*df*f*gamma*mu_0*(-gamma**2*mu_0**2*(B/mu_0 + M_s*(N_1 - N_3)) - gamma**2*mu_0**2*(B/mu_0 + M_s*(N_2 - N_3)))/((gamma*mu_0*(B/mu_0 + M_s*(N_1 - N_3)) + gamma*mu_0*(B/mu_0 + M_s*(N_2 - N_3)))*(-1.0*I*df*f - f**2 + f_r**2)**2) + M_s*gamma**2*mu_0**2/(-1.0*I*df*f - f**2 + f_r**2))
#
#        return Z*1j*f*np.exp(1j*phi) * chi_ddf
#
#    def __init__(self, *args, **kwargs):
#        super(VNAFMR_EllipsoidDerivativeQuickModel, self).__init__(
#            VNAFMR_EllipsoidDerivativeQuickModel.func, *args, **kwargs)
#        self.name = "VNAFMR_EllipsoidDerivativeQuickModel"
#        self.N = (1, 0, 0)
#
#    def fit(self, *args, **kwargs):
#        fit_kws_orig = kwargs.pop("fit_kws", {})
#        if "diag" not in fit_kws_orig:
#            fit_kws = {"diag": [1e9, 1, 1e9, 1e3, 1e6,
#                                1e9, 1, 1, 1, 1, 1]}
#            fit_kws.update(fit_kws_orig)
#        else:
#            fit_kws = fit_kws_orig
#
#        return super(VNAFMR_EllipsoidDerivativeQuickModel, self).fit(*args,
#                                                                     fit_kws=fit_kws,
#                                                                     **kwargs)
#    def calc_Z(self, y, params):
#        M_s = params[self.prefix + 'M_s'].value
#        B = params[self.prefix +'B'].value
#        gamma = params[self.prefix +'gamma'].value
#        df = params[self.prefix +'df'].value
#        N_1 = params[self.prefix +'N_1'].value
#        N_2 = params[self.prefix +'N_2'].value
#        N_3 = params[self.prefix +'N_3'].value
#        f_r = params[self.prefix +'f_r'].value
#        # amplitude of abs(chi) on resonance for N=(1,1,1)
#        amp_r_f = (np.sqrt(1.0*B**2*M_s**2*gamma**4*mu_0**2/(df**2*f_r**4) + 4.0*B**2*M_s**2*gamma**4*mu_0**2/(df**4*f_r**2) + 2.0*B*M_s**3*N_2*gamma**4*mu_0**3/(df**2*f_r**4) + 8.0*B*M_s**3*N_2*gamma**4*mu_0**3/(df**4*f_r**2) - 2.0*B*M_s**3*N_3*gamma**4*mu_0**3/(df**2*f_r**4) - 8.0*B*M_s**3*N_3*gamma**4*mu_0**3/(df**4*f_r**2) - 4.0*B*M_s**2*gamma**3*mu_0**2/(2*B*df**2*f_r**2*gamma + M_s*N_1*df**2*f_r**2*gamma*mu_0 + M_s*N_2*df**2*f_r**2*gamma*mu_0 - 2*M_s*N_3*df**2*f_r**2*gamma*mu_0) + 1.0*M_s**4*N_2**2*gamma**4*mu_0**4/(df**2*f_r**4) + 4.0*M_s**4*N_2**2*gamma**4*mu_0**4/(df**4*f_r**2) - 2.0*M_s**4*N_2*N_3*gamma**4*mu_0**4/(df**2*f_r**4) - 8.0*M_s**4*N_2*N_3*gamma**4*mu_0**4/(df**4*f_r**2) + 1.0*M_s**4*N_3**2*gamma**4*mu_0**4/(df**2*f_r**4) + 4.0*M_s**4*N_3**2*gamma**4*mu_0**4/(df**4*f_r**2) - 4.0*M_s**3*N_2*gamma**3*mu_0**3/(2*B*df**2*f_r**2*gamma + M_s*N_1*df**2*f_r**2*gamma*mu_0 + M_s*N_2*df**2*f_r**2*gamma*mu_0 - 2*M_s*N_3*df**2*f_r**2*gamma*mu_0) + 4.0*M_s**3*N_3*gamma**3*mu_0**3/(2*B*df**2*f_r**2*gamma + M_s*N_1*df**2*f_r**2*gamma*mu_0 + M_s*N_2*df**2*f_r**2*gamma*mu_0 - 2*M_s*N_3*df**2*f_r**2*gamma*mu_0) + 1.0*M_s**2*df**2*gamma**2*mu_0**2/(2*B*df*f_r*gamma + M_s*N_1*df*f_r*gamma*mu_0 + M_s*N_2*df*f_r*gamma*mu_0 - 2*M_s*N_3*df*f_r*gamma*mu_0)**2 - 2.0*M_s**2*df*gamma**2*mu_0**2/(4*B**2*df*f_r**2*gamma**2 + 4*B*M_s*N_1*df*f_r**2*gamma**2*mu_0 + 4*B*M_s*N_2*df*f_r**2*gamma**2*mu_0 - 8*B*M_s*N_3*df*f_r**2*gamma**2*mu_0 + M_s**2*N_1**2*df*f_r**2*gamma**2*mu_0**2 + 2*M_s**2*N_1*N_2*df*f_r**2*gamma**2*mu_0**2 - 4*M_s**2*N_1*N_3*df*f_r**2*gamma**2*mu_0**2 + M_s**2*N_2**2*df*f_r**2*gamma**2*mu_0**2 - 4*M_s**2*N_2*N_3*df*f_r**2*gamma**2*mu_0**2 + 4*M_s**2*N_3**2*df*f_r**2*gamma**2*mu_0**2) + 4.0*M_s**2*f_r**2*gamma**2*mu_0**2/(2*B*df*f_r*gamma + M_s*N_1*df*f_r*gamma*mu_0 + M_s*N_2*df*f_r*gamma*mu_0 - 2*M_s*N_3*df*f_r*gamma*mu_0)**2 + 1.0*M_s**2*gamma**2*mu_0**2/(2*B*f_r*gamma + M_s*N_1*f_r*gamma*mu_0 + M_s*N_2*f_r*gamma*mu_0 - 2*M_s*N_3*f_r*gamma*mu_0)**2))
#        return y/amp_r_f/f_r
#
#    def make_params(self, **kwargs):
#        p = super(VNAFMR_EllipsoidDerivativeQuickModel, self).make_params(**kwargs)
#        p[self.prefix + "N_1"].vary = False
#        p[self.prefix + "N_2"].vary = False
#        p[self.prefix + "N_3"].vary = False
#        p[self.prefix + "N_1"].value = self.N[0]
#        p[self.prefix + "N_2"].value = self.N[1]
#        p[self.prefix + "N_3"].value = self.N[2]
#        p[self.prefix + "B"].vary = False
#        p[self.prefix + "M_s"].vary = False
#        p[self.prefix + "gamma"].vary = False
#        p[self.prefix + "phi"].vary = False
#        p[self.prefix + "phi"].min = -np.pi*2
#        p[self.prefix + "phi"].max= np.pi*2
#        p[self.prefix + "f_r"].min = 0
#        p[self.prefix + "df"].min = 0
#        return p
#
#    def guess(self, data, x=None, **kwargs):
#        center, hwhm, height = guess_peak(np.abs(data), x=x)
#        pars = self.make_params(Ms=height, f_r=center, df=hwhm*2, **kwargs)
#        pars[self.prefix + 'df'].set(min=0.0)
#        pars[self.prefix + 'B'].value = 100
#        pars[self.prefix + 'Z'].value = self.calc_Z(height, pars)
#        pars[self.prefix + 'M_s'].value = 1.5421e+05
#        pars[self.prefix + 'gamma'].value = 27497699359.848057
#        return pars
#
#    def recommended_roi(self, x, data, arg):
#        p = self.guess(data, x=x)
#        width = p[self.prefix + "df"].value * float(arg)
#        fr = p[self.prefix + "f_r"].value
#        min_idx = np.argmin(np.abs(x - (fr - width)))
#        max_idx = np.argmin(np.abs(x - (fr + width)))
#
#        return np.arange(min_idx, max_idx)
#
#
#class VNAFMR_EllipsoidAngleDerivativeModel(ComplexModel):
#    def func(x, B=1, f_r=1e10, M_s=140e3, df=30e6, theta=0, phase=0,
#             gamma=28.0249527e9, Z=1, N_1=0, N_2=0, N_3=1):
#        f = x
#        chi_der = 0
#
#        return Z*1j*f*np.exp(1j*phase) * chi_der
#
#    def __init__(self, *args, **kwargs):
#        super(VNAFMR_EllipsoidAngleDerivativeModel, self).__init__(
#            VNAFMR_EllipsoidAngleDerivativeModel.func, *args, **kwargs)
#        self.name = "VNAFMR_EllipsoidAngleDerivativeModel"
#        self.N = (1, 0, 0)
#
#    def fit(self, *args, **kwargs):
#        fit_kws_orig = kwargs.pop("fit_kws", {})
#        if "diag" not in fit_kws_orig:
#            fit_kws = {"diag": [1e9, 1, 1e9, 1e3, 1e6,
#                                1e9, 1, 1, 1, 1, 1]}
#            fit_kws.update(fit_kws_orig)
#        else:
#            fit_kws = fit_kws_orig
#
#        return super(VNAFMR_EllipsoidAngleDerivativeModel, self).fit(*args,
#                                                                     fit_kws=fit_kws,
#                                                                     **kwargs)
#    def calc_Z(self, y, params):
#        M_s = params[self.prefix + 'M_s'].value
#        B = params[self.prefix +'B'].value
#        gamma = params[self.prefix +'gamma'].value
#        df = params[self.prefix +'df'].value
#        N_1 = params[self.prefix +'N_1'].value
#        N_2 = params[self.prefix +'N_2'].value
#        N_3 = params[self.prefix +'N_3'].value
#        f_r = params[self.prefix +'f_r'].value
#        # amplitude of abs(chi) on resonance for N=(1,1,1)
#        amp_r_f = (np.sqrt(1.0*B**2*M_s**2*gamma**4*mu_0**2/(df**2*f_r**4) + 4.0*B**2*M_s**2*gamma**4*mu_0**2/(df**4*f_r**2) + 2.0*B*M_s**3*N_2*gamma**4*mu_0**3/(df**2*f_r**4) + 8.0*B*M_s**3*N_2*gamma**4*mu_0**3/(df**4*f_r**2) - 2.0*B*M_s**3*N_3*gamma**4*mu_0**3/(df**2*f_r**4) - 8.0*B*M_s**3*N_3*gamma**4*mu_0**3/(df**4*f_r**2) - 4.0*B*M_s**2*gamma**3*mu_0**2/(2*B*df**2*f_r**2*gamma + M_s*N_1*df**2*f_r**2*gamma*mu_0 + M_s*N_2*df**2*f_r**2*gamma*mu_0 - 2*M_s*N_3*df**2*f_r**2*gamma*mu_0) + 1.0*M_s**4*N_2**2*gamma**4*mu_0**4/(df**2*f_r**4) + 4.0*M_s**4*N_2**2*gamma**4*mu_0**4/(df**4*f_r**2) - 2.0*M_s**4*N_2*N_3*gamma**4*mu_0**4/(df**2*f_r**4) - 8.0*M_s**4*N_2*N_3*gamma**4*mu_0**4/(df**4*f_r**2) + 1.0*M_s**4*N_3**2*gamma**4*mu_0**4/(df**2*f_r**4) + 4.0*M_s**4*N_3**2*gamma**4*mu_0**4/(df**4*f_r**2) - 4.0*M_s**3*N_2*gamma**3*mu_0**3/(2*B*df**2*f_r**2*gamma + M_s*N_1*df**2*f_r**2*gamma*mu_0 + M_s*N_2*df**2*f_r**2*gamma*mu_0 - 2*M_s*N_3*df**2*f_r**2*gamma*mu_0) + 4.0*M_s**3*N_3*gamma**3*mu_0**3/(2*B*df**2*f_r**2*gamma + M_s*N_1*df**2*f_r**2*gamma*mu_0 + M_s*N_2*df**2*f_r**2*gamma*mu_0 - 2*M_s*N_3*df**2*f_r**2*gamma*mu_0) + 1.0*M_s**2*df**2*gamma**2*mu_0**2/(2*B*df*f_r*gamma + M_s*N_1*df*f_r*gamma*mu_0 + M_s*N_2*df*f_r*gamma*mu_0 - 2*M_s*N_3*df*f_r*gamma*mu_0)**2 - 2.0*M_s**2*df*gamma**2*mu_0**2/(4*B**2*df*f_r**2*gamma**2 + 4*B*M_s*N_1*df*f_r**2*gamma**2*mu_0 + 4*B*M_s*N_2*df*f_r**2*gamma**2*mu_0 - 8*B*M_s*N_3*df*f_r**2*gamma**2*mu_0 + M_s**2*N_1**2*df*f_r**2*gamma**2*mu_0**2 + 2*M_s**2*N_1*N_2*df*f_r**2*gamma**2*mu_0**2 - 4*M_s**2*N_1*N_3*df*f_r**2*gamma**2*mu_0**2 + M_s**2*N_2**2*df*f_r**2*gamma**2*mu_0**2 - 4*M_s**2*N_2*N_3*df*f_r**2*gamma**2*mu_0**2 + 4*M_s**2*N_3**2*df*f_r**2*gamma**2*mu_0**2) + 4.0*M_s**2*f_r**2*gamma**2*mu_0**2/(2*B*df*f_r*gamma + M_s*N_1*df*f_r*gamma*mu_0 + M_s*N_2*df*f_r*gamma*mu_0 - 2*M_s*N_3*df*f_r*gamma*mu_0)**2 + 1.0*M_s**2*gamma**2*mu_0**2/(2*B*f_r*gamma + M_s*N_1*f_r*gamma*mu_0 + M_s*N_2*f_r*gamma*mu_0 - 2*M_s*N_3*f_r*gamma*mu_0)**2))
#        return y/amp_r_f/f_r
#
#    def make_params(self, **kwargs):
#        p = super(VNAFMR_EllipsoidDerivativeQuickModel, self).make_params(**kwargs)
#        p[self.prefix + "N_1"].vary = False
#        p[self.prefix + "N_2"].vary = False
#        p[self.prefix + "N_3"].vary = False
#        p[self.prefix + "N_1"].value = self.N[0]
#        p[self.prefix + "N_2"].value = self.N[1]
#        p[self.prefix + "N_3"].value = self.N[2]
#        p[self.prefix + "B"].vary = False
#        p[self.prefix + "M_s"].vary = False
#        p[self.prefix + "gamma"].vary = False
#        p[self.prefix + "phi"].vary = False
#        p[self.prefix + "phi"].min = -np.pi*2
#        p[self.prefix + "phi"].max= np.pi*2
#        p[self.prefix + "f_r"].min = 0
#        p[self.prefix + "df"].min = 0
#        p[self.prefix + "Z"].min = 0
#        return p
#
#    def guess(self, data, x=None, **kwargs):
#        center, hwhm, height = guess_peak(np.abs(data), x=x)
#        pars = self.make_params(Ms=height, f_r=center, df=hwhm, **kwargs)
#        pars[self.prefix + 'df'].set(min=0.0)
#        pars[self.prefix + 'B'].value = 100
#        pars[self.prefix + 'Z'].value = self.calc_Z(height, pars)
#        pars[self.prefix + 'M_s'].value = 1.5421e+05
#        pars[self.prefix + 'gamma'].value = 27497699359.848057
#        return pars
#
#    def recommended_roi(self, x, data, arg):
#        p = self.guess(data, x=x)
#        width = p[self.prefix + "df"].value * float(arg)
#        fr = p[self.prefix + "f_r"].value
#        min_idx = np.argmin(np.abs(x - (fr - width)))
#        max_idx = np.argmin(np.abs(x - (fr + width)))
#
#        return np.arange(min_idx, max_idx)

#%% Helper functions
def guess_peak(data, x=None, **kwargs):
    y = np.squeeze(np.real(data))
    x = np.squeeze(x)
    maxy, miny = np.max(y), np.min(y)
    imaxy = np.argmin(np.abs(y-maxy))
    halfmax_vals = np.where(y > (maxy+miny)/2.0)[0]
    hwhm = (x[halfmax_vals[-1]] - x[halfmax_vals[0]])/2.0
    center = x[imaxy]

    return center, hwhm, maxy

def guess_peak_lorentzian(data, x=None, **kwargs):
    y = np.abs(np.squeeze(np.real(data)))
    x = np.squeeze(x)

    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]
    
    # prepare fitting a lorentzian
    m_lin = LinearModel()
    m_lorentzian = LorentzianModel()
    p_lin = m_lin.guess(y, x=x)
    p_lorentzian = m_lorentzian.guess(y-m_lin.eval(x=x, params=p_lin), x=x)

    m = m_lin + m_lorentzian
    p = p_lin + p_lorentzian

    r = m.fit(y, x=x, params=p)

    return (r.best_values["center"],
            r.best_values["sigma"],
            r.best_values["amplitude"]/(np.pi*r.best_values["sigma"]))