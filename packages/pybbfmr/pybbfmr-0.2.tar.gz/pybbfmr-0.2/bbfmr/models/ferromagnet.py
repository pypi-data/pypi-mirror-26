# -*- coding: utf-8 -*-
"""
Models that derive the susceptibility symbolically from the Free Energy or
for an Ellipsoid using the Landau-Lifshitz-Gilbert-Equation.

Mind that they are all slow in execution. For precalculated shapes and
parameter combinations see bbfmr.damping.susceptibility .
"""

from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

from lmfit import Model
import sympy as s
from sympy import symbols, Symbol
from sympy.utilities import lambdify

from logging import getLogger
l = getLogger(__name__)

from bbfmr.complex_model import ComplexModel
from bbfmr.models.susceptibility import guess_peak
import numpy as np
import scipy.constants as c
pi = np.pi
mu_0 = 4*pi*1e-7
mu_b = c.physical_constants["Bohr magneton"][0]


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def spherical_to_cartesian(r, theta, phi):
    x = r * (np.cos(phi)*np.sin(theta))
    y = r * (np.sin(phi)*np.sin(theta))
    z = r * (np.ones_like(phi)*np.cos(theta))

    return np.array((x, y, z)).T


def plot_surface_spherical(R, T, G, **kwargs):
    pkts = spherical_to_cartesian(R, T, G)
    X = pkts[:, :, 0]
    Y = pkts[:, :, 1]
    Z = pkts[:, :, 2]

    ax = plt.gca()
    mesh = ax.plot_surface(X, Y, Z, **kwargs)
    ax.set_xlim(-np.max(R), np.max(R))
    ax.set_ylim(-np.max(R), np.max(R))
    ax.set_zlim(-np.max(R), np.max(R))

    return mesh


class Ferromagnet(Model):
    """
    Ferromagnetic susceptibility model in SI units, [Hz] and [T]
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self.chi_f, *args, **kwargs)
        self.set_param_hint('sigma', min=0)

    def resonance_frequency(F, g=2.0023, method="Powell", **kwargs):
        """
        Calculate the resonance frequency of for a given free energy
        distribution F (contains external field H) using the rectrangular
        method (minimizing free energy and using free energy derivatives with
        respect to the equilibrium magnetizations) according to
        Baselgia et al. PRB 38, 4, 2237 (1988).

        Params
        ======
        F : FreeEnergy
            Free energy object

        Returns
        =======
        omega_r : numeric [Hz]
            Resonance frequency \omega_r/2pi in [Hz]
        """
        F.find_equilibrium(method=method)
        f = F.F_equilibrium
        M1, M2, M3 = symbols("M_1:4")
        gamma = symbols("\gamma")
        Ms = symbols("M_sat")
        omega_r = gamma * s.sqrt((Ms*f.diff(M1, 2) - f.diff(M3)) *
                                 (Ms*f.diff(M2, 2) - f.diff(M3)) -
                                 (Ms*f.diff(M1).diff(M2))**2
                                 )
        omega_r = omega_r.subs(M1, 0).subs(M2, 0).subs(M3, Ms)
        omega_r = omega_r.subs(Ms, F.M_sat)
        omega_r = omega_r.subs(symbols("\mu_0"), mu_0)
        omega_r = omega_r.subs(symbols("H_x"), F.H[0])
        omega_r = omega_r.subs(symbols("H_y"), F.H[1])
        omega_r = omega_r.subs(symbols("H_z"), F.H[2])
        omega_r = omega_r.subs(gamma, g*mu_b/c.h)

        return omega_r.evalf().as_real_imag()[0] # only real part

    def chi_symbolic(F, component=(1, 1), method="Powell", **kwargs):
        """
        Return a symbolic expression for the ferromagnetic susceptibility
        derived from the free energy F.
        """
        M1, M2, M3 = symbols(r"M_1:4")
        Ms = symbols(r"M_sat")
        a = symbols(r"\alpha")
        g = symbols(r"\gamma")
        o = symbols(r"\omega")

        F.find_equilibrium(method=method, **kwargs)
        f = F.F_equilibirum
        g11_3 = Ms*f.diff(M1, 2) - f.diff(M3)
        g22_3 = Ms*f.diff(M2, 2) - f.diff(M3)
        g12 = Ms*f.diff(M1).diff(M2)
        det = (g11_3 - s.I*o*a/g)*(g22_3 - s.I*o*a/g) - g12**2 - (o/g)**2

        if component == (1, 1):
            comp = + g22_3 - s.I*o*a/g
        elif component == (1, 2):
            comp = - g12 - s.I*o/g
        elif component == (2, 1):
            comp = - g12 + s.I*o/g
        elif component == (2, 2):
            comp = + g11_3 - s.I*o*a/g

        expr = symbols(r"\mu_0") / det * comp
        expr = expr.subs(M1, 0).subs(M2, 0).subs(M3, Ms)

        return expr

    def chi_f(F, g=2.0023, alpha=1e-4, component=(1, 1), **kwargs):
        """
        Return a symbolic expression for the ferromagnetic susceptibility
        derived from the free energy F. That contains only the frequency f
        [Hz] as symbolic variable
        """
        expr = Ferromagnet.chi_symbolic(F, component=component, **kwargs)
        expr = (expr.subs(symbols("M_sat"), F.M_sat)
                    .subs(symbols(r"\mu_0"), 4*pi*1e-7)
                    .subs(symbols("H_x"), F.H[0])
                    .subs(symbols("H_y"), F.H[1])
                    .subs(symbols("H_z"), F.H[2])
                    .subs(symbols(r"\gamma"), g*mu_b/c.h)
                    .subs(symbols(r"\alpha"), alpha)
                    .subs(symbols(r"\omega"), symbols("f")*2*pi))

        return expr

    def chi_ellipsoid(B, f, M_s=140e3, alpha=1e-3,
                      gamma=28.0249527e9, N=(0, 0, 1)):
        """
        (1,1) component of susceptibility according to "Deriving the Polder
        susceptibility tensor for an ellipsoid." as a function of frequency

        Params
        ======
        B : numeric [T]
        External magnetic field (along Z w/ respect to (nx, ny, nz))

        f : numeric [Hz]
        Driving frequency

        M_s : numeric [A/m]
        Saturation magnetization

        alpha : numeric [unitless]
        Gilbert damping constant

        gamma : numeric [Hz/T]
        Gyromagnetic ratio (default 28GHz/T)

        N : array like [unitless]
        Demagnetization tensor [nx ny nz]
        """
        pi = np.pi
        mu_0 = 4*pi*1e-7
        f_M = mu_0*M_s
        N = np.array(N)
        B_x = B + mu_0*(N[0]-N[2])*M_s
        B_y = B + mu_0*(N[1]-N[2])*M_s

        f_x = gamma*B_x
        f_y = gamma*B_y
        f_rr = np.sqrt((1+alpha)*f_x*f_y)

        df = alpha*(f_x+f_y)

        try:
            len(f)
        except TypeError:
            f = np.array([f])

        result = np.zeros((len(f_rr), len(f)), dtype=np.complex128)
        for n, f_r in enumerate(f_rr):
            numerator = f_M * (1+alpha**2)*f_y[n]-1j*alpha*f
            denominator = f_rr[n]**2 - f**2 - 1j*f*df[n]
            result[n, :] = (numerator/denominator)

        return np.squeeze(result)

    def grad_chi_f(B, f, **kwargs):
        """
        (1,1) component of susceptibility according to "Deriving the Polder
        susceptibility tensor for an ellipsoid." as a function of frequency

        Params
        ======
        B : numeric [T]
        External magnetic field (along Z w/ respect to (nx, ny, nz))

        f : numeric [Hz]
        Driving frequency

        **kwargs passed through to chiF_11
        """
        return Ferromagnet.chi_f(B, f, **kwargs)


class FreeEnergy():
    mu_0 = symbols("\mu_0")

    def __init__(self):
        self.F = None
        self.M_sat = float(100e3)
        self._H = [0, 0, 1]  # current direction and strength of H
        self._H_dir = []     # direction and strength for which min of F has 
                             # already been calculated

        self._theta = None   # calculated equlibrium magnetization direction
        self._phi = None     # corresponding to _H_min direction and strength
        self._theta_dir = []
        self._phi_dir = []
        self._F_objective = None
        self._F_diff = {}

        Mx, My, Mz = symbols("M_x:z")
        Hx, Hy, Hz = symbols("H_x:z")
        M = [Mx, My, Mz]
        H = [Hx, Hy, Hz]
        self.F = - self.mu_0 * np.dot(M, H)

    def reset_minimization(self):
        self._theta = None
        self._phi = None
        self._theta_dir = []
        self._phi_dir = []
        self._H_dir = []
        self._F_objective = None        
        self._F_diff = {}

    def add_uniaxial(self, K, axis):
        Mx, My, Mz = symbols("M_x:z")
        M = [Mx, My, Mz]
        self.F += K/symbols("M_sat") * np.dot(axis, M)**2
        self.reset_minimization()

    def add_shape(self, N):
        if len(N) != 3 and np.shape(N) != (3, 3):
            raise ValueError("N must denote the demagnetization tensor in the \
                              xyz coordinate system and be of rank 3 (3x3)\
                              or a vector of length 3 (diagonal elements)")
        if len(N) == 3:
            N = np.array(N)/np.sum(N)
            N = np.diag(N)

        Mx, My, Mz = symbols("M_x:z")
        M = [Mx, My, Mz]
        self.F += self.mu_0/2 * np.dot(M, np.dot(N, M))
        self.reset_minimization()

    def add_cubic(self, K1, K2=0, axis=None):
        Mx, My, Mz = symbols("M_x:z")
        self.F += 1/4  * K1/symbols("M_sat")**4 * (Mx**2*My**2 + Mx**2*My**2 + Mx**2*My**2)
        self.F += 1/16 * K2/symbols("M_sat")**6 * Mx**2 * My**2 * Mz**2
        self.reset_minimization()

    @property
    def F_spherical(self):
        """
        Return the free energy as a function of spherical coordinates \theta
        and \phi, the orientation of the magnetization in the xyz coordinate-
        system. This is the objective function to minimize in order to deter-
        mine the orientation of M for minimal free energy.
        Note that these are spherical coordinates neglecting the radius (i.e.
        magnitude of magnetization) we assume this is always equal to M_sat.
        Note: Here, the spherical coordinates are defined in the most common 
        way. For theta=0, M points along z; For phi=0 M points along x.
        """
        theta, phi, M_sat = symbols("theta phi M_sat")
        Mx = M_sat * s.sin(theta) * s.cos(phi)
        My = M_sat * s.sin(theta) * s.sin(phi)
        Mz = M_sat * s.cos(theta)

        return (self.F.subs(symbols("M_x"), Mx)
                      .subs(symbols("M_y"), My)
                      .subs(symbols("M_z"), Mz))
    
    @property
    def F_equilibrium(self):
        """
        Return the free energy in the coordinate system of the equilibrium mag-
        netization according to Baselgia et al. PRB 38, 4, 2237 (1988).
        """
        t, p = symbols("theta phi")
        r = np.array([[s.cos(t)*s.cos(p), -s.sin(p), s.sin(t)*s.cos(p)],
                      [s.cos(t)*s.sin(p),  s.cos(p), s.sin(t)*s.cos(p)],
                      [-s.sin(t),                 0, s.cos(t)]
                      ])
        M_1, M_2, M_3 = symbols("M_1:4")
        M_123 = [M_1, M_2, M_3]

        M_xyz = np.dot(r, M_123)

        F = (self.F.subs(symbols("M_x"), M_xyz[0])
                 .subs(symbols("M_y"), M_xyz[1])
                 .subs(symbols("M_z"), M_xyz[2]))
        return F.subs(t, self.theta).subs(p, self.phi)

    def diff(self, var, order=1):
        """ 
        Calculate the derivatives of the free energy
        
        Params:
        =======
        var: Symbol or string
            Symbol to derive F_equilibrium by. If var is a string, gets sympified
        order: numeric or Symbol
            Order of the derivative if string. If Symbol, calculate 
            diff(var).diff(order)
        """
        if not isinstance(var, Symbol):
            var = symbols(var)
            
        if var not in self._F_diff.keys():
            l.debug("calculating derivatives anew")
            self._F_diff[var] = {0: None,
                                 1: self.F_equilibrium.diff(var, 1),
                                 2: self.F_equilibrium.diff(var, 2)}
        if isinstance(order, Symbol) and  order not in self._F_diff[var].keys():
            self._F_diff[var][order] = self.diff(var).diff(order)

        return self._F_diff[var][order]
        
    @property
    def F_objective(self):
        if self._F_objective is None:
            l.debug("calculating new objective function")
            # prepare for numerical minimization
            expr = self.F_spherical.subs(symbols("M_sat"), self.M_sat)
            expr *= symbols("\mu_0")
            expr = expr.subs(symbols("\mu_0"), mu_0)  # typ. num. more stable
            self._F_objective = lambdify(symbols("theta phi H_x H_y H_z"), expr)
        return self._F_objective
        
    def find_equilibrium(self, lookup=True, method="Powell", **kwargs):
        """
        Minimize the free energy to deduce the equilibrium magnetization
        direction and update self._theta and self._phi

        **kwargs are passed to scipy.optimize.minimize()
        """
        if not self._H_dir:
            # choose external magnetic field diretion as start for optimization
            theta_start = np.arctan2(self.H[2],
                                     np.sqrt(self.H[0]**2+self.H[1]**2))
            phi_start = np.arctan2(self.H[1], self.H[0])
        else:
            if lookup:
                # lookup previously calculated theta, phi for current H-field
                _H_dir = np.asarray(self._H_dir)
                idx = np.where(((_H_dir[:, 0] == self.H[0]) &
                                (_H_dir[:, 1] == self.H[1]) &
                                (_H_dir[:, 2] == self.H[2])))[0]
                if len(idx) == 1:
                    l.debug("Found previously calculated magnetization direction for H=(%.3f, %.3f, %.3f)" % tuple(self.H)
                            + " at index %d" % idx[0])
                    self._theta = self._theta_dir[idx[0]]
                    self._phi = self._phi_dir[idx[0]]
                    return self._theta, self.phi
                
            # previously calculated result of most similar H-direction as start
            for h in np.array(self._H_dir) - np.array(self.H):
                dist = np.abs(np.mean(h))

            theta_start = self._theta_dir[np.argmin(dist)]
            phi_start = self._phi_dir[np.argmin(dist)]

        def func_v(x):
            return self.F_objective(*tuple(x), *self.H)

        # minimize free energy M_eqi starting from M_start as initial guess
        res = minimize(func_v, np.array([theta_start, phi_start]),
                       method=method, **kwargs)

        self._theta = res.x[0]
        self._phi = res.x[1]

        # store values and H for later lookup
        self._H_dir.append(self.H)
        self._theta_dir.append(self.theta)
        self._phi_dir.append(self.phi)

        return self.theta, self.phi

    @property
    def M(self):
        """
        Get current equilibrium magnetization direction
        """
        Mx = self.M_sat * np.sin(self.theta) * np.cos(self.phi)
        My = self.M_sat * np.sin(self.theta) * np.sin(self.phi)
        Mz = self.M_sat * np.cos(self.theta)

        M = [Mx, My, Mz]

        return M

    @property
    def theta(self):
        """
        Theta is the polar angle of in the most common definition of the
        spherical coordinate system,, i.e. for theta=0, M points along z
        """
        if self._theta is None or self._phi is None:
            self.find_equilibrium()
        return self._theta

    @property
    def phi(self):
        """
        Theta is the azimuthal angle of in the most common definition of the
        spherical coordinate system,, i.e. for phi=0 M points along x
        """
        if self._theta is None or self._phi is None:
            self.find_equilibrium()
        return self._phi

    @property
    def H(self):
        """
        The currently applied static external magnetic field
        """
        return self._H

    @H.setter
    def H(self, value):
        self._H = value
        self._theta = None

    def report(self):
        print("mu_0 M_{sat} = %.2e T" % (self.M_sat*mu_0))
        print("mu_0 H_0 = %s T" % str(np.array(self.H)*mu_0))
        print("mu_0 M_eqi = %s  T" % str(np.array(self.M)*mu_0))
        print("F = %s [J/m³]" % str(self.F))
        expr = (self.F_spherical.subs(symbols("H_x"), self.H[0])
                                .subs(symbols("H_y"), self.H[1])
                                .subs(symbols("H_z"), self.H[2]))
        expr = expr.subs(symbols("M_sat"), self.M_sat)
        expr *= symbols("\mu_0")  # typ. num. more stable
        expr = expr.subs(symbols("\mu_0"), mu_0)
        print("to be minimized: F*mu_0 = %s" % str(expr.simplify()))

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.axis("off")
        x = Arrow3D([-1.1, 1.1], [0, 0], [0, 0],
                    mutation_scale=20, lw=2, arrowstyle="-|>", color="grey")
        y = Arrow3D([0, 0], [-1.1, 1.1], [0, 0],
                    mutation_scale=20, lw=2, arrowstyle="-|>", color="grey")
        z = Arrow3D([0, 0], [0, 0], [-1.1, 1.1],
                    mutation_scale=20, lw=2, arrowstyle="-|>", color="grey")
        ax.add_artist(x)
        ax.add_artist(y)
        ax.add_artist(z)

        M_eqi = self.M
        m = Arrow3D([0, M_eqi[0]*mu_0], [0, M_eqi[1]*mu_0], [0, M_eqi[2]*mu_0],
                    mutation_scale=20, lw=2, arrowstyle="-|>", color="orange")
        ax.add_artist(m)

        h = Arrow3D([0, self.H[0]*mu_0], [0, self.H[1]*mu_0], [0, self.H[2]*mu_0],
                    mutation_scale=20, lw=2, arrowstyle="-|>", color="k")
        ax.add_artist(h)

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        # plt.legend(["M_{equilibrium}", "H_0"])
        plt.show()


class FerromagnetEllipsoid():
    """
    Ferromagnetic susceptibility model in SI units, [Hz] and [T] as sympy
    expression. This is used just to derive the derivative of chi analytically
    later on a numerical np model base on this will be used.
    """
    def __init__(self):
        self.chi_s = None
        self.chi_derivative_s = None

    def chi_symbolic(N=None):
        """ chi_11 as sympy expression """
        H = symbols(r"H", real=True)
        f = symbols(r"f", real=True)
        Ms = symbols(r"M_sat", real=True)
        a = symbols(r"\alpha", real=True)
        g = symbols(r"\gamma", real=True)
        mu_0 = symbols(r"\mu_0", real=True)
        f_r = symbols(r"f_r", real=True)
        df = symbols(r"\Delta_f", real=True)

        N1, N2, N3 = symbols("N_1:4", real=True)
        if N is None:
            N = [N1, N2, N3]
        else:
            N = np.array(N)/np.sum(N)

        f_M = g*mu_0*Ms/(2*s.pi)

        H_x = H + (N[0]-N[2])*Ms
        H_y = H + (N[1]-N[2])*Ms

        f_x = g*mu_0*H_x/(2*s.pi)
        f_y = g*mu_0*H_y/(2*s.pi)

        numerator = f_M * ((1+a**2)*f_y-1j*a*f)
        denominator = f_r**2 - f**2 - 1j*f*df

        chi = (numerator/denominator)

        return chi

    def chi_stripped(self, N=(1, 1, 0)):
        """ leave only potential fit parameters in equation """
        if self.chi_s is None:
            chi_s = FerromagnetEllipsoid.chi_symbolic(N=N)

            M1, M2, M3 = symbols(r"M_1:4", real=True)
            H = symbols(r"H", real=True)
            Ms = symbols(r"M_sat", real=True)
            a = symbols(r"\alpha", real=True)
            g = symbols(r"\gamma", real=True)
            mu_0 = symbols(r"\mu_0", real=True)

            N1, N2, N3 = symbols("N_1:4")
            if N is None:
                N = [N1, N2, N3]
            else:
                N = np.array(N)/np.sum(N)

            H_x = H + (N[0]-N[2])*Ms
            H_y = H + (N[1]-N[2])*Ms

            f_x = g*mu_0*H_x/(2*s.pi)
            f_y = g*mu_0*H_y/(2*s.pi)

            chi_s = chi_s.series(symbols(r"\alpha", real=True), 0, 2).removeO()
            df = symbols(r"\Delta_f", real=True)
            chi_s = chi_s.subs(a, df/(f_x+f_y))

            f_r = symbols(r"f_r", real=True)
            self.chi_s = chi_s.subs(f_x*f_y, f_r**2/(1+a**2))

        return self.chi_s

    def chi_derivative_symbolic(N=None):
        f = symbols(r"f", real=True)
        c = FerromagnetEllipsoid.chi_symbolic(N=N)

        return c.diff(f)

    def chi_derivative_stripped(self, N=None):
        """ leave only potential fit parameters in equation """
        if self.chi_derivative_s is None:
            f = symbols(r"f", real=True)
            c = self.chi_stripped(N=N)
            self.chi_derivative_s = c.diff(f)

        return self.chi_derivative_s

    def chi(self, f, H=1/mu_0, f_r=1e10, M_s=140e3, df=30e6,
            gamma=28.0249527e9, N=(0, 0, 1), **kwargs):
        """
        (1,1) component of susceptibility according to "Deriving the Polder
        susceptibility tensor for an ellipsoid." as a function of frequency

        Params
        ======
        B : numeric [T]
        External magnetic field (along Z w/ respect to (nx, ny, nz))

        f : numeric [Hz]
        Driving frequency

        M_s : numeric [A/m]
        Saturation magnetization

        alpha : numeric [unitless]
        Gilbert damping constant

        gamma : numeric [Hz/T]
        Gyromagnetic ratio (default 28GHz/T)

        N : array like [unitless]
        Demagnetization tensor [nx ny nz]
        """
        mu_0 = 4*np.pi*1e-7
        H_s = symbols(r"H", real=True)
        f_s = symbols(r"f", real=True)
        f_r_s = symbols(r"f_r", real=True)
        mu_0_s = symbols(r"\mu_0", real=True)
        Ms_s = symbols(r"M_sat", real=True)
        df_s = symbols(r"\Delta_f", real=True)
        g_s = symbols(r"\gamma", real=True)

        c = self.chi_stripped(N)
        c = (c.subs(df_s, df)
              .subs(g_s, gamma)
              .subs(Ms_s, M_s)
              .subs(mu_0_s, mu_0)
              .subs(H_s, H)
              .subs(f_r_s, f_r))

        c = s.utilities.lambdify(f_s, c, "numpy")
        return np.vectorize(c)(f)

    def chi_derivative(self, f, H=1/mu_0, f_r=1e10, Ms=140e3, df=30e6,
                       gamma=28.0249527e9, N=(0, 0, 1), **kwargs):
        """
        (1,1) component of susceptibility according to "Deriving the Polder
        susceptibility tensor for an ellipsoid." as a function of frequency,
        first derivative.

        Params
        ======
        B : numeric [T]
        External magnetic field (along Z w/ respect to (nx, ny, nz))

        f : numeric [Hz]
        Driving frequency

        M_s : numeric [A/m]
        Saturation magnetization

        alpha : numeric [unitless]
        Gilbert damping constant

        gamma : numeric [Hz/T]
        Gyromagnetic ratio (default 28GHz/T)

        N : array like [unitless]
        Demagnetization tensor [nx ny nz]
        """
        H_s = symbols(r"H", real=True)
        f_s = symbols(r"f", real=True)
        Ms_s = symbols(r"M_sat", real=True)
        g_s = symbols(r"\gamma", real=True)
        mu_0_s = symbols(r"\mu_0", real=True)
        f_r_s = symbols(r"f_r", real=True)
        df_s = symbols(r"\Delta_f", real=True)

        c = self.chi_derivative_stripped(N)
        c = (c.subs(df_s, df)
              .subs(g_s, gamma)
              .subs(Ms_s, Ms)
              .subs(mu_0_s, mu_0)
              .subs(H_s, H)
              .subs(f_r_s, f_r))

        c = s.utilities.lambdify(f_s, c, "numpy")
        return np.vectorize(c)(f)

        def resonance_frequency(self, H=None, Ms=None, df=None, gamma=None,
                                N=None):
            if H is None:
                H = symbols(r"H", real=True)
            if H is None:
                Ms = symbols(r"M_sat", real=True)
            if H is None:
                df = symbols(r"\Delta_f", real=True)
            if gamma is None:
                gamma = symbols(r"\gamma", real=True)

            mu_0 = symbols(r"\mu_0", real=True)

            H_x = H + (N[0]-N[2])*Ms
            H_y = H + (N[1]-N[2])*Ms
            f_x = gamma*mu_0*H_x/(2*s.pi)
            f_y = gamma*mu_0*H_y/(2*s.pi)
            a = df/(f_x+f_y)

            f_r = s.sqrt((1+a**2)*f_x*f_y)
            return f_r


#%% Partly symbolic models for chi
class VNAFMR_EllipsoidModel(ComplexModel):
    def func(self, x, B=1, f_r=1e10, M_s=140e3, df=30e6,
             gamma=28.0249527e9, N1=0, N2=0, N3=1, Z=1, phi=0):
        chi = self.F.chi(f=x, H=B/mu_0, f_r=f_r, M_s=M_s, df=df,
                         gamma=gamma, N=(N1, N2, N3))

        return Z*np.exp(1j*phi) * chi

    def __init__(self, N=None, **kwargs):
        self.F = FerromagnetEllipsoid()
        super(VNAFMR_EllipsoidModel, self).__init__(self.func,
                                                    independent_vars=['x'],
                                                    **kwargs)
        del(self.param_names[0])  # delete "self" parameter (model is stateful)
        self.name = "VNAFMR_EllipsoidModel"

    def fit(self, *args, **kwargs):
        return super(VNAFMR_EllipsoidModel, self).fit(*args, **kwargs,
            fit_kws={"diag": [1e9, 1, 1e9, 1e3, 1e6,
                              1e9, 1, 1, 1, 1, 1]})

    def make_params(self, **kwargs):
        p = super().make_params(**kwargs)
        p[self.prefix + "B"].vary = False
        p[self.prefix + "M_s"].vary = False
        p[self.prefix + "gamma"].vary = False
        p[self.prefix + "N1"].vary = False
        p[self.prefix + "N2"].vary = False
        p[self.prefix + "N3"].vary = False
        p[self.prefix + "phi"].min = -np.pi
        p[self.prefix + "phi"].max = np.pi
        p[self.prefix + "f_r"].min = 0
        p[self.prefix + "df"].min = 0
        p[self.prefix + "Z"].min = 0
        return p

    def guess(self, data, x=None, **kwargs):
        center, hwhm, height = guess_peak(np.abs(data), x=x)
        pars = self.make_params(Ms=height, f_r=center, df=hwhm, **kwargs)
        pars['%sdf' % self.prefix].set(min=0.0)
        return pars


class VNAFMR_EllipsoidDerivativeModel(ComplexModel):
    def func(self, x, B=1, f_r=1e10, M_s=140e3, df=30e6,
             gamma=28.0249527e9, N1=0, N2=0, N3=1, Z=1):
        chi = self.F.chi_derivative(f=x, H=B/mu_0, f_r=f_r, M_s=M_s,
                                                  df=df, gamma=gamma, N=(N1, N2, N3))

        return Z * chi

    def __init__(self, *args, N=None, **kwargs):
        self.F = FerromagnetEllipsoid()
        super(VNAFMR_EllipsoidDerivativeModel, self).__init__(
            self.func, *args,
            independent_vars=["x"],
            **kwargs)
        del(self.param_names[0])  # delete "self" parameter (model is stateful)
        self.name = "VNAFMR_EllipsoidDerivativeModel"

    def fit(self, *args, **kwargs):
        fit_kws_orig = kwargs.pop("fit_kws", {})
        if "diag" not in fit_kws_orig:
            fit_kws = {"diag": [1e9, 1, 1e9, 1e3, 1e6,
                                1e9, 1, 1, 1, 1, 1]}
            fit_kws.update(fit_kws_orig)
        else:
            fit_kws = fit_kws_orig

        return super(VNAFMR_EllipsoidDerivativeModel, self).fit(*args,
                                                                fit_kws=fit_kws,
                                                                **kwargs)

    def make_params(self, **kwargs):
        p = super(VNAFMR_EllipsoidDerivativeModel, self).make_params(**kwargs)
        p[self.prefix + "B"].vary = False
        p[self.prefix + "M_s"].vary = False
        p[self.prefix + "gamma"].vary = False
        p[self.prefix + "N1"].vary = False
        p[self.prefix + "N2"].vary = False
        p[self.prefix + "N3"].vary = False
        p[self.prefix + "f_r"].min = 0
        p[self.prefix + "df"].min = 0
        p[self.prefix + "Z"].min = 0
        return p

    def guess(self, data, x=None, **kwargs):
        center, hwhm, height = guess_peak(np.abs(data), x=x)
        pars = self.make_params(Ms=height, f_r=center, df=hwhm, **kwargs)
        pars[self.prefix + 'df'].set(min=0.0)
        pars[self.prefix + 'Z'].value = 1e9
        pars[self.prefix + 'B'].value = 100
        return pars

