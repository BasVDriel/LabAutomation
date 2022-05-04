import pyvisa
import time

rm =  pyvisa.ResourceManager()
print(rm.list_resources())
funct = rm.open_resource('USB0::0x0400::0x09C4::DG1D181501642::INSTR')
scope = rm.open_resource('USB0::0x0699::0x039B::C010288::INSTR')

def sleep(t):
    time.sleep(t)

def main():
    funct.write('*IDN?')
    sleep(0.05)
    print('\n' + funct.read())

    scope.write('*IDN?')
    sleep(0.05)
    print('\n' + scope.read())

    funct.write("VOLT:UNIT VPP")
    sleep(0.1)
    funct.write("APPL:SIN 500,10,0.0")		# a sine wave, 500Hz, 10Vpp, 0v offset, phase offset 0 deg
    sleep(0.1)
    funct.write("PHAS 0")
    sleep(0.1)
    funct.write("OUTP1 ON")
    sleep(0.1)

    scope.write("SELect:CH2 1")
    scope.write("SELect:CH1 1")
    scope.write("AUTOSet EXECute")
    scope.close()

if __name__ == "__main__":
    main()



