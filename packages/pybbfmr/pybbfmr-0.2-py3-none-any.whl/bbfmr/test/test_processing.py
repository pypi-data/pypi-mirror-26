# -*- coding: utf-8 -*-
import unittest
from bbfmr.measurement import Measurement
from bbfmr.models.susceptibility import VNAFMR_EllipsoidDerivativeSphereModel
from bbfmr.models.dispersion import resfreq_kittel_ip
import bbfmr.processing as bp

import numpy as np

class TestComplexModel(unittest.TestCase):
    def setUp(self):
        f_lim = [27e9, 30e9]
        B_lim = [0, 1]
        M_s = 400e3
        gamma = 28.0249527e9
        x = np.linspace(*B_lim, num=500)
        y = np.linspace(*f_lim, num=20)
        x, y = np.meshgrid(x, y)
        z = VNAFMR_EllipsoidDerivativeSphereModel.func(
            y.T,
            B=x.T,
            f_r=resfreq_kittel_ip(
                x.T,
                M_eff=M_s, 
                gamma=gamma),
            M_s=M_s, 
            df=500e6,
            gamma=gamma, 
            Z=1, 
            phi=0
            )
        self.measurement = Measurement(X=x.T, Y=y.T, Z=z)

    def testDerivativeDivide_modamp1(self):
        m = self.measurement
        m.operations = []
        m.add_operation(bp.derivative_divide, modulation_amp=1, average=False)
        m.add_operation(bp.cut, x_idx=399)
        z_cut = m.Z        
        
        # calculate dd manually for this point
        m.operations = []
        m.add_operation(bp.cut, x_idx=398)
        z_m1 = m.Z
        m.operations = []
        m.add_operation(bp.cut, x_idx=399)
        z_0 = m.Z
        m.operations = []
        m.add_operation(bp.cut, x_idx=400)
        z_p1 = m.Z
        m.operations = []
        m.process()
        x_diff = (m.X[400,0]-m.X[398,0])/2 
        
        z_0_dd = (z_p1 - z_m1)/z_0 / x_diff 
        np.testing.assert_array_equal(z_cut, z_0_dd)
        
    def testDerivativeDivide_modamp2(self):
        m = self.measurement
        m.operations = []
        m.add_operation(bp.derivative_divide, modulation_amp=2, average=False)
        m.add_operation(bp.cut, x_idx=399)
        z_cut = m.Z        
        
        # calculate dd manually for this point and mod_amp 2
        m.operations = []
        m.add_operation(bp.cut, x_idx=397)
        z_m1 = m.Z
        m.operations = []
        m.add_operation(bp.cut, x_idx=399)
        z_0 = m.Z
        m.operations = []
        m.add_operation(bp.cut, x_idx=401)
        z_p1 = m.Z
        m.operations = []
        m.process()
        x_diff = (m.X[401,0]-m.X[397,0])/4
        
        z_0_dd = (z_p1 - z_m1)/z_0 / x_diff 
        np.testing.assert_array_equal(z_cut, z_0_dd)
        

if __name__ == '__main__':
    unittest.main()
