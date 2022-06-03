import pyvisa as pv
import time as tm
import numpy as np
import matplotlib.pyplot as plt

from settings import *
from Instruments import *

def bodePlot(freq, magnitude, phase):
    mag = np.array(magnitude)
    phs = np.array(phase)
    plt.subplot(2, 1, 1)
    plt.semilogx(freq, 20*np.log(mag/amplitude))
    plt.subplot(2, 1, 2)
    plt.semilogx(freq, phs)
    plt.show()

def main():
    lowerLimit = np.log(fLow)/np.log(10)
    upperLimit = np.log(fHigh)/np.log(10)
    freq = np.logspace(lowerLimit, upperLimit, samples)

    scope = Scope('USB0::0x0699::0x039B::C010288::INSTR')
    funct = Funct('USB0::0x0400::0x09C4::DG1D181501642::INSTR')

    amplitudeRes = []
    phaseRes = []

    scope.setRef('CH1')
    scope.setVScale('CH2', amplitude/4)
    scope.setHScale(0.5/fLow)
    vBaseline = amplitude
    scope.setVScale('CH2', amplitude*0.4)
    for f in freq:
        scope.setHScale(0.5/f)
        funct.setM(f, amplitude, 0.0)
        scope.setM('CH2', 'AMP')
        amp = scope.readM(f)
        scope.setM('CH2', 'PHA')

        if f < 25:
            scope.setHScale(0.25/f)

        phase = scope.readM(f)
        print("frequency: " + str(f) + " amplitude: " + str(amp) + " phase: " + str(phase))

        if amp < 0.9*vBaseline and not amp < 0.5*vBaseline:
            scope.setVScale('CH2', amp*0.3)

        vBaseline = amp
        amplitudeRes.append(amp)
        phaseRes.append(phase)

    bodePlot(freq, amplitudeRes, phaseRes)

if __name__ == "__main__":
    main()



