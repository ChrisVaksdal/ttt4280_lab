import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import csv
from scipy.interpolate import UnivariateSpline as spline

def bandpass_filter(s, fs, high, low, order):
    om = fs/2
    b, a = signal.butter(order, [high / om, low / om], btype="band")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)

def shelf_filter(s, fs, high):
    b, a = signal.butter(10, (high*2/fs), btype="high")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)
    return s

# Import data from bin file
filename="finger_11_data.csv"

with open(filename) as csvfile:
    csvreader=csv.reader(csvfile, delimiter=" ")
    header = next(csvreader)
    data = []
    for datapoint in csvreader:
        values = [float(value) for value in datapoint]
        data.append(values)

    data = signal.detrend(data, axis=0)  # removes DC component for each channel
    #sample_period *= 1e-6  # change unit to micro seconds
    sample_period = 1/40
    data = bandpass_filter(data, 1/sample_period, 0.8, 3.5, 10)

    # Generate time axis
    num_of_samples = data.shape[0]  # returns shape of matrix
    t = np.linspace(start=0, stop=num_of_samples*sample_period, num=num_of_samples)

    # Generate frequency axis and take FFT
    cs = spline(t, data[:,1])
    data = cs(data)
    freq = np.fft.fftfreq(n=num_of_samples, d=sample_period)
    spectrum = np.fft.fft(data, axis=0)  # takes FFT of all channels
    spectrum = shelf_filter(spectrum, 1/sample_period, 1)

    # Plot the results in two subplots
    # NOTICE: This lazily plots the entire matrixes. All the channels will be put into the same plots.
    # If you want a single channel, use data[:,n] to get channel n
    plt.subplot(2, 1, 1)
    plt.title("Time domain signal")
    plt.xlabel("Time [us]")
    plt.ylabel("Voltage")
    plt.plot(t, data)

    plt.subplot(2, 1, 2)
    plt.title("Power spectrum of signal")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Power [dB]")
    plt.plot(freq, 20*np.log(np.abs(spectrum))) # get the power spectrum

    plt.legend(["r", "g", "b"])
    plt.show()
    #plt.savefig("noise.png")
