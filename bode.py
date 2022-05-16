import pyvisa as pv
import time as tm
import numpy as np

from settings import *
from Instruments import *


def main():
    lowerLimit = np.log(fLow)/np.log(10)
    upperLimit = np.log(fHigh)/np.log(10)
    freq = np.logspace(lowerLimit, upperLimit, samples)

    scope = Scope('USB0::0x0699::0x039B::C010288::INSTR')
    funct = Funct('USB0::0x0400::0x09C4::DG1D181501642::INSTR')

    scope.readM()
    for f in freq:
        funct.setM(f, 10.0, 0.0)
        scope.setM('CH2', 'AMP')
        scope.readM()

if __name__ == "__main__":
    main()



