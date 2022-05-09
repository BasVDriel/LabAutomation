import pyvisa
import time

rm =  pyvisa.ResourceManager()
print(rm.list_resources())
funct = rm.open_resource('USB0::0x0400::0x09C4::DG1D181501642::INSTR')
scope = rm.open_resource('USB0::0x0699::0x039B::C010288::INSTR')

def sleep(t):
    time.sleep(t)

def scopeInit():
    scope.write("FPAnel:PRESS DEF")  #defaul setup to start with clean slate
    sleep(0.1)
    scope.write("SELect:CH2 1")
    sleep(0.1)
    scope.write("SELect:CH1 1")
    sleep(0.1)
    scope.write("MEASUREMENT:MEAS1:SOURCE1 CH2") #specifies measurment 1 source as ch2
    sleep(0.1)
    scope.write("MEASUREMENT:MEAS1:TYPE AMP") #measuremnt type amplitude
    sleep(0.1)
    scope.write("MEASUREMENT:MEAS1:STATE ON") #display the measurement
    sleep(0.1)
    scope.write("MEASUREMENT:GATING SCREEN") #measures only within screen bounds
    sleep(0.1)
    scope.write("HORIZONTAL:SCALE 400E-6") #horzontal time scale
    sleep(1)                               #make sure to delay plenty for thins to settle
    scope.write("MEASUREMENT:MEAS1:VALUE?") #9.9100E+37 means NaN not a number aka value not available
    sleep(0.1)
    print(scope.read())


def functInit():
    funct.write("VOLT:UNIT VPP")
    sleep(0.1)
    funct.write("APPL:SIN 1000,10,0.0")		# a sine wave, 500Hz, 10Vpp, 0v offset, phase offset 0 deg
    sleep(0.1)
    funct.write("PHAS 0")
    sleep(0.1)
    funct.write("OUTP1 ON")
    sleep(0.1)

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



