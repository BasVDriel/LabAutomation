# LabAutomation
An experiment for DIGOND at HHS university to automate various lab equipment with pyvisa. This code has only been tested on with the RIGOL DG1022A and the Textronix DPO2004B. 

# User guide
- Create a python environment with matplotlib, numpy and pyvisa. I used python 3.10.4 and anaconda.
- Git this repository
- With your environment enabled execute the following in the python console:
'''console
  import pyvisa
  rm = pyvisa.ResourceManager()
  print(rm.list_resources())
'''
- Now adjust the py.settings file as you wish
- Run bode.py
