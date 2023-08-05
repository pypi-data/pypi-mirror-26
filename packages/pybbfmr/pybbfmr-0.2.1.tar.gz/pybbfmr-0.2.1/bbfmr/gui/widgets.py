# -*- coding: utf-8 -*-
import inspect
from importlib import import_module
import sys
import guidata.qt.QtGui as qtgui
import guidata.qt.QtCore as QtCore
from guidata.configtools import get_icon
from guidata.qt.QtGui import QApplication, QWidget, \
    QVBoxLayout, QListWidget, QAbstractItemView, \
    QPushButton, QComboBox, QListWidgetItem, \
    QLineEdit, QLabel, QSpinBox, QCheckBox, QHBoxLayout, \
    QToolBar, QGridLayout, QDialog, QDialogButtonBox,\
    QTextEdit
try:
    import guidata.qt.QtWebKit as QtWebKit
    QTWEBKIT = True
except ImportError:
    QTWEBKIT = False
    
import re
import pydoc

import logging as l
l.basicConfig(level=l.DEBUG)


class QSliceInput(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.layout = QHBoxLayout()
        self.widgets = []
        for i, label_text in enumerate(["start", "stop", "step"]):
            label = QLabel(label_text)
            argument_widget = QLineEdit()

            self.layout.addWidget(label)
            self.layout.addWidget(argument_widget)
            self.widgets.append(argument_widget)
        self.setLayout(self.layout)
        self.slice = slice(None)
        
    def setSlice(self, slice):
        if slice is None:
            return False
        self.widgets[0].setText(str(slice.start))
        self.widgets[1].setText(str(slice.stop))
        self.widgets[2].setText(str(slice.step))
    
    def getSlice(self):
        return slice(*[int(w.text()) for w in self.widgets])
        
    
class OperationsWidget(QWidget):
    operations_changed = QtCore.pyqtSignal()
    operation_changed = QtCore.pyqtSignal(dict, int)
    operation_added = QtCore.pyqtSignal(dict, int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.widget_layout = QVBoxLayout()

        title_layout = QHBoxLayout()
        title_layout.addStretch()
        style = "<span style=\'color: #444444\'><b>%s</b></span>"
        title = QLabel(style % "Operations")
        title_layout.addWidget(title)
        title_layout.addStretch()
        self.widget_layout.addLayout(title_layout)

        # Create ListWidget
        self.list_widget = QListWidget()

        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        self.list_widget.model().rowsMoved.connect(lambda _: self.operations_changed.emit())
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.setSortingEnabled(False)
        self.list_widget.currentItemChanged.connect(self._populate_settings_update)
        self.widget_layout.addWidget(self.list_widget)

        otitle_layout = QHBoxLayout()
        otitle_layout.addStretch()
        otitle = QLabel(style % "Operation settings")
        otitle_layout.addWidget(otitle)
        otitle_layout.addStretch()
        self.widget_layout.addLayout(otitle_layout)

        self.operations_combo = QComboBox()
        self.operations_combo.currentIndexChanged.connect(self._populate_settings_add)
        self.widget_layout.addWidget(self.operations_combo)

        self.operation_settings = GenericOperationWidget()
        self.widget_layout.addWidget(self.operation_settings)

        self.toolbar = QToolBar()
        self.toolbar.addAction(get_icon('apply.png'), "Apply/Replace",
                               self._replace_operation)
        self.toolbar.addAction(get_icon('editors/edit_add.png'), "Add after",
                               self._add_operation)
        self.toolbar.addAction(get_icon('trash.png'), "Remove",
                               self._remove_operation)
        self.toolbar.addSeparator()
        self.toolbar.addAction(get_icon('quickview.png'), "Display help",
                               self._display_help)


        self.widget_layout.addWidget(self.toolbar)
        self.setLayout(self.widget_layout)

    def populate_available_operations(self, dict):
        """
        Populate combobox with available operation names
        """
        names = [name[17:] for name in dict]
        self.operations_combo.addItems(names)

    def set_operations(self, operations_dict):
        """
        Populate operations list with given dict of operations
        """
        self.list_widget.clear()
        for op in operations_dict:
            self.list_widget.addItem(Operation(op))

    def get_operations(self):
        """
        Return list of operations.
        """
        operations = []
        for i in range(self.list_widget.count()):
            op = self.list_widget.item(i)
            operations.append(op._op)

        return operations

    def _remove_operation(self):
        self.list_widget.takeItem(self.list_widget.currentRow())
        self.operations_changed.emit()

    def _add_operation(self):
        """
        Add operation currently in self.operation_settings to the operation
        list.

        Signals:
        ========
        Emits self.opeartion_added and self.operations_changed on success
        """
        op = self.operation_settings.get_operation()
        current_row = self.list_widget.currentRow()
        self.list_widget.insertItem(current_row + 1, Operation(op))
        index = self.list_widget.model().index(current_row + 1, 0)
        self.list_widget.setCurrentIndex(index)
        self.operation_added.emit(op, current_row + 1)
        self.operations_changed.emit()

    def _replace_operation(self):
        """
        Replace currently selected operation with operation in
        self.operation_settings (apply changed settings or replace operation).

        Signals:
        ========
        Emits self.operation_changed and self.operations_changed on success
        """
        op = self.operation_settings.get_operation()
        current_row = self.list_widget.currentRow()
        self.list_widget.takeItem(self.list_widget.currentRow())
        self.list_widget.insertItem(current_row, Operation(op))
        index = self.list_widget.model().index(current_row, 0)
        self.list_widget.setCurrentIndex(index)

        self.operation_changed.emit(op, current_row)
        self.operations_changed.emit()


    def _populate_settings_update(self, item):
        """
        Fill self.operation_settings with details of currently selected
        operation.
        """
        try:
            idx = self.operations_combo.findText(item._op["module"][17:])
            if idx >= 0:
                self.operations_combo.setCurrentIndex(idx)
            self.operation_settings.set_operation(item._op)
        except AttributeError:
            pass

    def _populate_settings_add(self, index):
        self.operation_settings.set_operation(
            {
                "module": "bbfmr.processing." + self.operations_combo.currentText()
            })
    
    def _display_help(self):
        package, fun = ("bbfmr.processing." + self.operations_combo.currentText()).rsplit('.', 1)
        module = import_module(package)
        
        dialog = QDialog(self)
        dialog.setMinimumSize(800,500)
        dialog.setWindowTitle("Documentation of %s.%s" % (package, fun))
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        dialog.setLayout(layout)
        
        if QTWEBKIT:
            view = QtWebKit.QWebView()
            html_doc = pydoc.html.docroutine(getattr(module, fun))
            view.setHtml(html_doc)
        else:
            view = QTextEdit(dialog)
            text_doc = pydoc.text.docroutine(getattr(module, fun))
            view.setText(text_doc)
            
        layout.addWidget(view)            
        dialog.show()
        

class GenericParameterWidget(QWidget):
    type_mapping = {"int": {"widget": QSpinBox,
                            "display_func": "setValue",
                            "display_conversion": int,
                            "get_func": "value",
                            "get_conversion": int},
                    "float": {"widget": QLineEdit,
                              "display_func": "setText",
                              "display_conversion": str,
                              "get_func": "text",
                              "get_conversion": float},
                    "bool": {"widget": QCheckBox,
                             "display_func": "setChecked",
                             "get_func": "isChecked"},
                    "slice": {"widget": QSliceInput,
                              "display_func": "setSlice",
                              "get_func": "getSlice"}}
    
    def __init__(self, parent=None, parameter_name=None, annotation=None):
        QWidget.__init__(self, parent)
        self.minimumHeight = 200 # FIXME: this does not have any effect 
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.checkbox = QCheckBox(parameter_name)
        font = qtgui.QFont()
        font.setPointSize(10)
        self.checkbox.setFont(font)
        self.checkbox.setChecked(True)
        self.checkbox.setToolTip(
            ((annotation["hint"] if "hint" in annotation else "Set the \"{name}\" parameter. ".format(name=parameter_name)) + 
             "\nIf unchecked, the default value ({value}) is used.".format(value=str(annotation["default"])))
            )
        self.layout.addWidget(self.checkbox)

        self.mapping = {}
        self.parameter_name = parameter_name
        self.annotation = annotation
        self.parameter_widget = self._create_parameter_widget(annotation)
        self.layout.addWidget(self.parameter_widget)

        self.checkbox.stateChanged.connect(self.set_enabled)
        
    def _create_parameter_widget(self, annotation):
        """Find and instancate widget corresponding to the parameter type."""
        if "widget" in annotation:
            self.mapping["widget"] = getattr(qtgui, annotation["widget"])
            self.mapping["display_func"] = annotation["display_func"]
            self.mapping["display_conversion"] = annotation["display_conversion"]
            self.mapping["get_func"] = annotation["get_func"]
        elif "type" in annotation:
            try:
                self.mapping = GenericParameterWidget.type_mapping[annotation["type"]]
            except KeyError:
                self.mapping["widget"] = QLabel(
                        "Parameter type {type} not supported in GUI.".format(type=annotation["type"]))
        else: 
            return None
        
        return self.mapping["widget"](self)            

    def set_parameter(self, parameter):
        """Set the currently displayed value(s) by operation parameter kwarg"""
        if not "display_conversion" in self.mapping or not callable(self.mapping["display_conversion"]):
            l.debug("Parameter {name} has no display conversion function.".format(name=self.parameter_name))
            self.mapping["display_conversion"] = lambda x:x
            
        if not callable(self.mapping["display_func"]):
            display = self.parameter_widget.__getattribute__(self.mapping["display_func"])
        else:
            display = self.mapping["display_func"]

        display(self.mapping["display_conversion"](parameter))
    
    def get_parameter(self):
        """Get currently displayed parameter value
        
        The return format is ready to be used as as **kwarg for the operation
        If a get_conversion is provided the raw input will be converted using 
        the get_conversion.Converts "" and "None" input to None.
        """ 
        if not self.checkbox.isChecked():
            return None
        
        try:
            parameter = self.parameter_widget.__getattribute__(self.mapping["get_func"])()
            if "get_conversion" in self.mapping:
                parameter = self.mapping["get_conversion"](parameter)
        except ValueError:
            l.warning('Could not parse parameter \'{name}\' value.'.format(name=self.parameter_name))
            parameter = None
        return parameter
    
    def set_enabled(self,state=True):
        self.checkbox.setChecked(state)
        #self.checkbox.setDisabled(not state)
        self.parameter_widget.setDisabled(not state)

class GenericOperationWidget(QWidget):
    def __init__(self, parent=None, op=None):
        QWidget.__init__(self, parent)
        self.widget_layout = QVBoxLayout()
        self.minimumHeight = 200 # FIXME: this does not have any effect
        self.setLayout(self.widget_layout)

        self._op = None
        self._widgets = []
        self._par_names = []

    def _clear_widgets(self):
        """
        Remove any dynamically created widget
        """
        for i in reversed(range(self.widget_layout.count())):
            widget = self.widget_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                widget.setParent(None)

        self._widgets = []

    def _set_widgets(self):
        """
        Parse operation (function arguments) and create widgets according to
        the function annotations. Fill with default or current argument values
        and display the widgets.
        """
        self._clear_widgets()

        package, fun = self._op["module"].rsplit('.', 1)
        module = import_module(package)
        self._op["function"] = getattr(module, fun)
        argspec = inspect.getfullargspec(self._op["function"])

        self._widgets = []
        widget = None
        for name, annotation in sorted(argspec.annotations.items()):
            annotation["default"] = argspec.defaults[argspec.args.index(name)]
            try:
                widget = GenericParameterWidget(parameter_name=name, annotation=annotation)
            except KeyError:
                l.warning(
                    ("Can't find wiget for type: {type} for parameter " +
                    "{name}").format(type=annotation["type"], name=name)
                    )
                continue
            
            try:
                l.debug(self._op["kwargs"])
                widget.set_parameter(self._op["kwargs"][name])
            except KeyError:
                widget.set_parameter(annotation["default"] or 0)
                widget.set_enabled(False)                

            self._widgets.append(widget)
            
        # Add widgets to layout
        if not self._widgets:
            self.widget_layout.addWidget(QLabel("No operation parameters"))
        for i, widget in enumerate(self._widgets):
            self.widget_layout.addWidget(self._widgets[i])

    def set_operation(self, op):
        """
        Set operation to represent and create widgets.
        """
        self._op = op
        self._set_widgets()

    def get_operation(self):
        """
        Returns operation dict for the current state of the parameter widgets.
        """
        kwargs = {w.parameter_name: w.get_parameter() for w in self._widgets if w.checkbox.isChecked()}
        self._op["kwargs"] = kwargs

        package, fun = self._op["module"].rsplit('.', 1)
        module = import_module(package)
        self._op["function"] = getattr(module, fun)
        return self._op        


class Operation(QListWidgetItem):
    def __init__(self, operation, parent=None):
        QListWidgetItem.__init__(self, parent)
        self._op = operation
        self.setText(self._op["module"][17:])

        
class TdmsChannelSelectWidget(QWidget):
    GROUP_PREFIX = "Read."

    def __init__(self, parent=None,
                 tdms_file=None,
                 group_label="Data group",
                 channel_labels=["X channel",
                                 "Y channel",
                                 "Z channel",
                                 "Z2 channel",
                                 ]):
        """
        Params
        ======
        twin_z : bool
            Allow to select two Z (data) channels
        group_label : str:
            Label text for group combo box
        channel_labels : list of str
            Label texts for channel combo boxes
        """
        QWidget.__init__(self, parent)
        self.widget_layout = QVBoxLayout()

        self.group_widgets = []
        self.channel_widgets = []
        for i, label_text in enumerate([group_label] + channel_labels):
            label = QLabel(label_text)
            channel_widget = QComboBox()
            channel_widget.addItem(label_text)
            channel_widget.setMinimumWidth(250)
            channel_widget.setDisabled(True)
            
            group_widget = QComboBox()
            group_widget.addItem(label_text)
            group_widget.setMinimumWidth(250)
            group_widget.setDisabled(True)

            layout = QHBoxLayout()
            layout.addWidget(label)
            layout.addWidget(group_widget)
            if i != 0:
                layout.addWidget(channel_widget)
            self.widget_layout.addLayout(layout)

            if i == 0:
                self.group_combo = group_widget
                self.group_combo.currentIndexChanged.connect(self.change_sub_channels)
            else:
                self.group_widgets.append(group_widget)
                self.channel_widgets.append(channel_widget)

                group_widget.currentIndexChanged.connect(self._populate_channels)


        self.setLayout(self.widget_layout)

        self.tdms_file = tdms_file

    @property
    def tdms_file(self):
        return self._tdms_file

    @tdms_file.setter
    def tdms_file(self, tdms_file):
        """
        Set the Tdms file in self.tdmsFiles at the specified index to be
        the currently used one and fill group and channel boxes appropriately)
        """
        self._tdms_file = tdms_file

        self._reset_channel_boxes()
        if tdms_file:
            self._populate_groups()
            self._populate_channels()

    def _reset_channel_boxes(self):
        for w in self.channel_widgets:
            w.clear()

    def _populate_groups(self, index=None):
        """
        Fill group_combo with the group names of the TDMS file that contain
        TdmsChannelSelectWidget.GROUP_PREFIX in their name. Try to reselect the
        item with the same index as selected before.

        Parameters
        ==========
        index: int
            unused, for compatibility with signals
        """
        self.blockSignals(True)
        old_index = self.group_combo.currentIndex()  

        for group_combo in ([self.group_combo] + self.group_widgets):
            group_combo.clear()
            for group in self.tdms_file.groups():
                if group.startswith(self.GROUP_PREFIX):
                    group_combo.addItem(group[len(self.GROUP_PREFIX):])
            group_combo.setEnabled(True)
            group_combo.setCurrentIndex(old_index)
            self.blockSignals(False)

    def _populate_channels(self, index=None):
        """
        Populate self.xChannelBox and self.yChannelBox with the channels
        of the selected group. If possible, use the channels selected before.

        Parameters
        ==========
        index: int
            unused, for compatibility with signals
        """
        for group_combo, channel_combo in zip(self.group_widgets, self.channel_widgets):
            
            group = self.GROUP_PREFIX + str(group_combo.currentText())
            channel_paths = [c.path for c in self.tdms_file.group_channels(group)]
    
            old_index = channel_combo.currentIndex()
        
            # Fill with new channels
            expr = re.compile(r"'/'(.+)'")
            channels = [expr.search(path).group(1) for path in channel_paths]
    
            channel_combo.clear()
            channel_combo.addItems(channels)
            channel_combo.setDisabled(False)
            channel_combo.setCurrentIndex(old_index)

    def get_group(self):
        """ Return selected group. No selection will return an empty string."""
        return self.GROUP_PREFIX + self.group_combo.currentText()

    def get_groups(self):
        """ Return selected group. No selection will return an empty string."""
        return [self.GROUP_PREFIX + w.currentText() for w in self.group_widgets]

    def get_channels(self):
        """
        Return list of selected channels (x, y, z and z2 if twin_x in was set
        to true). Channels where no selection has been made return an empy str.
        """
        return [w.currentText() for w in self.channel_widgets]
                
                
    def change_sub_channels(self):
        """
        Changes the channels according to the set top channel (group_combo)
        
        Parameters
        ==========
        index: int
            index to which the channels are set
        """
        new_index=self.group_combo.currentIndex()
        for group_combo in self.group_widgets:
            group_combo.setCurrentIndex(new_index)


class TdmsChannelSelectDialog(QDialog):
    def __init__(self, parent=None, **kwargs):
        QDialog.__init__(self)
        layout = QVBoxLayout()
        self.tdms_widget = TdmsChannelSelectWidget(parent=self, **kwargs)
        layout.addWidget(self.tdms_widget)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)


    @staticmethod
    def get_group_channels(parent = None, **kwargs):
        """
        Params
        ======
        parent: None
        
        **kwargs : 
            Passed to TdmsChannelSelectWidget.__init__()

        Returns
        =======
        paths : list
            path (tuple of [group channel]) of all selected channels
        """
        dialog = TdmsChannelSelectDialog(parent, **kwargs)
        result = dialog.exec_()
        groups = dialog.tdms_widget.get_groups()
        channels = dialog.tdms_widget.get_channels()

        return list(zip(groups, channels)), result == QDialog.Accepted


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = OperationsWidget()
    import bbfmr.processing as bp
    widget.populate_available_operations(list(filter(None, [("bbfmr.processing.%s" % s) if "__" not in s else None for s in dir(bp)])))
    ops = [{'module': "bbfmr.processing.limit_rois", 'kwargs':{'axis': 2}}]
    widget.set_operations(ops)
    widget.show()
    sys.exit(app.exec_())
