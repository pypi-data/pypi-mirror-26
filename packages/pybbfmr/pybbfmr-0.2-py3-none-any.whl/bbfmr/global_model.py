# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import operator
from lmfit.model import _ensureMatplotlib, CompositeModel

class GlobalCompositeModel(CompositeModel):
    _names_collide = (
        "\nTwo models have parameters named '{clash}'. "
        "Use distinct names.")
    _bad_arg   = "CompositeModel: argument {arg} is not a Model"

    def __init__(self, left, right, operator=operator.add, **kws):
        super().__init__(left, right, operator, **kws)

    def eval(self, params=None, **kwargs):
        # TODO: The following works, but evaluates each model for all input 
        #       parameters and selects the appropriate afterwards. 
        #       That's really inefficient when many models are combined /o\. 
        # TODO: At the same time then fixing the above one should document and
        #       assert the form of the supplied data and the independent var.
        #       The model expects this data as a list of lists:
        #       independent_var = [[x0_0, x0_1, ...], [x1_0, x1_1, ...], ...]
        #       data = [[d0_0, d0_1, ...], [d1_0, d1_1, ...], ...]
        return [
            vals[i] 
            for i, vals in enumerate(self.eval_components(params=params, **kwargs).values())]

    @_ensureMatplotlib
    def plot(
            self, x, y=None, params=None, datafmt='o', fitfmt='-',
            initfmt='--', xlabel=None, ylabel=None, yerr=None,
            numpoints=None, fig=None, data_kws={}, fit_kws={},
            init_kws={}, ax_res_kws={}, ax_fit_kws={},
            fig_kws={}, labels=None):
        if fig is None:
            fig = plt.figure()
        if labels is None:
            labels = range(len(x))

        for i in range(len(x)):
            plt.plot(
                x[i], y[i], 
                datafmt, label="data %s" % labels[i], 
                **data_kws)
            plt.plot(
                x[i], self.components[i].eval(x=x[i], params=params),
                fitfmt, label="best fit %s" % labels[i], 
                **fit_kws)
        plt.legend(loc="best")