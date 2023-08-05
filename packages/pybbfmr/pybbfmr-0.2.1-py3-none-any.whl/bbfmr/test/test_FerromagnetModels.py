# -*- coding: utf-8 -*-
import unittest
from bbfmr.models import (VNAFMR_SimpleFieldModel, ComplexLinearModel,
                          VNAFMR_EllipsoidModel, FerromagnetEllipsoid,
                          VNAFMR_EllipsoidDerivativeModel)
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


class TestVNAFMRFieldModels(unittest.TestCase):
    def setUp(self):
        lim = [0, 2]
        self.params = {"dB": 0.01,
                       "f": 5e9,
                       "M_eff": 140e3,
                       "gamma": 28.024e9,
                       "slope": (1e-3 + 0.0005*1j),
                       "intercept": (1e-2 + 0.02*1j)}
        self.b = b = np.linspace(*lim, num=5000)
        self.chi = VNAFMR_SimpleFieldModel.chi_ip_yy(b, **self.params)
        self.params["Z"] = Z = 1
        self.params["phi"] = phi = 0
        self.y = Z*self.chi*np.exp(1j*phi)
        self.y_slope = b*self.params["slope"] + self.params["intercept"]

    def testFitFieldSuscept(self):
        m = VNAFMR_SimpleFieldModel()
        p = m.guess(self.y, x=self.b)
        p["f"].value = self.params["f"]
        p["f"].vary = False
        p["phi"].value = 0.1 # FIXME: this is very sensitive to initial guess
        r = m.fit(data=self.y, params=p, x=self.b)
#        r.plot()
#        print(r.fit_report())
        param_dict = r.params.valuesdict()
        self.assertEqual(len(r.params), 6)
        params0 = self.params.copy()
        params0["B_res"] = 1.036517765
        params0["slope"] = 0
        params0["intercept"] = 0

        for key, val in param_dict.items():
            self.assertAlmostEqual(val, params0[key])

    def testFitFieldSusceptDrift(self):
        y = np.add(self.y, self.y_slope)
        m1 = VNAFMR_SimpleFieldModel()
        m2 = ComplexLinearModel()
        p1 = m1.guess(y, x=self.b)
        p1["f"].value = self.params["f"]
        p1["f"].vary = False
        p1["phi"].value = 0

        p2 = m2.guess(y, x=self.b)
        m = m1 + m2
        r = m.fit(data=y, params=p1+p2, x=self.b)
       # r.plot()
       # pprint(r.fit_report())
        param_dict = r.params.valuesdict()
        self.assertEqual(len(r.params), 10)
        params0 = self.params.copy()
        params0["B_res"] = 1.036517765
        params0["slope"] = 0
        params0["intercept_im"] = np.imag(self.params["intercept"])
        params0["intercept_re"] = np.real(self.params["intercept"])
        params0["slope_im"] = np.imag(self.params["slope"])
        params0["slope_re"] = np.real(self.params["slope"])

        for key, val in param_dict.items():
            self.assertAlmostEqual(val, params0[key])


class TestVNAFMRFreqModels(unittest.TestCase):
    def setUp(self):
        self.mu_0 = 4*np.pi*10e-7
        lim = [9.8e9, 10.2e9]
        self.params = {"f_r": 1e10,
                       "M_s": 140e3,
                       "df": 30e6,
                       "gamma": 28.02495e9,
                       "N1": 0,
                       "N2": 0,
                       "N3": 1,
                       }
        self.params["N"] = (self.params["N1"],
                            self.params["N2"],
                            self.params["N3"])
        self.f = f = np.linspace(*lim, num=1000)
        self.chi = FerromagnetEllipsoid().chi(f, **self.params)
        self.params["Z"] = Z = 1
        self.params["phi"] = phi = 0
        self.params["B"] = 1
        self.y = Z*self.chi*np.exp(1j*phi)

    def testFitFreqSuscept(self):
        m = VNAFMR_EllipsoidModel()
        p = m.guess(self.y, x=self.f)
        p["B"].value = self.params["B"]
        p["M_s"].value = self.params["M_s"]
        p["gamma"].value = self.params["gamma"]
        p["N1"].value = self.params["N1"]
        p["N2"].value = self.params["N2"]
        p["N3"].value = self.params["N3"]
        p["df"].value = p["df"].value
        p["phi"].value = 0.1 #FIXME: quite sensitive to phi (cyclic? bounds?)
        p["Z"].value = 1

        y_noise = ((np.random.rand(len(self.y))-0.5)*np.max(self.y)/10 +
                   1j*(np.random.rand(len(self.y))-0.5)*np.max(self.y)/10)
        r = m.fit(data=self.y+y_noise, params=p, x=self.f, method="leastsq")
        np.testing.assert_array_less(np.abs(r.residual),
                                     np.ones(len(r.residual))*0.8)
        return r


class TestVNAFMRFreqDerModels(unittest.TestCase):
    def setUp(self):
        self.mu_0 = 4*np.pi*10e-7
        lim = [9.8e9, 10.2e9]
        self.params = {"f_r": 1e10,
                       "M_s": 140e3,
                       "df": 30e6,
                       "gamma": 28.02495e9,
                       "N1": 0,
                       "N2": 0,
                       "N3": 1,
                       }
        self.params["N"] = (self.params["N1"],
                            self.params["N2"],
                            self.params["N3"])
        self.f = f = np.linspace(*lim, num=1000)
        self.chi = FerromagnetEllipsoid.chi_derivative(f, **self.params)
        self.params["Z"] = Z = 1
        self.params["B"] = 1
        self.y = Z*self.chi

    def testFitFreqDerSuscept(self):
        m = VNAFMR_EllipsoidDerivativeModel()
        p = m.guess(self.y, x=self.f)
        p["B"].value = self.params["B"]
        p["M_s"].value = self.params["M_s"]
        p["gamma"].value = self.params["gamma"]
        p["N1"].value = self.params["N1"]
        p["N2"].value = self.params["N2"]
        p["N3"].value = self.params["N3"]
        p["df"].value = p["df"].value
        p["Z"].value = 1

        y_noise = ((np.random.rand(len(self.y))-0.5)*np.max(self.y)/10 +
                   1j*(np.random.rand(len(self.y))-0.5)*np.max(self.y)/10)
        r = m.fit(data=self.y+y_noise, params=p, x=self.f, method="leastsq")

        np.testing.assert_array_less(np.abs(r.residual),
                                     np.ones(len(r.residual))*0.8)
        return r

if __name__ == '__main__':
    plt.close("all")
    #unittest.main()

    t = TestVNAFMRFreqModels()
    t.setUp()
    r = t.testFitFreqSuscept()
