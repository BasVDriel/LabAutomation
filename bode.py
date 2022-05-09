import pyvisa as pv
import time as tm
import numpy as np

sd = 0.1            #short delay
md = 0.5            #medium delay
ld = 1              #long delay
fLow = 10.0  
fHigh = 100000.0  
samples = 100.0

rm =  pv.ResourceManager()
print(rm.list_resources())
funct = rm.open_resource('USB0::0x0400::0x09C4::DG1D181501642::INSTR')
scope = rm.open_resource('USB0::0x0699::0x039B::C010288::INSTR')

def sleep(t):
    tm.sleep(t)

def scopeInit():
    scope.write("FPAnel:PRESS DEF")                 #defaul setup to start with clean slate
    sleep(sd)
    scope.write("SELect:CH2 1")                     #enalbe ch2
    sleep(sd)
    scope.write("SELect:CH1 1")                     #enable ch1
    sleep(sd)
    scope.write("MEASUREMENT:MEAS1:SOURCE1 CH2")    #specifies measurment 1 source as ch2
    sleep(sd)
    scope.write("MEASUREMENT:MEAS1:TYPE AMP")       #measuremnt type amplitude
    sleep(sd)
    scope.write("MEASUREMENT:MEAS1:STATE ON")       #display the measurement
    sleep(sd)
    scope.write("MEASUREMENT:GATING SCREEN")        #measures only within screen bounds
    sleep(sd)
    scope.write("HORIZONTAL:SCALE 400E-6")          #horzontal time scale
    sleep(ld)                                       #make sure to delay plenty for things to settle
    scope.write("MEASUREMENT:MEAS1:VALUE?")         #9.9100E+37 means NaN not a number aka value not available
    sleep(sd)
    print(scope.read())


def functInit():
    funct.write("VOLT:UNIT VPP")
    sleep(sd)
    funct.write("APPL:SIN 1000,10,0.0")		# a sine wave, 500Hz, 10Vpp, 0v offset, phase offset 0 deg
    sleep(sd)
    funct.write("OUTP1 ON")
    sleep(sd)


def main():
    funct.write('*IDN?')
    sleep(0.05)
    print('\n' + funct.read())

    scope.write('*IDN?')
    sleep(0.05)
    print('\n' + scope.read())

    functInit()
    scopeInit()

if __name__ == "__main__":
    main()



