import ras_import
from scipy import signal
import numpy as np


file=""
sample_periode, data=ras_import.raspi_import(file,2)



signal_I=scipy.fft.rfft(data[]) #Tror disse linjene må flyttes innen for radar_speed
signal_Q=scipy.fft.rfft(data[])

def doppler(f_d,f_0):
    c=3e8
    v=(c*f_d)/(2*f_0)
    return v

def sinc_interp(x, s, u):
    if len(x) != len(s):
        raise ValueError('x and s must be the same length')
    
    # Find the period    
    T = s[1] - s[0]
    
    sincM = np.tile(u, (len(s), 1)) - np.tile(s[:, np.newaxis], (1, len(u)))
    y = np.dot(x, np.sinc(sincM/T))
    return y

def bandpass_filter(s, fs, high, low, order):
    om = fs/2
    b, a = signal.butter(order, [high / om, low / om], btype="band")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)

def radar_speed(data,Fs):
    fft, freqs=