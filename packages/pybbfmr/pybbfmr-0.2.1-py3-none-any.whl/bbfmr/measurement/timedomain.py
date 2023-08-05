# -*- coding: utf-8 -*-
"""
Class for timedomain measurements using a digitizer card
"""
from bbfmr.measurement import Measurement

import numpy as np
from nptdms import TdmsFile

# support versioning of processing operations; expose version of package
from bbfmr._version import get_versions
__version__ = get_versions()['version']
del(get_versions)


class TimeDomainMeasurement(Measurement):
    """Represents a time-domain measurement for the millikelvin EPR Setup at
    ABAQUS. Data is recorded using a digitizer card (e.g. from Gage). A
    measurement contains several time-traces which are functions of either
    magnetic field or pulse sequence.

    Each time-trace contains both the in-phase (real) and quadrature
    (imaginary) part, as well as the acquisition time of the digitizer card.

    Params
    ======
    group : str (Gage)
        Data group of the measurement.
    channel1 : str (Ch1(V))
        Channel name of in-phase channel. 
    channel2 : str (Ch2(V))
        Channel name of quadrature channel.
    magnet_name : str (VRM)
        Instrument name of the magnet
    magnet_channel : str (Z-Axis (T))
        Channel of the magnetic field
    awg_name : str (M8190A LoadSequence)
        Instrument name of the AWG LoadSequence instruction
    awg_channel : str (Sequence Number)
        Channel of the sequence number set
    sample_rate : float (None)
        Use pre-defined sample rate
    sample_length : float (None)
        Use pre-defined sample length
    """
    def __init__(self, fname=None, tdms_file=None, **kwargs):
        super(TimeDomainMeasurement, self).__init__(**kwargs)
        if fname or tdms_file:
            self.load_raw_data(fname, tdms_file=tdms_file, **kwargs)

    def load_raw_data(self, fname, *args, tdms_file=None, **kwargs):
        """Load time-domain data from tdms file and detect the type of
        sweep.
        """
        if tdms_file is None:
            tdms_file = TdmsFile(fname)
        tdms = tdms_file

        group          = kwargs.get('group', 'Gage')
        magnet_name    = kwargs.get('magnet_name', 'VRM')
        magnet_channel = kwargs.get('magnet_channel', 'Z-Axis (T)')
        awg_name       = kwargs.get('awg_name', 'M8190A LoadSequence')
        awg_channel    = kwargs.get('awg_channel', 'Sequence Number')
        channel1       = kwargs.get('channel1', 'Ch1(V)')
        channel2       = kwargs.get('channel2', 'Ch2(V)')
        
        set_group = 'Set.{:s}'.format(group)
        read_group = 'Read.{:s}'.format(group)

        sample_rate = kwargs.get('sample_rate', None) or \
            float(tdms.channel_data(set_group,
                  'Gage Settings.Acquisition.Sample Rate')[0])
        sample_length = kwargs.get('sample_length', None) or  \
            float(tdms.channel_data(set_group, 
                  'Gage Settings.Acquisition.Segment Size')[0])

        # Determine the type of sweep: Either a fieldsweep or a sequence
        # number sweep.
        fieldchannel = '{:s}.{:s}'.format(magnet_name, magnet_channel)
        sequencechannel = '{:s}.{:s}'.format(awg_name, awg_channel)
        channels = [c.path.split('/')[2].strip("'") for c in
                    tdms.group_channels(read_group)]
        if fieldchannel in channels:
            sweeptype = 'field'
            xlabel = 'Magnetic Field'
        elif sequencechannel in channels:
            sweeptype = 'sequence'
        else:
            # Probably just a single time trace
            sweeptype = 'none'

        # Extract magnetic fields used in the measurement
        if sweeptype == 'field':
            fields = tdms.channel_data(read_group, fieldchannel)
        else:
            try:
                magnet_set_group = 'Set.{:s}'.format(magnet_name)
                fields = np.array([tdms.channel_data(magnet_set_group,
                                  magnet_channel)], dtype=float)
            except:
                # No magnetic field was set at all
                fields = [0]

        # Extract sequence numbers
        if sweeptype == 'sequence':
            sequence_ids = tdms.channel_data(read_group, sequencechannel)
        else:
            awg_set_group = 'Set.{:s}'.format(awg_name)
            sequence_ids = np.array([tdms.channel_data(awg_set_group,
                                     awg_channel)[0]])
        # Convert to int
        sequence_ids = sequence_ids.astype(int)

        sweeppoints = max(len(sequence_ids), len(fields))
        data_shape  = (int(sweeppoints), int(sample_length))
        channel1    = np.reshape(tdms.channel_data(read_group, channel1),
                                 data_shape)
        channel2    = np.reshape(tdms.channel_data(read_group, channel2),
                                 data_shape)
        channel1    -= np.mean(channel1)
        channel2    -= np.mean(channel2)
        complex_signal = channel1 + 1.0j*channel2

        time = np.arange(0, sample_length * 1/sample_rate, 1/sample_rate)

        self.metadata["fname"] = fname
        self.metadata["load_raw_data_args"] = args
        self.metadata["load_raw_data_kwargs"] = kwargs
        self.metadata["yabel"] = 'Acquisition Time'
        self.metadata["zlabel"] = 'Complex signal'
        self.metadata["sample_rate"] = sample_rate
        self.metadata["sample_length"] = sample_length
        self.metadata["sweeptype"] = sweeptype
        self.metadata["title"] = os.path.basename(fname)

        if sweeptype == 'none':
            self.set_XYZ(None, time, complex_signal)
            self.metadata["xlabel"] = ''
        elif sweeptype == 'field':
            self.set_XYZ(fields, time, complex_signal)
            self.metadata["xlabel"] = 'Magnetic Field'
        elif sweeptype == 'sequence':
            self.set_XYZ(sequence_ids, time, complex_signal)
            self.metadata["xlabel"] = 'Sequence ID'

