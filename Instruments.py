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

class Scope(Instrument):
    def __init__(self, ID):
        Instrument.__init__(self, ID)
        self.inst.write("FPAnel:PRESS DEF")                 #defaul setup to start with clean slate
        sleep(sd)
        self.inst.write("SELect:CH2 1")                     #enalbe ch2
        sleep(sd)
        self.inst.write("SELect:CH1 1")                     #enable ch1
        sleep(sd)
        self.inst.write("MEASUREMENT:GATING OFF")        #measures everywhere
        
    def setVScale(self, ch, volt): 
        self.inst.write(ch + ":SCALE " + str(volt))            #set vertical scale

    def setM(self, source, m_type):
        self.inst.write("MEASUREMENT:IMMED:SOURCE1 " + source)    #specifies measurment 1 source as ch2
        self.inst.write("MEASUREMENT:IMMED:TYPE " + m_type)       #measuremnt type amplitude 

    def readM(self):
        self.inst.write("MEASUREMENT:IMMED:VALUE?")         #9.9100E+37 means NaN not a number aka value not available
        sleep(md)
        return float(self.inst.read())

class Funct(Instrument):
    def __init__(self, ID):
        Instrument.__init__(self, ID)
                                             #make sure to delay plenty for things to settle
    def setM(self, freq, amp, off):
        self.inst.write("VOLT:UNIT VPP")
        sleep(sd)
        #self.inst.write("APPL:SIN 1000,10,0.0")		# a sine wave, 500Hz, 10Vpp, 0v offset, phase offset 0 deg
        self.inst.write("APPL:SIN " + str(freq) + ',' + str(amp) + ',' + str(off))
        sleep(sd)
        self.inst.write("OUTP1 ON")
        sleep(sd)