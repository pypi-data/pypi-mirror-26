import platform
import numpy as np
from toon.input.base_input import BaseInput

if platform.system() is 'Windows':
    import nidaqmx
    import nidaqmx.system
    from nidaqmx.constants import AcquisitionType, TerminalConfiguration
    from nidaqmx.stream_readers import AnalogMultiChannelReader
    from nidaqmx.errors import DaqError

    system = nidaqmx.system.System.local()
else:
    raise NotImplementedError('NIDAQ only available on Windows.')


class ForceTransducers(BaseInput):
    """1D transducers."""

    def __init__(self, **kwargs):

        BaseInput.__init__(self, **kwargs)

        self._device_name = system.devices[0].name  # Assume the first NIDAQ-mx device is the one we want
        self._channels = [self._device_name + '/ai' + str(n) for n in
                          [2, 9, 1, 8, 0, 10, 3, 11, 4, 12]]
        self._data_buffer = np.full(10, np.nan)

    def __enter__(self):
        self._device = nidaqmx.Task()

        self._device.ai_channels.add_ai_voltage_chan(
            ','.join(self._channels),
            terminal_config=TerminalConfiguration.RSE
        )

        self._device.timing.cfg_samp_clk_timing(200, sample_mode=AcquisitionType.CONTINUOUS)
        self._reader = AnalogMultiChannelReader(self._device.in_stream)
        self._device.start()
        return self

    def read(self):
        try:
            self._reader.read_one_sample(self._data_buffer, timeout=0)
            timestamp = self.time()
        except DaqError:
            return None
        return {'time': timestamp, 'data': np.copy(self._data_buffer)}

    def __exit__(self, type, value, traceback):
        self._device.stop()
        self._device.close()
