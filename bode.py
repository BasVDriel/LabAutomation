from binascii import Incomplete
import pyvisa as pv
import time as tm
import numpy as np
import matplotlib.pyplot as plt

from settings import *
from Instruments import *

def bodePlotInit(freq, magnitude, phase):
    mag = np.array(magnitude)
    phs = np.array(phase)
    plt.ion()
    fig = plt.subplot(2, 1, 1)
    plt.semilogx(freq, 20*np.log10(mag/(2*amplitude)))
    plt.grid()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain (dB)")
    plt.subplot(2, 1, 2)
    plt.semilogx(freq, phs)
    plt.grid()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Angle (degrees)")
    fig.draw()

def main():
    lowerLimit = np.log(fLow)/np.log(10)
    upperLimit = np.log(fHigh)/np.log(10)
    freq = np.logspace(lowerLimit, upperLimit, samples)

    funct = Funct('USB0::0x0400::0x09C4::DG1D181501642::INSTR')
    scope = Scope('USB0::0x0699::0x039B::C010288::INSTR')

    amplitudeRes = []
    phaseRes = []

    scope.setRef('CH1')
    scope.setHScale(0.5/fLow)
    vBaseline = startAmplitude
    pBaseline = 0
    vScale = vBaseline*0.4
    scope.setVScale('CH2', vScale)
    for f in freq:
        tries = 0
        incomplete = True
        while incomplete and (tries < 5):
            incomplete = False
            scope.setHScale(0.25/f)
            funct.setM(f, amplitude, 0.0)
            scope.setM('CH2', 'AMP')
            amp = scope.readM(f)
            scope.setM('CH2', 'PHA')
            phase = scope.readM(f)

            print("frequency: " + str(f) + " amplitude: " + str(amp) + " phase: " + str(phase))

            if amp < 0.9*vBaseline and not amp < 0.5*vBaseline: # adjust vertical scalling
                vScale = amp*0.3
                scope.setVScale('CH2', vScale)
                print("scaling down")
                tries+=1
                incomplete = True

            if (amp > 1.1*vBaseline or amp > 3.5*vScale) and not amp > 1.5*vBaseline:
                vScale = amp*1.3
                scope.setVScale('CH2', vScale)
                print("scaling up")
                tries+=1
                incomplete = True

            if amp == 9.91e+37:
                amp = amplitudeRes[-1]
                print("NaN error")
                tries+=1
                incomplete = True

            if phase == 9.91e+37:
                phase = phaseRes[-1]
                print("NaN error")
                tries+=1
                incomplete = True

            if phase > pBaseline+50 or phase < pBaseline-50:
                print("phase outlier")
                tries+=1
                incomplete = True

            
        vBaseline = amp
        amplitudeRes.append(amp)
        phaseRes.append(phase)
        pBaseline = phaseRes[-1]
    bodePlot(freq[0:len(amplitudeRes)], amplitudeRes, phaseRes)


if __name__ == "__main__":
    main()



