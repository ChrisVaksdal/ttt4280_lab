from numpy.lib.function_base import angle
import ras_import
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import statistics
sample_periode, data = ras_import.raspi_import('cardata2.bin', 2)


def doppler(f_d, f_0=24e9):
    c = 3e8
    v = (c*f_d)/(2*f_0)
    return v


def fart(v, f_0=24.13e9):
    return (2*f_0*v)/(3e8)


def freq_from_fft(sig, fs):
    """
    Estimate frequency from peak of FFT
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * signal.blackmanharris(len(sig))
    f = np.fft.fft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
    # true_i = np.polyfit(np.log(abs(f)), i,4)[0] #The function that should be here is no longer supported

    # Convert to equivalent frequency
    return fs * i / len(windowed)


def find_peak(fft, freqs):
    i = np.argmax(fft)  # Esay way to finding peek of fft
    peakFreq = freqs[i]
    print("Peak frequncey",peakFreq)
    return peakFreq


# The bandpass filter is not neede but can be used if the signal contanis more noise
'''
def bandpass_filter(s, fs, high, low, order=5):
    om = fs/2
    b, a = signal.butter(order, [high / om, low / om], btype="band")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)
'''


def complex_fft(data, Fs, real=0, imag=1):
    # print(data)
    ifi = data[:, real]
    ifq = data[:, imag]
    if(len(ifi) % 2 == 1):
        ifi = ifi[:-1]
        ifq = ifq[:-1]
    ifi = signal.detrend(ifi, axis=0)  # Remove the DC komponent
    ifq = signal.detrend(ifq, axis=0)
    # print(ifi)
    # print(ifq)
    complex_signal = np.vectorize(complex)(ifi, ifq)
    # FIndin the diffrences in angle betwen to phasor to calculate wich way the dopler shift is
    '''
    diff = np.rad2deg(
        angle(complex_signal[100]))-np.rad2deg(angle(complex_signal[200]))
    dir = int(diff)/abs(int(diff))
    '''
    fft = np.fft.fft(complex_signal)

    # print(fft)
    # Finds the frquency of the sampled fft
    fft=10*np.log10(abs(fft))
    freq = np.fft.fftfreq(fft.size, 1/Fs)
    #treshold=100
    #fft=fft[(fft>=-treshold) & (fft<=treshold)]
    #plt.plot(freq, fft)
    #plt.show()
    return freq, fft, dir


def radar_speed(data, Fs=32.5e3):
    freqs, fft, dir = complex_fft(data, Fs)
    print("Retningen til farten", dir)
    print(doppler(find_peak(fft,freqs)))
    neg=fft[:int(len(fft)/2)]
    freqs_neg=freqs[20:int(len(fft)/2)-21]
    pos=fft[int(len(fft)/2):-1]
    freqs_pos=freqs[21+int(len(fft)/2):-20]
    neg=neg[20:-20]
    pos=pos[20:-20]
    #print(len(pos))
    #print(len(freqs_pos))
    peak_pos=find_peak(pos,freqs_pos)
    peak_neg = find_peak(neg, freqs_neg)
    #print(peak_pos)
    if (abs(peak_pos)>abs(peak_neg)):
        speed=doppler(peak_pos)
    else:
        speed=doppler(peak_neg)
    
    return speed

def standar_div(antall):
    speed=[]
    for i in range(2,antall):
        sample_periode, data = ras_import.raspi_import('cardata'+str(i)+'.bin', 2)
        speed.append(radar_speed(data))
    return statistics.stdev(speed)

def power_sectrum(data,Fs=32.5e3):
    freqs, fft, dir = complex_fft(data, Fs)
    plt.plot(freqs, fft)
    plt.title("Power spectrum of FFT")
    plt.xlabel("Frewuency [Hz]")
    plt.ylabel("Power [dB]")
    plt.show()


print("Fart:", radar_speed(data))
power_sectrum(data)
print("Standar avik",standar_div(4))