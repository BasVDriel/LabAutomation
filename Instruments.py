import pyvisa as pv
import time as tm
from settings import *

def sleep(t):
    tm.sleep(t)

class Instrument:
    def __init__(self, ID):
        self.ID = ID
        self.inst = pv.ResourceManager().open_resource(self.ID)
        self.inst.write('*IDN?')
        sleep(sd)
        print('\n' + self.inst.read())  
        self.inst.timeout = 5000 

    def wait(self):
        self.inst.write("*OPC?")

class Scope(Instrument):
    def __init__(self, ID):
        Instrument.__init__(self, ID)
        self.inst.write("FPAnel:PRESS DEF")                 #defaul setup to start with clean slate
        self.wait()
        self.inst.write("SELect:CH2 1")                     #enalbe ch2
        self.wait()
        self.inst.write("SELect:CH1 1")                     #enable ch1
        self.wait()
        self.inst.write("MEASUREMENT:GATING OFF")        #measures everywhere
        self.wait()

    def setRef(self, ch):                                  # refernce for measurements that require one
        self.inst.write("MEASUREMENT:IMMED:SOURCE2 " + ch)
        self.wait()
        
    def setVScale(self, ch, volt): 
        self.inst.write(ch + ":SCALE " + str(volt))            #set vertical scale
        self.wait()

    def setHScale(self, time):
        self.inst.write("HORIZONTAL:SCALE " + str(time))
        self.wait()

    def setM(self, ch, m_type):
        self.inst.write("MEASUREMENT:IMMED:SOURCE1 " + ch)      #pecifies measurment 1 source as ch2
        self.wait()
        self.inst.write("MEASUREMENT:IMMED:TYPE " + m_type)       #measuremnt type amplitude
        self.wait()

    def readM(self, freq):
        self.inst.write("MEASUREMENT:IMMED:VALUE?")         #9.9100E+37 means NaN not a number aka value not available
        sleep(sd*5*(1/freq))
        return float(self.inst.read())

    def singleTrigger(self):
        self.inst.write("FPAnel:PRESS SING")    
        self.wait()


class Funct(Instrument):
    def __init__(self, ID):
        Instrument.__init__(self, ID)
        sleep
        self.inst.write("OUTP1 ON")
        sleep(sd)
                                             #make sure to delay plenty for things to settle
    def setM(self, freq, amp, off):
        self.inst.write("VOLT:UNIT VPP")
        sleep(sd)
        self.inst.write("APPL:SIN " + str(freq) + ',' + str(amp*2) + ',' + str(off))
        sleep(sd)