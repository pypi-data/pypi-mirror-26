# -*- coding: utf-8 -*-
from guiqwt.plot import ImageDialog
from guidata import qapplication
from guidata.qt.QtGui import QColor, QAction
from guidata.configtools import get_icon
from guiqwt.shapes import PointShape
from guiqwt.tools import PointTool
from guidata.qt.QtGui import QFileDialog
from bbfmr.measurement.vna import VNAMeasurement
from bbfmr.measurement.vna import VNASeparateFieldsMeasurement
import bbfmr.processing as bp
import bbfmr.processing.filter as bpf
from bbfmr.gui.widgets import OperationsWidget, TdmsChannelSelectDialog
from nptdms import TdmsFile
import numpy as np
import jsonpickle
import os
import types 
from guidata.qt.QtCore import QT_VERSION_STR

QT5 = int(QT_VERSION_STR[0])>4

try:
    from peakit.controller.MeasurementController import MeasurementController
    peakit = True
except ImportError:
    peakit = False

def module_functions(module): 
    return [
        str(module.__dict__.get(a).__name__) for a in dir(module) 
            if isinstance(module.__dict__.get(a), types.FunctionType)
        ]
    

class Gui(object):
    def __init__(self, xlabel=None, ylabel=None, winTitle=None):
        """
        Boilerplate code for guiqwt image window. Includes qt application,
        x-,y-crosssection,  itemlistpanel, contrast adjustment.

        Returns
        --------
        win : guiqwt.plot.ImageDialog
        _app : PyQt4.QtGui.QApplication
        """

        self._app = qapplication()
        self.win = ImageDialog(
            edit = False, toolbar = True, wintitle = winTitle,
            options = dict(
                xlabel = xlabel,
                ylabel=ylabel,
                yreverse=False,
                lock_aspect_ratio = False))
        self.itemlist_panel = self.win.get_itemlist_panel()
        self.itemlist_panel.show()
        action = QAction(get_icon('busy.png'), "Reload", self.itemlist_panel)
        action.triggered.connect(self.reload_measurement)
        self.itemlist_panel.children()[-2].addAction(action)
        self.win.plot_widget.plot.SIG_ITEM_REMOVED.connect(self.remove_measurement)

        action = QAction(get_icon('save_all.png'), "Save all", self.itemlist_panel)
        action.triggered.connect(self.save_measurements)
        self.itemlist_panel.children()[-3].addAction(action)
        
        def fun(shape):
            shape.symbol.pen().setWidth(2)
            shape.symbol.setColor(QColor(255,0,0))
        self.win.add_tool(PointTool, handle_final_shape_cb=fun)
        self.win.get_xcs_panel().show()
        self.win.get_ycs_panel().show()
        self.win.get_contrast_panel().show()
        
        action = QAction(get_icon('fileopen.png'), "Open measurement", self.itemlist_panel)
        action.triggered.connect(self.load_measurement)
        self.win.get_toolbar().addAction(action)
        self.win.get_toolbar().addAction("Load VNA measurement", self.load_VNAMeasurement)
        self.win.get_toolbar().addAction("Load VNA measurement ...", self.load_VNAMeasurement_select_channels)
        self.win.get_toolbar().addAction("Load VNA fields measurement ", self.load_VNASeparateFieldsMeasurement)
        self.win.get_toolbar().addAction("Get points", self.get_points)
        self.win.get_toolbar().addAction("Export Data", self.save_current_data)

        
        if peakit:
            self.win.get_toolbar().addAction("Fitting tool ...",
                                             self.launchFittingTool)
            self.fitting_controller = MeasurementController()
        else:
            self.fitting_controller = None
            
        self.operations_widget = OperationsWidget()
        bbfmr_operations = ["bbfmr.processing.%s" % f for f in module_functions(bp)]
        bbfmr_operations += ["bbfmr.processing.filter.%s" % f for f in module_functions(bpf)]
        self.operations_widget.populate_available_operations(bbfmr_operations)
        self.itemlist_panel.layout().addWidget(self.operations_widget)
        self.itemlist_panel.listwidget.selectionModel().selectionChanged.connect(self.refresh_operations)
        self.operations_widget.operations_changed.connect(self.replot_measurement)

        self.plot_items = self.win.plot_widget.plot.items
        self.measurements = []
        
    def _get_current_plot_item(self):
        selection = self.itemlist_panel.listwidget.selectedIndexes()
        if len(selection) > 0:
            list_idx = selection[0].row()
            plot_item_idx = len(self.plot_items) - 1 - list_idx

            return self.plot_items[plot_item_idx], plot_item_idx
        else:
            return None, None

    def get_points(self):
        points = []
        for item in self.itemlist_panel.listwidget.items:
            if isinstance(item, PointShape):
                print(item.get_pos())
                points.append(item.get_pos())
                
        fname = Gui._get_save_file_name(caption='Save file', filter ="dat (*.dat *.)")
        np.savetxt(fname, points, delimiter= '\t')
        return points

    def refresh_operations(self):
        plot_item, _ = self._get_current_plot_item()
        if plot_item is not None:
            self.operations_widget.set_operations(plot_item.measurement.operations)

    def add_measurement(self, m, **kwargs):
        self.measurements.append(m)
        if "title" not in m.metadata or not m.metadata["title"]:
            m.metadata["title"] = m.metadata["fname"]

        _, image = self.imshow(m.X[:, 0], m.Y[0, :], m.Z.T,
                               title=m.metadata["title"],
                               **kwargs)
        image.measurement = m

    def remove_measurement(self, item):
        self.measurements.remove(item.measurement)
        
    def reload_measurement(self):
        """
        Trigger reloading of the currently selected measurement
        """
        plot_item, plot_item_idx = self._get_current_plot_item()
        if plot_item is None:
            return False
            
        plot_item.measurement.reload()
        self.replot_measurement()
        
    def replot_measurement(self):
        """
        Recreate theimage for the currently selected image. Taking into account
        any changed operations. Called when operations_widget.operations_changed
        is emitted
        """
        plot_item, plot_item_idx = self._get_current_plot_item()
        if plot_item is None:
            return False

        m = plot_item.measurement
        m.operations = self.operations_widget.get_operations()
        m.process()

        # recreate the image (this handles sorting of data and other bla)
        from guiqwt.builder import make
        image = make.xyimage(m.X[:, 0], m.Y[0, :], m.Z.T,
                             interpolation="nearest",
                             title=m.metadata["title"])

        # update image to the new data values
        plot_item.set_data(image.data)
        plot_item.set_xy(image.x, image.y)
        plot_item.plot().replot()
        #self.win.get_plot().replot()

    def imshow(self, x, y, data, title=None, cmap="RdYlGn"):
        """
        Create 2D xyimage for guiqwt image dialog



        Returns
        --------
        plot : guiqwt.image.ImagePlot
          Plot widget in guiqwt ImageDialog
        image : guiqwt.image.XYImageItem
           Newly created image object
        """
        from guiqwt.builder import make
        image = make.xyimage(x, y, data, interpolation="nearest", title=title, )
        plot = self.win.get_plot()
        plot.add_item(image)
        plot.do_autoscale()
        plot.replot()
        image.set_color_map(cmap)
        image.measurement = None

        return plot, image

    def pcolorshow(self, aX, aY, aData, title=None):
        """
        Create 2D xyimage for guiqwt image dialog

        Returns
        --------

        plot : ?
          Plot widget in guiqwt ImageDialog
        image : ?
           new image object
        """
        from guiqwt.builder import make
        image = make.pcolor(aX, aY, aData, interpolation="nearest", title=title, )
        plot = self.win.get_plot()
        plot.add_item(image)
        plot.do_autoscale()
        plot.replot()

        return plot, image

    def save_measurements(self):
        """
        Save measurements object descriptions to .measurement.json file(s)
        """
        folder = QFileDialog.getExistingDirectory(caption="Save measurements")

        for m in self.measurements:
            fname = os.path.basename(m.metadata["fname"]) + ".measurement.json"
            m.save(os.path.join(folder, fname))

    def _get_open_file_names(*args, **kwargs):
        if QT5:
            fnames, _ = QFileDialog.getOpenFileNames(*args, **kwargs)
        else:
            fnames = QFileDialog.getOpenFileNames(*args, **kwargs)
            
        return fnames
            
    def _get_save_file_name(*args, **kwargs):
        if QT5:
            fnames, _ = QFileDialog.getSaveFileName(*args, **kwargs)
        else:
            fnames = QFileDialog.getSaveFileName(*args, **kwargs)
            
        return fnames
            
        
    def load_measurement(self):
        """
        Load measurements according to .measurement.json file(s)
        """
        fnames = Gui._get_open_file_names(
            caption="Open Tdms file(s)",
            filter=u"Measurements Object Descriptions (*.measurement.json);;All files (*.*)")
        for fname in fnames:
            with open(fname, "r") as f:
                m = jsonpickle.loads(f.read())
            self.add_measurement(m, cmap="RdYlGn")
        return fnames

    def load_VNAMeasurement(self):
        """
        Load a VNA measurement from a TDMS file. Apply certain standard
        operations and plot data.
        """
        fnames = Gui._get_open_file_names(
            caption="Open Tdms file(s)",
            filter=u"TDMS (*.tdms);;All files (*.*)")
        for fname in fnames:
            m = VNAMeasurement(fname)
            m.add_operation(bp.derivative_divide, modulation_amp=4)
            m.add_operation(bp.mag)

            self.add_measurement(m, cmap="RdYlGn")
        return fnames

    def load_VNAMeasurement_select_channels(self):
        """
        Load a VNA measurement from a TDMS file. Apply certain standard
        operations and plot data. Allow to select used channels.
        """
        fnames = Gui._get_open_file_names(
            caption="Open Tdms file(s)",
            filter=u"TDMS (*.tdms);;All files (*.*)")
        for fname in fnames:
            tdms_file = TdmsFile(fname)
            channel_labels = ["Field channel",
                             "Frequency channel",
                             "Re(signal) channel",
                             "Im(signal) channel"]
            paths, accepted = TdmsChannelSelectDialog.get_group_channels(tdms_file=tdms_file,
                                                                                   channel_labels=channel_labels)
            m = VNAMeasurement(fname=fname,
                               tdms_file=tdms_file,
                               group=paths[2][0],
                               field_channel=paths[0][1],
                               freq_channel=paths[1][1],
                               signal_channel=paths[2][1],
                               imag_channel=paths[3][1])
            m.add_operation(bp.derivative_divide, modulation_amp=4)
            m.add_operation(bp.mag)

            self.add_measurement(m, cmap="RdYlGn")
        return fnames

    def launchFittingTool(self):
        """
        ...
        """
        plot_item, _ = self._get_current_plot_item()
        if plot_item is not None:
            measurement = plot_item.measurement
        else:
            measurement = None
        self.fitting_controller.measurement = measurement
        self.fitting_controller.show_view()

        
    def load_VNASeparateFieldsMeasurement(self):
        """
        Load a VNA measurement from a TDMS file with two magnetic field channels
        (field_before, field_after). Apply certain standard operations and 
        plot data. Allow to select used channels.
        """
        fnames = Gui._get_open_file_names(
            caption="Open Tdms file(s)",
            filter=u"TDMS (*.tdms);;All files (*.*)")
        for i, fname in enumerate(fnames):
            tdms_file = TdmsFile(fname)
            
            if i==0:
                channel_labels = [
                    "Field_before",
                    "Field_after",
                    "Frequency",
                    "Re(signal)",
                    "Im(signal)"]

                paths, accepted = TdmsChannelSelectDialog.get_group_channels(
                    tdms_file=tdms_file,
                    channel_labels=channel_labels)

            m = VNASeparateFieldsMeasurement(
                fname=fname,
                tdms_file=tdms_file,
                path_field_before=paths[0],
                path_field_after=paths[1],
                path_frequency=paths[2],
                path_real_signal=paths[3],
                path_imag_signal=paths[4])
            m.add_operation(bp.derivative_divide, modulation_amp=4)
            m.add_operation(bp.real)

            self.add_measurement(m, cmap="RdYlGn")
        return fnames
        
        
    def save_current_data(self):
        """
        The currently visible data will be exported in three columns
        (e.g. field, frequency, signal). Data will be saved in a .dat-file.
        """
        fname = Gui._get_save_file_name(caption='Save file', filter ="dat (*.dat *.)")
        plot_item, _ = self._get_current_plot_item()
        if plot_item is not None:
            plot_item.measurement.export_single_file(fname)       

        
        
    def run(self):
        self.win.show()
        self.win.exec()
        
g=Gui()
g.run()