# -*- coding: utf-8 -*-
import unittest
from bbfmr.complex_model import ComplexModel
from bbfmr.models import ComplexLinearModel
from lmfit.models import LinearModel
import numpy as np


def f_chiprime(x, w_M=1, w_res=1, alpha=20, **kwargs):
    def fun(w):
        w = x
        return (w_M*(-1.0*1j*alpha - 1)/(alpha**2*w**2 + (-w + w_res)**2) +
                w_M*(-2*alpha**2*w - 2*w + 2*w_res) *
                (-1.0*1j*alpha*w - w + w_res) /
                (alpha**2*w**2 + (-w + w_res)**2)**2)
    return fun(np.array(x))

class TestComplexModel(unittest.TestCase):
    def setUp(self):
        lim = [-0.5, 0.5]
        self.params = {"w_M": 100,
                       "w_res": 1,
                       "alpha": 20,
                       "slope_re": 1000,
                       "slope_im": 1110,
                       "intercept_re": 100,
                       "intercept_im": -100,
                       }
        self.x = x = np.linspace(*lim, num=500)
        self.y = f_chiprime(x, **self.params)
        self.y_slope = (x*(self.params["slope_re"] +
                           1j*self.params["slope_im"]) +
                        self.params["intercept_re"] +
                        1j*self.params["intercept_im"])

    def testFitComplexModel(self):
        m = ComplexModel(f_chiprime)
        p = m.make_params()
        r = m.fit(data=self.y, params=p, x=self.x)
        param_dict = r.params.valuesdict()
        self.assertEqual(len(r.params), 3)
        for key, val in param_dict.items():
            self.assertAlmostEqual(val, self.params[key])
        np.testing.assert_almost_equal(r.best_fit, self.y)

    def testCompositeModel(self):
        m1 = ComplexModel(f_chiprime, prefix="m1_")
        m2 = ComplexLinearModel(prefix="m2_")
        m = m1 + m2
        p = m1.make_params() + m2.make_params()
        r = m.fit(data=self.y+self.y_slope, params=p, x=self.x)
        self.assertEqual(len(r.params), 7)
        np.testing.assert_almost_equal(r.best_fit, self.y+self.y_slope)

    def testComplexLinearModel(self):
        m = ComplexLinearModel()
        p = m.guess(self.y_slope+0.1*self.x, x=self.x)
        #p=m.make_params()
        r = m.fit(data=self.y_slope, params=p, x=self.x)
        param_dict = r.params.valuesdict()

        self.assertEqual(len(r.params), 4)
        for key, val in param_dict.items():
            self.assertAlmostEqual(val, self.params[key])
        np.testing.assert_almost_equal(r.best_fit, self.y_slope)

if __name__ == '__main__':
    unittest.main()
