# -*- coding: utf-8 -*-
from bbfmr.models import Ferromagnet, FreeEnergy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sympy import symbols, lambdify


sns.set_style("ticks")
pi = np.pi
mu_0 = 4*pi*1e-7

freq = np.linspace(.001e9, 2.5e9, num=100000)
B = np.linspace(0.01, 0.25, num=20)  # [T]#r = f.chiF_11(B, 10e9)
B_dir = np.array([0, 0, 1])
B_dir = B_dir/np.sqrt(np.dot(B_dir, B_dir))
f = FreeEnergy()
f.M_sat = 140e3
f.add_shape(N=[0, 0, 1])

plt.figure("resfreq")
plt.clf()
omega = []
for h in B/mu_0:
    f.H = B_dir*h
    omega.append(np.real(complex(
                Ferromagnet.resonance_frequency(f, method="Powell"))
                ))

plt.plot(B, np.array(omega), 's', label="resfreq from free energy")

#%%
plt.figure("chi")
plt.clf()
resfreq = []
for h in B/mu_0:
    f.H = B_dir*h
    chi = Ferromagnet.chi_f(f, method="Powell")
    c = lambdify(symbols("f"), chi)
    signal = c(freq)
    resfreq.append(freq[np.argmax(np.imag(signal))])

    plt.plot(freq, np.imag(signal))
#%%
plt.figure("resfreq")
plt.plot(B, np.array(resfreq)*2*pi, 'o', label="resfreq from chi")

# %%
plt.figure("chi_el")
plt.clf()
resfreq_el = []
for b in B:
    signal = Ferromagnet.chi_ellipsoid([b], freq, M_s=f.M_sat, alpha=1e-4, N=(0, 0, 1))
    resfreq_el.append(freq[np.argmax(np.imag(signal))])
    plt.plot(freq, np.imag(signal))

plt.figure("resfreq")
plt.plot(B, resfreq_el, 'o', label="resfreq from chi ellipsoid")
plt.legend()
