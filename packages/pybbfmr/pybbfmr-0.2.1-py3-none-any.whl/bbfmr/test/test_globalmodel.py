# -*- coding: utf-8 -*-
import unittest
from numpy import linspace, mean
from lmfit.models import LinearModel
from lmfit import Parameters
from bbfmr.global_model import GlobalCompositeModel
#from numpy.random import rand
#import matplotlib.pyplot as plt


class TestGlobalModel(unittest.TestCase):
    def setUp(self):
        self.slopes = [1, 1.2, 1.1]
        self.offsets = [0, 50, 25]
        self.x = [
            linspace(-50, 50, num=20, dtype=float)
            for i in range(len(self.slopes))]
        # noise = [(rand(*np.shape(self.x[0]))-0.5)*5 for i in range(len(self.x))]
        self.y = [
            self.x[i]*self.slopes[i] + self.offsets[i]# + noise[i] 
            for i in range(len(self.x))]
        
    def testSharedParameter(self):
        models = [
            LinearModel(independent_variables=["x"], prefix="m%d_" % i) 
            for i in range(len(self.x))]
        global_model = models[0]
        for i in range(1,len(models)):
            global_model = GlobalCompositeModel(global_model, models[i])
            
        params = Parameters()
        for i in range(len(models)):
            params += models[i].guess(self.y[i], x=self.x[i])            
        # models share slope but not offset parameter
        params["m1_slope"].expr = "m0_slope"
        params["m2_slope"].expr = "m0_slope"

        result = global_model.fit(self.y, x=self.x, params=params) 
        # global_model.plot(x=self.x, y=self.y, params=result.params)
        
        self.assertAlmostEqual(
            result.best_values["m0_slope"],
            mean(self.slopes))
        for i in range(len(self.x)):
            self.assertAlmostEqual(
                result.best_values["m%d_intercept" % i],
                self.offsets[i],
                places=5)
                
        return result, params