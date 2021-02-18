import ras_import
from scipy import signal
import numpy as np


file=""
sample_periode, data=ras_import.raspi_import(file,2)



def doppler(f_d,f_0=24e9):
    c=3e8
    v=(c*f_d)/(2*f_0)
    return v

def freq_from_fft(sig, fs):
    """
    Estimate frequency from peak of FFT
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * np.blackmanharris(len(sig))
    f = np.rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
    true_i = np.parabolic(np.log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * true_i / len(windowed)


def bandpass_filter(s, fs, high, low, order):
    om = fs/2
    b, a = signal.butter(order, [high / om, low / om], btype="band")
    a = signal.detrend(a, axis=0)   # Remove DC-component.
    return signal.lfilter(b, a, s)

def complex_fft(data,Fs,real=0,imag=1):
    ifi=data[:,real]
    ifq=data[:,imag]
    if(len(ifi)%2==1):
        ifi=ifi[:-1]
        ifq=ifq[:-1]
    compelx_signal=complex(ifi,ifq)
    fft=np.fft.fft(compelx_signal)
    freq=np.fft.fftfreq(fft.size) #usikker på om dette er riktig
    return freq, fft

def radar_speed(data,Fs):
    fft, freqs=complex(data,Fs)
    peak_freq=freq_from_fft(fft,Fs)
    speed=doppler(peak_freq)
    return speed