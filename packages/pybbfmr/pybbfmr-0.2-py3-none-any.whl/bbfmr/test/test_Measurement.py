# -*- coding: utf-8 -*-
import unittest
import os
from shutil import rmtree
from bbfmr.measurement import Measurement
from bbfmr.processing import real
import bbfmr.processing as p
from numpy.testing import assert_equal
import numpy as np
from pprint import pprint
import seaborn as sns
sns.set_style("ticks")
from numpy import pi
mu_0 = 4*pi*1e-7
import matplotlib.pyplot as plt
import jsonpickle


plt.close("all")
class TestMeasurement(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def generate_data(self):
        x = np.linspace(-3, 3, num=20)
        y = np.linspace(-2, 2, num=30)
        y, x = np.meshgrid(y, x)
        z = (1 - x / 2. + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)
        # x and y are bounds, so z should be the value *inside* those bounds.
        # Therefore, remove the last value from the z array.
        z = z[:, :]
        self.m = Measurement(X=x, Y=y, Z=z)

    def test_axes_consistency(self):
        self.m = Measurement(X=np.arange(0, 10),
                             Y=np.arange(10, 15),
                             Z=np.reshape(np.tile(np.arange(20, 25), reps=10),
                                          (10, 5)))
        self.m.add_operation(p.cut, x_idx=0)
        self.m.process()
        assert_equal(self.m.X, [np.tile(0, reps=5)])
        assert_equal(self.m.Y, [np.arange(10, 15)])
        self.m.replace_operation(p.cut, p.cut, y_idx=0)
        self.m.process()
        assert_equal(self.m.X, np.transpose([np.arange(0, 10)]))
        assert_equal(self.m.Y, np.transpose([np.tile(10, reps=10)]))

    def test_add_operation(self):
        self.generate_data()
        self.m.add_operation(p.gradient, axis=0)
        self.m.add_operation(p.cut, x_idx=0)
        self.m.process()
        self.m.plot()
        self.assertAlmostEqual(np.min(self.m.Z), -0.071751715403607239)

    def test_find_remove_operation(self):
        self.generate_data()
        self.m.add_operation(p.gradient, axis=0)
        self.m.add_operation(p.cut, y_idx=1)
        self.m.process()
        idx = self.m.find_operation(p.gradient)
        self.m.remove_operation(idx[0])
        self.m.process()
        self.assertAlmostEqual(np.min(self.m.Z), -0.12646124371669062)

    def test_replace_operation(self):
        self.generate_data()
        self.m.add_operation(p.cut, x_idx=1)
        self.m.process()
        self.m.replace_operation(p.cut, p.cut, y_idx=1)
        self.m.process()
        self.assertAlmostEqual(np.min(self.m.Z), -0.12646124371669062)

class TestMeasurementSavingLoading(unittest.TestCase):
    def setUp(self):
        x = np.linspace(-3, 3, num=50)
        y = np.linspace(-2, 2, num=80)
        y, x = np.meshgrid(y, x)
        z = ((1 - x / 2. + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)*1 +
             (1 - x / 5. + x ** 3 + y ** 6) * np.exp(-x ** 2 - y ** 2)*1j)
        self.m = Measurement(X=x, Y=y, Z=z)
        self.m.metadata["title"] = "test-measurement"
        self.m.process()
        self.m_re = Measurement(X=x, Y=y, Z=z)
        self.m_re.add_operation(real)
        self.m_re.process()

        self.path = "./test_measurement"

    def testSaving(self):
        if self.path:
            self.m.save(self.path, overwrite=True)
            os.remove(self.path + ".measurement.json")
        else:
            raise ValueError("Test is wrong, check saving path!")

    def testLoadingComplex(self):
        self.assertTrue(self.m.Z.dtype == complex)
        self.m.save(self.path, overwrite=True)

        with open(self.path + ".measurement.json", "r") as f:
            m = jsonpickle.loads(f.read())

        if self.path:
            os.remove(self.path + ".measurement.json")
        else:
            raise ValueError("Test is wrong, check saving path!")

        np.testing.assert_array_equal(m.X, self.m.X)
        np.testing.assert_array_equal(m.Y, self.m.Y)
        np.testing.assert_array_equal(m.Z, self.m.Z)

    def testLoadingReal(self):
        self.assertTrue(self.m_re.Z.dtype == float)
        self.m_re.save(self.path, overwrite=True)

        with open(self.path + ".measurement.json", "r") as f:
            m = jsonpickle.loads(f.read())

        os.remove(self.path + ".metadata.json")

        np.testing.assert_array_equal(m.X, self.m_re.X)
        np.testing.assert_array_equal(m.Y, self.m_re.Y)
        np.testing.assert_array_equal(m.Z, self.m_re.Z)
        self.assertEqual(m.operations, self.m_re.operations)

if __name__ == '__main__':
    unittest.main()