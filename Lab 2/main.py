import ras_import
import scipy.signal as signal
import concurrent.futures
import numpy as np

def bandpass(sig, fs,higcut,lowcut,order): #Bandpass filter you can use on the data.
    ny=fs*0.5

    b,a=signal.butter(order,[higcut/ny,lowcut/ny],btype='band')
    a=signal.detrend(a, axis=0)
    return signal.lfilter(b,a,sig)

def cross_correlate(sig1,sig2):
   cross=signal.correlate(sig1,sig2,mode='full',method='auto')
   lags=signal.correlation_lags(sig1.size,sig2.size,mode='full')
   return lags[np.argmax(np.abs(cross))]
def angle(filname):
    a,b= ras_import.raspi_import(filname)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures=[]
        for data in b:
            futures.append(executor.submit(bandpass,b))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        done=[]
        done.append(executor.submit(cross_correlate,args=[futures[0],futures[1]]))
        done.append(executor.submit(cross_correlate,args=[futures[1],futures[2]]))
        done.append(executor.submit(cross_correlate,args=[futures[0],futures[2]]))

    angle=np.arctan(np.sqrt(3)*(done[0]+done[2])/(done[0]-done[2]-2*done[1]))

    return angle/np.pi*180
