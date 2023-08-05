# -*- coding: utf-8 -*-
import unittest
from bbfmr.models.ferromagnet import FreeEnergy, Ferromagnet
from numpy.testing import assert_almost_equal
import numpy as np
from numpy import pi
mu_0 = 4*pi*1e-7


class TestFreeEnergy(unittest.TestCase):
    f = None
    M_sat = None

    def setUp(self):
        self.f = FreeEnergy()
        self.M_sat = float(140e3)
        self.f.M_sat = self.M_sat

    def tearDown(self):
        del(self.f)

    def test_no_anisotropy(self):
        self.f.H = [0, 0, 1/mu_0]
        assert_almost_equal(np.array(self.f.M)*mu_0,
                            np.array([0, 0, 1])*self.M_sat*mu_0)

    def test_shape(self):
        self.f.H = [0, 0.01/mu_0, 0.001/mu_0]
        self.f.add_shape([0, 0, 1])
        assert_almost_equal(np.array(self.f.M)*mu_0,
                            np.array([0, 1, 0])*self.M_sat*mu_0,
                            decimal=3)

    def test_uniaxial(self):
        self.f.H = [0, 0, 0.01/mu_0]
        self.f.add_uniaxial(-0.2/mu_0, [1, 0, 0])

        assert_almost_equal(np.array(self.f.M)*mu_0,
                            np.array([1, 0, 0])*self.M_sat*mu_0)

    def test_cubic(self):
        self.f.H = [0, 0, 1./mu_0]
        self.f.add_cubic(1, 0, [1, 0, 0])

        # FIXME: this test only tests syntax
        assert_almost_equal(np.array(self.f.M)*mu_0, 
                            np.array([0, 0, 1])*self.M_sat*mu_0)

    def test_lookup_uniaxial(self):
        self.f.H = [0, 0, 0.2/mu_0]
        self.f.add_uniaxial(1, [1, 0, 0])
        M_orig = self.f.M
        self.f.H = [0, 1/mu_0, 0/mu_0]
        self.f.find_equilibrium()
        self.f.H = [0, 0, 0.2/mu_0]
        self.f.find_equilibrium(lookup=True)
        assert_almost_equal(self.f.M, M_orig)

#if __name__ == '__main__':
#    unittest.main()

# %% For manual quick testing
import logging as l
l.getLogger("bbfmr.models.ferromagnet").setLevel(l.DEBUG)

f = FreeEnergy()
f.M_sat = float(140e3)
#f.add_shape([0, 0, 1])
f.add_cubic(K1=10e-3*140e3) # 10mT * 140kA/m = 1400 VsA/m³ = 1400 J/m³
f.report()
theta = np.linspace(pi/2,3/2*pi, num=50)
B = 0.6
angle = []
resfreq=[]
for t in theta:
    f.H = np.array([np.sin(t), 0, np.cos(t)])*B/mu_0
    angle.append(f.find_equilibrium())
    resfreq.append(Ferromagnet.resonance_frequency(F=f))

# %%
import matplotlib.pyplot as plt
plt.subplot(121)
angle = np.array(angle)
plt.plot(np.rad2deg(theta), np.cos(theta))
plt.plot(np.rad2deg(theta), np.cos(angle[:,0]), 'o', markersize=2)
resfreq=np.array(resfreq)
plt.subplot(122)
plt.plot(np.rad2deg(theta), resfreq/1e9, 'o', markersize=2)
plt.gca().ticklabel_format(style="sci", useOffset=False)
plt.tight_layout()