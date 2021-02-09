import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from math import atan, pi




""" Simple nth-degree butterworth bandpass-filter. """
def bandpass_filter(s, fs, high, low, order):
    om = fs/2
    b, a = signal.butter(order, [high / om, low / om], btype="band")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)

""" Returns delay between signals s1 and s2 as a number of samples. """
def cross_correlate_get_latency(s1, s2):
    cross = signal.correlate(s1, s2, mode="full", method="auto")
    lags = signal.correlation_lags(s1.size, s2.size, mode="full")
    lag = lags[np.argmax(cross)]
    return lag

""" Import sampled data from .bin-file. """
def import_data(path="adcData.bin", channels=3):
    with open(path, 'r') as fid:
        sample_period = np.fromfile(fid, count=1, dtype=float)[0]
        data = np.fromfile(fid, dtype=np.uint16)
        data = data.reshape((-1, channels))
    return sample_period*1000, data




""" Constants: """
C = 343.4                       # Speed of sound.
FS = 32500                      # Sampling frequency in Hz.
LOW_CUT = 100                   # Bottom of filter band in Hz.
HIGH_CUT = 2500                 # Top of filter band in Hz.
FILTER_ORDER = 3                # Order of bandpass-filter used to filter input.
SENSOR_DIST = 6.2 * 10**(-2)    # Distance between sensors in meters.

FT = 1 / FS



if __name__ == "__main__":
    # Get data:
    _, data = import_data()
    s1 = data[:,0]
    s2 = data[:,1]
    s3 = data[:,2]

    # Filter:
    s1 = bandpass_filter(s1, FS, LOW_CUT, HIGH_CUT, FILTER_ORDER)
    s2 = bandpass_filter(s2, FS, LOW_CUT, HIGH_CUT, FILTER_ORDER)
    s3 = bandpass_filter(s3, FS, LOW_CUT, HIGH_CUT, FILTER_ORDER)

    # Correlate and find latency:
    latencyNumSamples_s1s2 = cross_correlate_get_latency(s1, s2)
    latencyNumSamples_s1s3 = cross_correlate_get_latency(s1, s3)
    latencyNumSamples_s2s3 = cross_correlate_get_latency(s2, s3)

    """ Commented out because it does not affect results.
    # Convert to time in seconds
    latency_s1s2 = latencyNumSamples_s1s2 * FT
    latency_s1s3 = latencyNumSamples_s1s3 * FT
    latency_s2s3 = latencyNumSamples_s2s3 * FT
    """

    # The angle of the sound is calculated using theta = atan((sqrt(3) * (n12+n13)/(n12-n13-2n23))
    theta = atan((3**0.5) * (latencyNumSamples_s1s2 + latencyNumSamples_s1s3)/(latencyNumSamples_s1s2 - latencyNumSamples_s1s3 - 2*latencyNumSamples_s2s3)) # Angle of sound in radians.
    theta *= 360 / (2*pi)   # Convert angle to degrees.
    print("Angle theta: {}".format(theta))
