import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
import scipy.signal as signal
import csv
from scipy.interpolate import UnivariateSpline as spline
from scipy import stats
import statistics

def bandpass_filter(s, fs, high, low, order):
    om = fs/2
    b, a = signal.butter(order, [high / om, low / om], btype="band")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)

def shelf_filter(s, fs, high):
    b, a = signal.butter(10, (high*2/fs), btype="high")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)
def SNR(fft,puls_freq):
    return statistics.mean(fft)/puls_freq
r=[]
g=[]
b=[]
def find_peak(fft, freqs):
    i = np.argmax(fft)  # Esay way to finding peek of fft
    peakFreq = freqs[i]
    #print("Pulse",peakFreq*60)
    return peakFreq*60
filnavn=["finger_data_24.csv","finger_14_data.csv","finger_data_20.csv","finger_data_23.csv","finger_11_data.csv"]
h_puls=["finger_data_26.csv"]
reflectans=["finger_data_32.csv","finger_data_40.csv", "finger_data_41.csv"]
for i in reflectans:
# Import data from bin file
    filename=i

    with open(filename) as csvfile:
        csvreader=csv.reader(csvfile, delimiter=" ")
        header = next(csvreader)
        data = []
        for datapoint in csvreader:
            values = [float(value) for value in datapoint]
            data.append(values)
        #sample_period *= 1e-6  # change unit to micro seconds
        sample_period = 1/40
        data = bandpass_filter(data, 1/sample_period, 0.5, 3.5, 10)
        data = signal.detrend(data, axis=0)  # removes DC component for each channel
        #data=data[:,0:2]

        # Generate time axis
        num_of_samples = data.shape[0]  # returns shape of matrix
        t = np.linspace(start=0, stop=num_of_samples*sample_period, num=num_of_samples)

        # Generate frequency axis and take FFT
        #cs = spline(t, data[:,1])
        #data = cs(data)
        freq = np.fft.fftfreq(n=num_of_samples, d=sample_period)
        spectrum = np.fft.fft(data,num_of_samples, axis=0)  # takes FFT of all channels
        print("SNR R",SNR(10*np.log(np.abs(spectrum[:,0])),10*np.log(abs(np.argmax(spectrum)))))
        print("SNR G",SNR(10*np.log(np.abs(spectrum[:,1])),10*np.log(abs(np.argmax(spectrum)))))
        print("SNR B",SNR(10*np.log(np.abs(spectrum[:,2])),10*np.log(abs(np.argmax(spectrum)))))
        for i in range(len(freq)):
            if freq[i]<=0.7 or freq[i]>=3.5:
                spectrum[i]=0
        #spectrum = shelf_filter(spectrum, 1/sample_period, 1)
        r.append(find_peak(spectrum[:,0],freq))
        g.append(find_peak(spectrum[:,1],freq))
        b.append(find_peak(spectrum[:,2],freq))
    
        plt.subplot(2, 1, 1)
        plt.title("Time domain signal")
        plt.xlabel("Time [s]")
        plt.ylabel("Voltage")
        plt.plot(t, data)
        plt.legend(["r", "g", "b"])

        plt.subplot(2, 1, 2)
        plt.title("Power spectrum of signal")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Power [dB]")
        plt.plot(freq, 20*np.log(np.abs(spectrum))) # get the power spectrum

        plt.show()
        #plt.savefig("noise.png")
        
print(r)  
print("Rød standaravik",statistics.stdev(r))
print("Grønn standaravik",statistics.stdev(g))
print("Blå standaravik",statistics.stdev(b))

print("Rød snitt",statistics.mean(r))
print("Grønn snitt",statistics.mean(g))
print("Blå snitt",statistics.mean(b))
    # Plot the results in two subplots
    # NOTICE: This lazily plots the entire matrixes. All the channels will be put into the same plots.
    # If you want a single channel, use data[:,n] to get channel n